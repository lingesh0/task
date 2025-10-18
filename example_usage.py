#!/usr/bin/env python3
"""
Example usage of the Deep Work Session Tracker Python SDK
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'deepwork_sdk'))

from deepwork_sdk.api.sessions_api import SessionsApi
from deepwork_sdk import ApiClient, Configuration

def main():
    # Initialize the API client
    configuration = Configuration(host="http://localhost:8000")
    client = ApiClient(configuration)
    api = SessionsApi(client)
    
    print("Deep Work Session Tracker - SDK Example")
    print("=" * 40)
    
    try:
        # Create a new session
        print("Creating a new session...")
        from deepwork_sdk.models.session_create import SessionCreate
        
        session_data = SessionCreate(
            title="Write documentation",
            goal="Finish README and API documentation",
            scheduled_duration=45.0
        )
        
        session = api.create_session_api_v1_sessions_post(session_data)
        print(f"Created session: {session.title} (ID: {session.id})")
        
        # Start the session
        print("Starting session...")
        session = api.start_session_api_v1_sessions_session_id_start_patch(session.id)
        print(f"Session started at: {session.start_time}")
        
        # Get session history
        print("\nFetching session history...")
        history = api.get_session_history_api_v1_sessions_history_get()
        print(f"Total sessions: {history.total_sessions}")
        print(f"Completed sessions: {history.completed_sessions}")
        print(f"Total productive time: {history.total_productive_time:.1f} minutes")
        
        print("\nSDK example completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the backend server is running on http://localhost:8000")

if __name__ == "__main__":
    main()
