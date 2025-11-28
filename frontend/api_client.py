import requests
import os

BASE_URL = "http://127.0.0.1:8000/api/v1"

class APIClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def create_session(self):
        try:
            response = requests.post(f"{self.base_url}/session/")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error creating session: {e}")
            return None

    def get_session(self, session_id):
        try:
            response = requests.get(f"{self.base_url}/session/{session_id}")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error getting session: {e}")
            return None

    def upload_document(self, session_id, file_obj, filename):
        try:
            files = {"file": (filename, file_obj, "application/pdf")}
            data = {"session_id": session_id}
            response = requests.post(f"{self.base_url}/documents/upload", files=files, data=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error uploading document: {e}")
            return None

    def chat(self, session_id, message):
        try:
            payload = {"session_id": session_id, "message": message}
            response = requests.post(f"{self.base_url}/chat/", json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error chatting: {e}")
            return None
