import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_create_session():
    response = requests.post(f"{BASE_URL}/session/")
    if response.status_code == 200:
        print("Session created successfully:")
        print(json.dumps(response.json(), indent=2))
        return response.json()["session_id"]
    else:
        print(f"Failed to create session: {response.text}")
        return None

def test_get_session(session_id):
    response = requests.get(f"{BASE_URL}/session/{session_id}")
    if response.status_code == 200:
        print("Session retrieved successfully:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failed to retrieve session: {response.text}")

if __name__ == "__main__":
    print("Testing Session API...")
    session_id = test_create_session()
    if session_id:
        test_get_session(session_id)
