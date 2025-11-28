import requests
import json
import os

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_debug():
    print("Testing debug endpoint...")
    response = requests.get(f"{BASE_URL}/documents/debug")
    if response.status_code == 200:
        print("Debug endpoint working:", response.json())
    else:
        print(f"Debug endpoint failed: {response.status_code} {response.text}")

def test_upload(session_id):
    file_path = "test_doc.pdf"
    if not os.path.exists(file_path):
        print("Please run create_pdf.py first")
        return

    print(f"Uploading {file_path} to session {session_id}...")
    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {"session_id": session_id}
        response = requests.post(f"{BASE_URL}/documents/upload", files=files, data=data)
        
    if response.status_code == 200:
        print("Upload successful:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Upload failed: {response.status_code} {response.text}")

if __name__ == "__main__":
    test_debug()
    
    print("Creating session...")
    session_res = requests.post(f"{BASE_URL}/session/")
    if session_res.status_code == 200:
        session_id = session_res.json()["session_id"]
        print(f"Session ID: {session_id}")
        test_upload(session_id)
    else:
        print("Failed to create session")
