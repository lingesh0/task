#!/usr/bin/env python3
"""
Clean up the database by removing invalid sessions
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import SessionLocal
from backend import models

def cleanup_database():
    db = SessionLocal()
    try:
        print("Cleaning up database...")
        
        # Find sessions with empty titles
        invalid_sessions = db.query(models.Session).filter(models.Session.title == "").all()
        print(f"Found {len(invalid_sessions)} sessions with empty titles")
        
        for session in invalid_sessions:
            print(f"Deleting session {session.id}: '{session.title}'")
            db.delete(session)
        
        db.commit()
        print("Database cleanup complete!")
        
        # Verify cleanup
        remaining_sessions = db.query(models.Session).all()
        print(f"Remaining sessions: {len(remaining_sessions)}")
        
        for session in remaining_sessions:
            print(f"Session {session.id}: '{session.title}' - {session.status}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_database()
