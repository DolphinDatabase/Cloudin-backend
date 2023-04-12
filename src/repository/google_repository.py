import requests
from .repository import Repository

class GoogleRepository(Repository):
    def list(self) -> list:
        url = "https://www.googleapis.com/drive/v3/files"
        headers = {
            "Authorization": f"Bearer {self.configuration.token}"
        }
        params = {
            "pageSize": 1000,
            "fields": "nextPageToken, files(id, name, size)"
        }

        files = []
        
        next_page_token = True
        while next_page_token:
            response = requests.get(url, headers=headers, params=params)
            json_response = response.json()
            files.extend(json_response["files"])
            next_page_token = json_response.get("nextPageToken", None)
            params["pageToken"] = next_page_token
        
        return files
    
    def download(self, file: str) -> None:
        return super().download(file)

    def upload(self, file: str) -> None:
        return super().upload(file)
