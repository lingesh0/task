#!/usr/bin/env python3
"""
Test the history endpoint specifically
"""
import requests
import json

def test_history():
    try:
        response = requests.get("http://localhost:8000/api/v1/sessions/history")
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"JSON Response: {json.dumps(data, indent=2)}")
        else:
            print("Error response received")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_history()
