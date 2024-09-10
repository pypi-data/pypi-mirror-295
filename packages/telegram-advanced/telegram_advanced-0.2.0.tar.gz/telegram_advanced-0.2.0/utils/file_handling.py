# utils/file_handling.py
import os
import requests

class FileHandler:
    def __init__(self, client):
        self.client = client

    def download_file(self, file_id, destination):
        file_info = self.client._make_request("getFile", {"file_id": file_id})
        file_path = file_info['result']['file_path']
        file_url = f"https://api.telegram.org/file/bot{self.client.token}/{file_path}"
        
        response = requests.get(file_url)
        with open(destination, 'wb') as f:
            f.write(response.content)
        
        return destination

    def upload_file(self, file_path, file_type):
        with open(file_path, 'rb') as f:
            files = {file_type: f}
            return self.client._make_request(f"send{file_type.capitalize()}", files=files)

    def get_file_reference(self, file_id):
        file_info = self.client._make_request("getFile", {"file_id": file_id})
        return file_info['result']['file_unique_id']

    def refresh_file_reference(self, file_id, file_reference):
        # Implement logic to refresh file reference when it becomes invalid
        pass