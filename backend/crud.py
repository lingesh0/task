from sqlalchemy.orm import Session, joinedload
from . import models, schemas
from datetime import datetime
from typing import List, Optional

def create_session(db: Session, session: schemas.SessionCreate):
    """Create a new session"""
    db_session = models.Session(
        title=session.title,
        goal=session.goal,
        scheduled_duration=session.scheduled_duration
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_session(db: Session, session_id: int):
    """Get a session by ID"""
    return db.query(models.Session).filter(models.Session.id == session_id).first()

def get_sessions(db: Session, skip: int = 0, limit: int = 100):
    """Get all sessions with pagination"""
    return db.query(models.Session).offset(skip).limit(limit).all()

def update_session_status(db: Session, session_id: int, status: str, **kwargs):
    """Update session status and other fields"""
    session = get_session(db, session_id)
    if session:
        session.status = status
        for key, value in kwargs.items():
            setattr(session, key, value)
        db.commit()
        db.refresh(session)
    return session

def start_session(db: Session, session_id: int):
    """Start a session"""
    return update_session_status(db, session_id, "active", start_time=datetime.now())

def pause_session(db: Session, session_id: int, reason: str):
    """Pause a session and create interruption record"""
    session = get_session(db, session_id)
    if session and session.status == "active":
        # Create interruption record
        interruption = models.Interruption(
            session_id=session_id,
            reason=reason
        )
        db.add(interruption)
        
        # Update session status
        session.status = "paused"
        db.commit()
        db.refresh(session)
        return session
    return None

def resume_session(db: Session, session_id: int):
    """Resume a paused session"""
    session = get_session(db, session_id)
    if session and session.status == "paused":
        session.status = "active"
        db.commit()
        db.refresh(session)
        return session
    return None

def complete_session(db: Session, session_id: int):
    """Complete a session and determine final status"""
    session = get_session(db, session_id)
    if session and session.status in ["active", "paused"]:
        session.end_time = datetime.now()
        
        # Calculate actual duration
        if session.start_time:
            actual_duration = (session.end_time - session.start_time).total_seconds() / 60
            
            # Count interruptions
            interruption_count = len(session.interruptions)
            
            # Determine final status based on business rules
            if interruption_count > 3:
                session.status = "interrupted"
            elif actual_duration > session.scheduled_duration * 1.1:
                session.status = "overdue"
            elif session.status == "paused" and not any(i.pause_time > session.start_time for i in session.interruptions):
                session.status = "abandoned"
            else:
                session.status = "completed"
        
        db.commit()
        db.refresh(session)
        return session
    return None

def get_session_history(db: Session):
    """Get session history with statistics"""
    sessions = db.query(models.Session).options(joinedload(models.Session.interruptions)).order_by(models.Session.created_at.desc()).all()
    
    total_sessions = len(sessions)
    completed_sessions = len([s for s in sessions if s.status == "completed"])
    interrupted_sessions = len([s for s in sessions if s.status == "interrupted"])
    overdue_sessions = len([s for s in sessions if s.status == "overdue"])
    abandoned_sessions = len([s for s in sessions if s.status == "abandoned"])
    
    # Calculate total productive time (only completed sessions)
    total_productive_time = 0
    total_interruptions = 0
    
    for session in sessions:
        if session.status == "completed" and session.start_time and session.end_time:
            actual_duration = (session.end_time - session.start_time).total_seconds() / 60
            total_productive_time += actual_duration
        total_interruptions += len(session.interruptions)
    
    return schemas.SessionHistory(
        sessions=sessions,
        total_sessions=total_sessions,
        completed_sessions=completed_sessions,
        interrupted_sessions=interrupted_sessions,
        overdue_sessions=overdue_sessions,
        abandoned_sessions=abandoned_sessions,
        total_productive_time=total_productive_time,
        total_interruptions=total_interruptions
    )
