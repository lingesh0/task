#!/usr/bin/env python3
"""
Test business logic scenarios for Deep Work Session Tracker
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_endpoint(method, url, data=None, expected_status=200, description=""):
    """Test an API endpoint and return results"""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Method: {method} {url}")
    if data:
        print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PATCH":
            response = requests.patch(url, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == expected_status:
            print("PASS")
            return response.json()
        else:
            print(f"FAIL - Expected {expected_status}, got {response.status_code}")
            return None
            
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def main():
    print("Business Logic Testing - Deep Work Session Tracker")
    print("="*60)
    
    # Test 1: Interrupted Session (>3 pauses)
    print("\n1. Testing INTERRUPTED Session Logic")
    print("Creating session that will be paused 4 times...")
    
    session_data = {
        "title": "Interrupted Session Test",
        "goal": "Test interruption logic with 4+ pauses",
        "scheduled_duration": 30.0
    }
    
    session = test_endpoint("POST", f"{BASE_URL}/sessions/", session_data, 200, "Create session for interruption test")
    if not session:
        print("Cannot proceed without session creation")
        return
    
    session_id = session["id"]
    
    # Start the session
    test_endpoint("PATCH", f"{BASE_URL}/sessions/{session_id}/start", expected_status=200, description="Start session")
    
    # Pause 4 times (should make it interrupted when completed)
    for i in range(4):
        pause_data = {"reason": f"Interruption {i+1} - testing interruption logic"}
        test_endpoint("PATCH", f"{BASE_URL}/sessions/{session_id}/pause", pause_data, 200, description=f"Pause {i+1}")
        test_endpoint("PATCH", f"{BASE_URL}/sessions/{session_id}/resume", expected_status=200, description=f"Resume {i+1}")
    
    # Complete the session (should be "interrupted")
    completed_session = test_endpoint("PATCH", f"{BASE_URL}/sessions/{session_id}/complete", expected_status=200, description="Complete session (should be interrupted)")
    
    if completed_session and completed_session["status"] == "interrupted":
        print("INTERRUPTED logic working correctly!")
    else:
        print("INTERRUPTED logic failed!")
    
    # Test 2: Abandoned Session (paused but never resumed)
    print("\n2. Testing ABANDONED Session Logic")
    print("Creating session that will be paused but never resumed...")
    
    session_data = {
        "title": "Abandoned Session Test",
        "goal": "Test abandonment logic - pause but never resume",
        "scheduled_duration": 30.0
    }
    
    session = test_endpoint("POST", f"{BASE_URL}/sessions/", session_data, 200, "Create session for abandonment test")
    if not session:
        print("Cannot proceed without session creation")
        return
    
    session_id = session["id"]
    
    # Start the session
    test_endpoint("PATCH", f"{BASE_URL}/sessions/{session_id}/start", expected_status=200, description="Start session")
    
    # Pause the session
    pause_data = {"reason": "Got distracted and never came back"}
    test_endpoint("PATCH", f"{BASE_URL}/sessions/{session_id}/pause", pause_data, 200, "Pause session")
    
    # Complete without resuming (should be "abandoned")
    completed_session = test_endpoint("PATCH", f"{BASE_URL}/sessions/{session_id}/complete", expected_status=200, description="Complete session (should be abandoned)")
    
    if completed_session and completed_session["status"] == "abandoned":
        print("ABANDONED logic working correctly!")
    else:
        print("ABANDONED logic failed!")
    
    # Test 3: Overdue Session (>110% of scheduled duration)
    print("\n3. Testing OVERDUE Session Logic")
    print("Creating session with very short duration to test overdue logic...")
    
    session_data = {
        "title": "Overdue Session Test",
        "goal": "Test overdue logic with short duration",
        "scheduled_duration": 0.1  # 0.1 minutes = 6 seconds
    }
    
    session = test_endpoint("POST", f"{BASE_URL}/sessions/", session_data, 200, "Create session for overdue test")
    if not session:
        print("Cannot proceed without session creation")
        return
    
    session_id = session["id"]
    
    # Start the session
    test_endpoint("PATCH", f"{BASE_URL}/sessions/{session_id}/start", expected_status=200, description="Start session")
    
    # Wait a bit to exceed 110% of scheduled duration (6 seconds * 1.1 = 6.6 seconds)
    print("Waiting 2 seconds to exceed 110% of scheduled duration...")
    time.sleep(2)
    
    # Complete the session (should be "overdue")
    completed_session = test_endpoint("PATCH", f"{BASE_URL}/sessions/{session_id}/complete", expected_status=200, description="Complete session (should be overdue)")
    
    if completed_session and completed_session["status"] == "overdue":
        print("OVERDUE logic working correctly!")
    else:
        print("OVERDUE logic failed!")
    
    # Test 4: Normal Completed Session
    print("\n4. Testing COMPLETED Session Logic")
    print("Creating session that will complete normally...")
    
    session_data = {
        "title": "Normal Completed Session Test",
        "goal": "Test normal completion logic",
        "scheduled_duration": 30.0
    }
    
    session = test_endpoint("POST", f"{BASE_URL}/sessions/", session_data, 200, "Create session for normal completion test")
    if not session:
        print("Cannot proceed without session creation")
        return
    
    session_id = session["id"]
    
    # Start the session
    test_endpoint("PATCH", f"{BASE_URL}/sessions/{session_id}/start", expected_status=200, description="Start session")
    
    # Complete quickly (should be "completed")
    completed_session = test_endpoint("PATCH", f"{BASE_URL}/sessions/{session_id}/complete", expected_status=200, description="Complete session (should be completed)")
    
    if completed_session and completed_session["status"] == "completed":
        print("COMPLETED logic working correctly!")
    else:
        print("COMPLETED logic failed!")
    
    # Test 5: Verify all sessions in history
    print("\n5. Verifying All Sessions in History")
    history = test_endpoint("GET", f"{BASE_URL}/sessions/history", expected_status=200, description="Get session history")
    
    if history:
        print(f"Total sessions: {history['total_sessions']}")
        print(f"Completed sessions: {history['completed_sessions']}")
        print(f"Interrupted sessions: {history['interrupted_sessions']}")
        print(f"Overdue sessions: {history['overdue_sessions']}")
        print(f"Abandoned sessions: {history['abandoned_sessions']}")
        print(f"Total productive time: {history['total_productive_time']:.2f} minutes")
        print(f"Total interruptions: {history['total_interruptions']}")
        
        # Verify we have one of each status
        expected_counts = {
            "completed": 2,  # Normal completed + one from earlier tests
            "interrupted": 1,
            "overdue": 1,
            "abandoned": 1
        }
        
        actual_counts = {
            "completed": history['completed_sessions'],
            "interrupted": history['interrupted_sessions'],
            "overdue": history['overdue_sessions'],
            "abandoned": history['abandoned_sessions']
        }
        
        print("\nStatus verification:")
        all_correct = True
        for status, expected in expected_counts.items():
            actual = actual_counts[status]
            if actual >= expected:
                print(f"PASS {status.capitalize()}: {actual} (expected at least {expected})")
            else:
                print(f"FAIL {status.capitalize()}: {actual} (expected at least {expected})")
                all_correct = False
        
        if all_correct:
            print("\nAll business logic tests PASSED!")
        else:
            print("\nSome business logic tests FAILED!")
    
    print(f"\n{'='*60}")
    print("Business Logic Testing Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
