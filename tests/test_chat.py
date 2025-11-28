import requests
import json
import os

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_chat(session_id):
    print(f"Testing chat for session {session_id}...")
    
    # 1. Ask a question
    question = "What is this document about?"
    print(f"User: {question}")
    
    response = requests.post(
        f"{BASE_URL}/chat/",
        json={"session_id": session_id, "message": question}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"AI: {data['response']}")
        print("Sources:")
        for source in data['sources']:
            print(f"- {source['source']}")
    else:
        print(f"Chat failed: {response.status_code} {response.text}")

if __name__ == "__main__":
    # We assume we have a session with a document uploaded from the previous test
    # If not, we should create one.
    # For simplicity, let's create a new session, upload, and then chat.
    
    print("Creating session...")
    session_res = requests.post(f"{BASE_URL}/session/")
    if session_res.status_code == 200:
        session_id = session_res.json()["session_id"]
        print(f"Session ID: {session_id}")
        
        # Upload
        file_path = "test_doc.pdf"
        if os.path.exists(file_path):
            print(f"Uploading {file_path}...")
            with open(file_path, "rb") as f:
                files = {"file": f}
                data = {"session_id": session_id}
                upload_res = requests.post(f"{BASE_URL}/documents/upload", files=files, data=data)
                if upload_res.status_code == 200:
                    print("Upload successful.")
                    test_chat(session_id)
                else:
                    print(f"Upload failed: {upload_res.text}")
        else:
            print("test_doc.pdf not found. Run create_pdf.py first.")
    else:
        print("Failed to create session")
