#!/usr/bin/env python3
"""
Test error handling and validation for Deep Work Session Tracker
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_error_scenario(method, url, data=None, expected_status=400, description=""):
    """Test an error scenario and return results"""
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
            return True
        else:
            print(f"FAIL - Expected {expected_status}, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    print("Error Handling and Validation Testing - Deep Work Session Tracker")
    print("="*60)
    
    # Test 1: Invalid session ID (404)
    print("\n1. Testing Invalid Session ID")
    test_error_scenario("GET", f"{BASE_URL}/sessions/99999", expected_status=404, description="Get non-existent session")
    
    # Test 2: Invalid data validation (422)
    print("\n2. Testing Data Validation")
    
    # Empty title
    invalid_data = {
        "title": "",
        "goal": "Test goal",
        "scheduled_duration": 30.0
    }
    test_error_scenario("POST", f"{BASE_URL}/sessions/", invalid_data, 422, description="Create session with empty title")
    
    # Empty goal
    invalid_data = {
        "title": "Test title",
        "goal": "",
        "scheduled_duration": 30.0
    }
    test_error_scenario("POST", f"{BASE_URL}/sessions/", invalid_data, 422, description="Create session with empty goal")
    
    # Negative duration
    invalid_data = {
        "title": "Test title",
        "goal": "Test goal",
        "scheduled_duration": -10.0
    }
    test_error_scenario("POST", f"{BASE_URL}/sessions/", invalid_data, 422, description="Create session with negative duration")
    
    # Zero duration
    invalid_data = {
        "title": "Test title",
        "goal": "Test goal",
        "scheduled_duration": 0.0
    }
    test_error_scenario("POST", f"{BASE_URL}/sessions/", invalid_data, 422, description="Create session with zero duration")
    
    # Missing required fields
    invalid_data = {
        "title": "Test title"
        # Missing goal and scheduled_duration
    }
    test_error_scenario("POST", f"{BASE_URL}/sessions/", invalid_data, 422, description="Create session with missing required fields")
    
    # Test 3: Invalid state transitions
    print("\n3. Testing Invalid State Transitions")
    
    # Create a session
    session_data = {
        "title": "Error Test Session",
        "goal": "Test error handling",
        "scheduled_duration": 30.0
    }
    response = requests.post(f"{BASE_URL}/sessions/", json=session_data)
    if response.status_code != 200:
        print("Failed to create test session")
        return
    
    session_id = response.json()["id"]
    print(f"Created test session with ID: {session_id}")
    
    # Try to start already started session
    requests.patch(f"{BASE_URL}/sessions/{session_id}/start")  # Start it first
    test_error_scenario("PATCH", f"{BASE_URL}/sessions/{session_id}/start", expected_status=400, description="Start already started session")
    
    # Try to pause non-active session
    test_error_scenario("PATCH", f"{BASE_URL}/sessions/{session_id}/pause", {"reason": "Test"}, expected_status=400, description="Pause non-active session")
    
    # Try to resume non-paused session
    test_error_scenario("PATCH", f"{BASE_URL}/sessions/{session_id}/resume", expected_status=400, description="Resume non-paused session")
    
    # Test 4: Invalid pause data
    print("\n4. Testing Invalid Pause Data")
    
    # Create new session for pause testing
    session_data = {
        "title": "Pause Test Session",
        "goal": "Test pause validation",
        "scheduled_duration": 30.0
    }
    response = requests.post(f"{BASE_URL}/sessions/", json=session_data)
    session_id = response.json()["id"]
    requests.patch(f"{BASE_URL}/sessions/{session_id}/start")  # Start it
    
    # Pause without reason
    test_error_scenario("PATCH", f"{BASE_URL}/sessions/{session_id}/pause", {}, expected_status=422, description="Pause without reason")
    
    # Pause with empty reason
    test_error_scenario("PATCH", f"{BASE_URL}/sessions/{session_id}/pause", {"reason": ""}, expected_status=422, description="Pause with empty reason")
    
    # Test 5: Invalid session operations on completed session
    print("\n5. Testing Operations on Completed Session")
    
    # Complete the session
    requests.patch(f"{BASE_URL}/sessions/{session_id}/complete")
    
    # Try to start completed session
    test_error_scenario("PATCH", f"{BASE_URL}/sessions/{session_id}/start", expected_status=400, description="Start completed session")
    
    # Try to pause completed session
    test_error_scenario("PATCH", f"{BASE_URL}/sessions/{session_id}/pause", {"reason": "Test"}, expected_status=400, description="Pause completed session")
    
    # Try to resume completed session
    test_error_scenario("PATCH", f"{BASE_URL}/sessions/{session_id}/resume", expected_status=400, description="Resume completed session")
    
    # Test 6: Invalid JSON data
    print("\n6. Testing Invalid JSON Data")
    
    # This would require sending raw data, but requests handles JSON automatically
    # So we'll test with malformed data that requests can still send
    invalid_data = {
        "title": "Test",
        "goal": "Test",
        "scheduled_duration": "not_a_number"  # Invalid type
    }
    test_error_scenario("POST", f"{BASE_URL}/sessions/", invalid_data, 422, description="Create session with invalid data types")
    
    # Test 7: Test with very long strings
    print("\n7. Testing Input Length Limits")
    
    # Very long title (should still work, but test boundary)
    long_title = "A" * 1000
    long_goal = "B" * 1000
    
    long_data = {
        "title": long_title,
        "goal": long_goal,
        "scheduled_duration": 30.0
    }
    
    response = requests.post(f"{BASE_URL}/sessions/", json=long_data)
    if response.status_code == 200:
        print("PASS - Long strings accepted")
        # Clean up
        session_id = response.json()["id"]
        requests.delete(f"{BASE_URL}/sessions/{session_id}")  # This will fail, but that's expected
    else:
        print(f"FAIL - Long strings rejected: {response.status_code}")
    
    # Test 8: Test edge cases
    print("\n8. Testing Edge Cases")
    
    # Very small duration
    edge_data = {
        "title": "Edge Test",
        "goal": "Test edge cases",
        "scheduled_duration": 0.01  # Very small duration
    }
    response = requests.post(f"{BASE_URL}/sessions/", json=edge_data)
    if response.status_code == 200:
        print("PASS - Very small duration accepted")
    else:
        print(f"FAIL - Very small duration rejected: {response.status_code}")
    
    # Very large duration
    edge_data = {
        "title": "Edge Test 2",
        "goal": "Test large duration",
        "scheduled_duration": 999999.0  # Very large duration
    }
    response = requests.post(f"{BASE_URL}/sessions/", json=edge_data)
    if response.status_code == 200:
        print("PASS - Very large duration accepted")
    else:
        print(f"FAIL - Very large duration rejected: {response.status_code}")
    
    print(f"\n{'='*60}")
    print("Error Handling and Validation Testing Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
