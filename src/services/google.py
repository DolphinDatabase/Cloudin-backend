import time
import requests
import os
import json

from io import BytesIO
from ..utils.mymeType import getMymetype


class GoogleService:
    token = ""

    def __init__(self, refreshToken:str):
        data = {
            "refresh_token":refreshToken,
            "client_id":"532089225272-1im33klerc0hmvspgo6mh08aobithavt.apps.googleusercontent.com",
            "client_secret":"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",
            "grant_type":"refresh_token"
        }
        req = requests.post("https://oauth2.googleapis.com/token",json=data).json()
        self.token = req['access_token']
    
    def files_by_folder(self, folder):
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"q": f"'{folder}' in parents", "fields": "*"}
        req = requests.get(
            "https://www.googleapis.com/drive/v3/files", headers=headers, params=params
        )
        num_of_files = len(req.json()["files"]) - 1
        return num_of_files

    def list_files_by_folder(self, folder: str):
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            params = {
                "q": f"'{folder}' in parents",
                "pageSize": 1000,
                "fields": "nextPageToken, files(id, name)",
            }
            url = "https://www.googleapis.com/drive/v3/files"
            files = []
            next_page_token = True
            while next_page_token:
                response = requests.get(url, headers=headers, params=params)
                json_response = response.json()
                files.extend(json_response["files"])
                next_page_token = json_response.get("nextPageToken", None)
                params["pageToken"] = next_page_token
            return files
        except Exception as e:
            return {"error": f"list files error: {e}"}

    def download(self, fileID: str, fileName: str):
        file_url = f"https://www.googleapis.com/drive/v3/files/{fileID}?alt=media"
        start_time = time.time()
        response = requests.get(
            file_url, headers={"Authorization": f"Bearer {self.token}"}, stream=True
        )
        if not os.path.exists("./downloads/google"):
            os.makedirs("./downloads/google")

        output_file = os.path.join("./downloads/google", fileName)
        total_time = None
        with open(output_file, "wb") as output:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    output.write(chunk)
                    total_time = time.time() - start_time
        file_size = os.path.getsize(output_file)
        return {"title": fileName, "time": total_time, "size": file_size}

    def upload(self, fileName: str, path: str, folder: str):
        url = "https://www.googleapis.com/drive/v2/files"
        data = {
            "title": fileName,
            "parents": [{"id": folder}],
            "mimeType": getMymetype("./downloads/" + path + "/" + fileName)[0],
            "description": "Powered by Cloud-in",
        }
        start_time = time.time()
        req = requests.post(
            url,
            headers={"Authorization": f"Bearer {self.token}"},
            data=json.dumps(data),
        )
        file_id = req.json()["selfLink"].split("/")[-1]
        req_content = (
            "https://www.googleapis.com/upload/drive/v2/files/"
            + file_id
            + "?uploadType=media"
        )
        with open("./downloads/" + path + "/" + fileName, "rb") as file:
            content = BytesIO(file.read())
        req = requests.put(
            req_content,
            headers={"Authorization": f"Bearer {self.token}"},
            data=content,
        )
        total_time = time.time() - start_time
        os.remove("./downloads/" + path + "/" + fileName)
        return {"title": fileName, "time": total_time}

    def remove_file(self, fileID: str, fileName: str,path: str):
        url = f"https://www.googleapis.com/drive/v3/files/{fileID}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return {"message": "File successfully deleted."}
        else:
            raise Exception("Error deleting file Google")
        