#!/usr/bin/env python3
"""
Script to generate Python SDK from FastAPI OpenAPI specification
"""
import subprocess
import sys
import os
import time
import requests
from pathlib import Path

def check_backend_running():
    """Check if the backend server is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_backend():
    """Start the backend server in the background"""
    print("Starting backend server...")
    backend_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "backend.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])
    return backend_process

def wait_for_backend(max_wait=30):
    """Wait for backend to be ready"""
    print("Waiting for backend to start...")
    for i in range(max_wait):
        if check_backend_running():
            print("Backend is ready!")
            return True
        time.sleep(1)
        print(f"Waiting... ({i+1}/{max_wait})")
    return False

def generate_sdk():
    """Generate Python SDK using OpenAPI Generator"""
    print("Generating Python SDK...")
    
    # Check if openapi-generator is installed
    try:
        subprocess.run(["openapi-generator-cli", "version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Installing openapi-generator-cli...")
        subprocess.run([sys.executable, "-m", "pip", "install", "openapi-generator-cli"], check=True)
    
    # Generate SDK
    cmd = [
        "openapi-generator-cli", "generate",
        "-i", "http://localhost:8000/openapi.json",
        "-g", "python",
        "-o", "deepwork_sdk",
        "--additional-properties=packageName=deepwork_sdk,projectName=deepwork-sdk"
    ]
    
    subprocess.run(cmd, check=True)
    print("SDK generated successfully!")

def main():
    """Main function"""
    print("Deep Work Session Tracker - SDK Generator")
    print("=" * 50)
    
    # Check if backend is already running
    if not check_backend_running():
        backend_process = start_backend()
        try:
            if not wait_for_backend():
                print("Failed to start backend server")
                return 1
        except KeyboardInterrupt:
            print("\nStopping backend server...")
            backend_process.terminate()
            return 1
    else:
        print("Backend is already running")
        backend_process = None
    
    try:
        generate_sdk()
        
        # Create example usage script
        create_example_script()
        
        print("\nSDK generation complete!")
        print("SDK location: ./deepwork_sdk/")
        print("Example usage: python example_usage.py")
        
    except Exception as e:
        print(f"Error generating SDK: {e}")
        return 1
    finally:
        if backend_process:
            print("\nStopping backend server...")
            backend_process.terminate()
    
    return 0

def create_example_script():
    """Create example usage script"""
    example_script = '''#!/usr/bin/env python3
"""
Example usage of the Deep Work Session Tracker Python SDK
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'deepwork_sdk'))

from deepwork_sdk.api.sessions_api import SessionsApi
from deepwork_sdk import ApiClient

def main():
    # Initialize the API client
    client = ApiClient(host="http://localhost:8000")
    api = SessionsApi(client)
    
    print("Deep Work Session Tracker - SDK Example")
    print("=" * 40)
    
    try:
        # Create a new session
        print("Creating a new session...")
        session_data = {
            "title": "Write documentation",
            "goal": "Finish README and API documentation",
            "scheduled_duration": 45.0
        }
        
        session = api.create_session(session_data)
        print(f"Created session: {session.title} (ID: {session.id})")
        
        # Start the session
        print("Starting session...")
        session = api.start_session(session.id)
        print(f"Session started at: {session.start_time}")
        
        # Get session history
        print("\\nFetching session history...")
        history = api.get_session_history()
        print(f"Total sessions: {history.total_sessions}")
        print(f"Completed sessions: {history.completed_sessions}")
        print(f"Total productive time: {history.total_productive_time:.1f} minutes")
        
        print("\\nSDK example completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the backend server is running on http://localhost:8000")

if __name__ == "__main__":
    main()
'''
    
    with open("example_usage.py", "w") as f:
        f.write(example_script)
    
    print("Created example_usage.py")

if __name__ == "__main__":
    sys.exit(main())
