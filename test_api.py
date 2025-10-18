#!/usr/bin/env python3
"""
Comprehensive API testing script for Deep Work Session Tracker
"""
import requests
import json
import time
from datetime import datetime

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
    print("Deep Work Session Tracker API Testing")
    print("="*60)
    
    # Test 1: Create a session
    print("\n1. Testing Session Creation")
    session_data = {
        "title": "Test Deep Work Session",
        "goal": "Complete API testing and validation",
        "scheduled_duration": 30.0
    }
    
    session = test_endpoint("POST", f"{BASE_URL}/sessions/", session_data, 200, "Create new session")
    if not session:
        print("Cannot proceed without session creation")
        return
    
    session_id = session["id"]
    print(f"Created session with ID: {session_id}")
    
    # Test 2: Get the session
    print("\n2. Testing Session Retrieval")
    test_endpoint("GET", f"{BASE_URL}/sessions/{session_id}", expected_status=200, description="Get session by ID")
    
    # Test 3: Start the session
    print("\n3. Testing Session Start")
    started_session = test_endpoint("PATCH", f"{BASE_URL}/sessions/{session_id}/start", expected_status=200, description="Start session")
    
    # Test 4: Pause the session
    print("\n4. Testing Session Pause")
    pause_data = {"reason": "Phone call interruption"}
    test_endpoint("PATCH", f"{BASE_URL}/sessions/{session_id}/pause", pause_data, 200, "Pause session with reason")
    
    # Test 5: Resume the session
    print("\n5. Testing Session Resume")
    test_endpoint("PATCH", f"{BASE_URL}/sessions/{session_id}/resume", expected_status=200, description="Resume session")
    
    # Test 6: Complete the session
    print("\n6. Testing Session Completion")
    completed_session = test_endpoint("PATCH", f"{BASE_URL}/sessions/{session_id}/complete", expected_status=200, description="Complete session")
    
    # Test 7: Get session history
    print("\n7. Testing Session History")
    history = test_endpoint("GET", f"{BASE_URL}/sessions/history", expected_status=200, description="Get session history with statistics")
    
    # Test 8: Test error handling - invalid session ID
    print("\n8. Testing Error Handling")
    test_endpoint("GET", f"{BASE_URL}/sessions/99999", expected_status=404, description="Get non-existent session (should return 404)")
    
    # Test 9: Test invalid data validation
    print("\n9. Testing Data Validation")
    invalid_data = {
        "title": "",  # Empty title should fail
        "goal": "Test goal",
        "scheduled_duration": 30.0
    }
    test_endpoint("POST", f"{BASE_URL}/sessions/", invalid_data, 422, description="Create session with invalid data (should return 422)")
    
    print(f"\n{'='*60}")
    print("API Testing Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
