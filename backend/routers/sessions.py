from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/", response_model=schemas.Session)
def create_session(session: schemas.SessionCreate, db: Session = Depends(get_db)):
    """Create a new deep work session"""
    return crud.create_session(db=db, session=session)

@router.get("/history", response_model=schemas.SessionHistory)
def get_session_history(db: Session = Depends(get_db)):
    """Get session history with statistics"""
    return crud.get_session_history(db=db)

@router.get("/{session_id}", response_model=schemas.Session)
def get_session(session_id: int, db: Session = Depends(get_db)):
    """Get a specific session by ID"""
    session = crud.get_session(db=db, session_id=session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.patch("/{session_id}/start", response_model=schemas.Session)
def start_session(session_id: int, db: Session = Depends(get_db)):
    """Start a planned session"""
    session = crud.get_session(db=db, session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status != "planned":
        raise HTTPException(status_code=400, detail="Session can only be started if it's in planned status")
    
    return crud.start_session(db=db, session_id=session_id)

@router.patch("/{session_id}/pause", response_model=schemas.Session)
def pause_session(session_id: int, pause_data: schemas.SessionPause, db: Session = Depends(get_db)):
    """Pause an active session"""
    session = crud.get_session(db=db, session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status != "active":
        raise HTTPException(status_code=400, detail="Session can only be paused if it's active")
    
    return crud.pause_session(db=db, session_id=session_id, reason=pause_data.reason)

@router.patch("/{session_id}/resume", response_model=schemas.Session)
def resume_session(session_id: int, db: Session = Depends(get_db)):
    """Resume a paused session"""
    session = crud.get_session(db=db, session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status != "paused":
        raise HTTPException(status_code=400, detail="Session can only be resumed if it's paused")
    
    return crud.resume_session(db=db, session_id=session_id)

@router.patch("/{session_id}/complete", response_model=schemas.Session)
def complete_session(session_id: int, db: Session = Depends(get_db)):
    """Complete a session (active or paused)"""
    session = crud.get_session(db=db, session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status not in ["active", "paused"]:
        raise HTTPException(status_code=400, detail="Session can only be completed if it's active or paused")
    
    return crud.complete_session(db=db, session_id=session_id)
