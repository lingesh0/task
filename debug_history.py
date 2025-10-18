#!/usr/bin/env python3
"""
Debug the history endpoint issue
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import SessionLocal
from backend import crud, models

def debug_history():
    db = SessionLocal()
    try:
        print("Testing database connection...")
        
        # Test basic query
        print("Querying sessions...")
        sessions = db.query(models.Session).all()
        print(f"Found {len(sessions)} sessions")
        
        for session in sessions:
            print(f"Session {session.id}: {session.title} - {session.status}")
            print(f"  Interruptions: {len(session.interruptions)}")
        
        # Test the history function
        print("\nTesting get_session_history...")
        history = crud.get_session_history(db)
        print(f"History created successfully!")
        print(f"Total sessions: {history.total_sessions}")
        print(f"Completed sessions: {history.completed_sessions}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_history()
