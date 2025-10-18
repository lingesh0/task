#!/usr/bin/env python3
"""
Test database operations and data persistence
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import SessionLocal
from backend import crud, models
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_database_operations():
    print("Database Operations Testing - Deep Work Session Tracker")
    print("="*60)
    
    # Test 1: Create session via API and verify in database
    print("\n1. Testing Session Creation and Database Persistence")
    
    session_data = {
        "title": "Database Test Session",
        "goal": "Test database persistence and relationships",
        "scheduled_duration": 25.0
    }
    
    # Create via API
    response = requests.post(f"{BASE_URL}/sessions/", json=session_data)
    if response.status_code != 200:
        print(f"Failed to create session via API: {response.status_code}")
        return
    
    api_session = response.json()
    session_id = api_session["id"]
    print(f"Created session via API with ID: {session_id}")
    
    # Verify in database
    db = SessionLocal()
    try:
        db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
        if db_session:
            print(f"Session found in database: {db_session.title}")
            print(f"Status: {db_session.status}")
            print(f"Scheduled duration: {db_session.scheduled_duration}")
            print("PASS - Session persisted to database")
        else:
            print("FAIL - Session not found in database")
            return
    finally:
        db.close()
    
    # Test 2: Start session and verify start_time is set
    print("\n2. Testing Session Start and Database Update")
    
    response = requests.patch(f"{BASE_URL}/sessions/{session_id}/start")
    if response.status_code != 200:
        print(f"Failed to start session: {response.status_code}")
        return
    
    # Verify start_time in database
    db = SessionLocal()
    try:
        db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
        if db_session and db_session.start_time:
            print(f"Session started at: {db_session.start_time}")
            print("PASS - Start time recorded in database")
        else:
            print("FAIL - Start time not recorded")
    finally:
        db.close()
    
    # Test 3: Pause session and verify interruption record
    print("\n3. Testing Interruption Creation and Database Persistence")
    
    pause_data = {"reason": "Database test interruption"}
    response = requests.patch(f"{BASE_URL}/sessions/{session_id}/pause", json=pause_data)
    if response.status_code != 200:
        print(f"Failed to pause session: {response.status_code}")
        return
    
    # Verify interruption record in database
    db = SessionLocal()
    try:
        from sqlalchemy.orm import joinedload
        db_session = db.query(models.Session).options(joinedload(models.Session.interruptions)).filter(models.Session.id == session_id).first()
        if db_session and db_session.interruptions:
            interruption = db_session.interruptions[0]
            print(f"Interruption recorded: {interruption.reason}")
            print(f"Pause time: {interruption.pause_time}")
            print("PASS - Interruption persisted to database")
        else:
            print("FAIL - Interruption not recorded in database")
    finally:
        db.close()
    
    # Test 4: Complete session and verify end_time and status
    print("\n4. Testing Session Completion and Final Status")
    
    response = requests.patch(f"{BASE_URL}/sessions/{session_id}/complete")
    if response.status_code != 200:
        print(f"Failed to complete session: {response.status_code}")
        return
    
    # Verify completion in database
    db = SessionLocal()
    try:
        db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
        if db_session and db_session.end_time and db_session.status == "completed":
            print(f"Session completed at: {db_session.end_time}")
            print(f"Final status: {db_session.status}")
            print("PASS - Completion recorded in database")
        else:
            print("FAIL - Completion not recorded properly")
    finally:
        db.close()
    
    # Test 5: Verify session history includes all data
    print("\n5. Testing Session History Data Integrity")
    
    response = requests.get(f"{BASE_URL}/sessions/history")
    if response.status_code != 200:
        print(f"Failed to get session history: {response.status_code}")
        return
    
    history = response.json()
    our_session = None
    for session in history["sessions"]:
        if session["id"] == session_id:
            our_session = session
            break
    
    if our_session:
        print(f"Session found in history: {our_session['title']}")
        print(f"Status: {our_session['status']}")
        print(f"Interruptions: {len(our_session['interruptions'])}")
        print(f"Start time: {our_session['start_time']}")
        print(f"End time: {our_session['end_time']}")
        print("PASS - Session data integrity maintained")
    else:
        print("FAIL - Session not found in history")
    
    # Test 6: Verify database relationships
    print("\n6. Testing Database Relationships")
    
    db = SessionLocal()
    try:
        # Test session-interruption relationship
        from sqlalchemy.orm import joinedload
        session_with_interruptions = db.query(models.Session).options(joinedload(models.Session.interruptions)).filter(models.Session.id == session_id).first()
        if session_with_interruptions and session_with_interruptions.interruptions:
            interruption = session_with_interruptions.interruptions[0]
            print(f"Session has {len(session_with_interruptions.interruptions)} interruption(s)")
            print(f"Interruption belongs to session {interruption.session_id}")
            print(f"Interruption reason: {interruption.reason}")
            print("PASS - Database relationships working correctly")
        else:
            print("FAIL - Database relationships not working")
    finally:
        db.close()
    
    # Test 7: Verify data consistency across operations
    print("\n7. Testing Data Consistency")
    
    # Get session via API
    response = requests.get(f"{BASE_URL}/sessions/{session_id}")
    if response.status_code != 200:
        print(f"Failed to get session: {response.status_code}")
        return
    
    api_session = response.json()
    
    # Get same session from database
    db = SessionLocal()
    try:
        from sqlalchemy.orm import joinedload
        db_session = db.query(models.Session).options(joinedload(models.Session.interruptions)).filter(models.Session.id == session_id).first()
        if db_session:
            # Compare key fields
            api_title = api_session["title"]
            db_title = db_session.title
            api_status = api_session["status"]
            db_status = db_session.status
            api_interruptions = len(api_session["interruptions"])
            db_interruptions = len(db_session.interruptions)
            
            print(f"API Title: {api_title}, DB Title: {db_title}")
            print(f"API Status: {api_status}, DB Status: {db_status}")
            print(f"API Interruptions: {api_interruptions}, DB Interruptions: {db_interruptions}")
            
            if (api_title == db_title and api_status == db_status and 
                api_interruptions == db_interruptions):
                print("PASS - Data consistency maintained between API and database")
            else:
                print("FAIL - Data inconsistency detected")
        else:
            print("FAIL - Session not found in database")
    finally:
        db.close()
    
    print(f"\n{'='*60}")
    print("Database Operations Testing Complete!")
    print("="*60)

if __name__ == "__main__":
    test_database_operations()
