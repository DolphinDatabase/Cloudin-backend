import json
import mimetypes
import os
from io import BytesIO

import requests

from .repository import Repository


class GoogleDriveRepository(Repository):

    DOWNLOAD_FOLDER_PATH = "./downloads/google"

    def list(self) -> list:
        url = "https://www.googleapis.com/drive/v3/files"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"pageSize": 1000, "fields": "nextPageToken, files(id, name, size)"}

        files = []

        next_page_token = True
        while next_page_token:
            response = requests.get(url, headers=headers, params=params)
            json_response = response.json()
            files.extend(json_response["files"])
            next_page_token = json_response.get("nextPageToken", None)
            params["pageToken"] = next_page_token

        return files

    def download(self, file) -> str:
        file_url = f"https://www.googleapis.com/drive/v3/files/{file.id}?alt=media"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.get(
            file_url,
            headers=headers,
            stream=True
        )

        if not os.path.exists(self.DOWNLOAD_FOLDER_PATH):
            os.makedirs(self.DOWNLOAD_FOLDER_PATH)

        output_file = os.path.join(self.DOWNLOAD_FOLDER_PATH, file.name)

        with open(output_file, "wb") as output:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    output.write(chunk)

        return file.name

    def upload(self, file, origin: Repository) -> bool:
        file_mimetype = mimetypes.MimeTypes().guess_type(f"{origin.DOWNLOAD_FOLDER_PATH}/{file}", strict=True)
        file_size = os.stat(f"{origin.DOWNLOAD_FOLDER_PATH}/{file}").st_size

        url_upload = self.request_file_create(file, file_mimetype)

        with open(f"{origin.DOWNLOAD_FOLDER_PATH}/{file}", "rb") as file:
            content = BytesIO(file.read())

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Length": file_size
        }

        response = requests.put(
            url_upload,
            headers=headers,
            data=content
        )

        if response not in (200, 201):
            return False

        os.remove(f"{origin.DOWNLOAD_FOLDER_PATH}/{file}")
        return True

    def request_file_create(self, file_name, mimetype):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json; charset=UTF-8"
        }

        data = {
            "title": file_name,
            "mimeType": mimetype,
            "description": "Powered by Cloud-in",
        }

        response = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable",
            headers=headers,
            data=json.dumps(data)
        )

        if response.status_code == 200:
            return response.headers["Location"]

        return None
