import time
import requests
import os
import json

from io import BytesIO
from ..utils.mymeType import getMymetype


class GoogleService:
    token = ""

    def __init__(self, token):
        self.token = token

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
        try:
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
        except Exception as e:
            return {"error": f"download error: {e}"}

    def upload(self, fileName: str, path: str, folder: str):
        try:
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
        except Exception as e:
            return {"error": f"upload error: {e}"}
