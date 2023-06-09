from flask import Blueprint, jsonify, request, make_response
import requests
import time
import os
import mimetypes
import json
from io import BytesIO


drivebp = Blueprint("google", __name__, url_prefix="/google")

# @drivebp.route('/auth')
# def authenticate():
#     return google_drive.authenticate()


# @drivebp.route('/auth/refresh-token')
# def refresh_token():
#     return google_drive.refresh_token()


# @drivebp.route('/files')
# def list_files(access_token=''):
#     return google_drive.list_files(access_token)


def getMymetype(url):
    return mimetypes.MimeTypes().guess_type(url, strict=True)


def filesByFolderGoogle(token, folder):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": f"'{folder}' in parents", "fields": "*"}
    req = requests.get(
        "https://www.googleapis.com/drive/v3/files", headers=headers, params=params
    )
    num_of_files = len(req.json()["files"]) - 1
    return num_of_files


@drivebp.route("/list", strict_slashes=False)
def list_files():
    try:
        token = request.headers.get("token")
        url = "https://www.googleapis.com/drive/v3/files"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"pageSize": 1000, "fields": "nextPageToken, files(id, name, size)"}
        files = []
        next_page_token = True
        while next_page_token:
            response = requests.get(url, headers=headers, params=params)
            json_response = response.json()

            files.extend(json_response["files"])
            next_page_token = json_response.get("nextPageToken", None)
            params["pageToken"] = next_page_token
        return make_response(jsonify({"result": files}), 200)
    except Exception as e:
        return make_response(jsonify({"error": f"list files error: {e}"}), 500)


# Rota da listagem de pasta do google drive cld-73
@drivebp.route("/list/folder", strict_slashes=False)
def list_folders():
    try:
        token = request.headers.get("token")
        url = "https://www.googleapis.com/drive/v3/files"
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "q": "mimeType='application/vnd.google-apps.folder' and trashed=false",
            "fields": "nextPageToken, files(id, name)",
            "pageSize": 1000,
        }
        folders = []
        next_page_token = True
        while next_page_token:
            response = requests.get(url, headers=headers, params=params)
            json_response = response.json()
            folders.extend(json_response["files"])
            next_page_token = json_response.get("nextPageToken", None)
            params["pageToken"] = next_page_token
        return make_response(jsonify({"result": folders}), 200)
    except Exception as e:
        return make_response(jsonify({"error": f"list folder error:{e}"}, 500))


@drivebp.route("/download", strict_slashes=False)
def download_file(file_id, file_name, token):
    try:
        file_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
        start_time = time.time()
        response = requests.get(
            file_url, headers={"Authorization": f"Bearer {token}"}, stream=True
        )
        if not os.path.exists("./downloads/google"):
            os.makedirs("./downloads/google")

        output_file = os.path.join("./downloads/google", file_name)
        total_time = None
        with open(output_file, "wb") as output:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    output.write(chunk)
                    total_time = time.time() - start_time
        file_size = os.path.getsize(output_file)
        return make_response(
            jsonify({"title": file_name, "time": total_time, "size": file_size}), 200
        )
    except Exception as e:
        return make_response(jsonify({"error": f"download error: {e}"}), 500)


@drivebp.route("/upload", strict_slashes=False)
def upload_file(file_name, token, origin):
    try:
        url = "https://www.googleapis.com/drive/v2/files"
        data = {
            "title": file_name,
            "mimeType": getMymetype("./downloads/google/" + file_name)[0],
            "description": "Powered by Cloud-in",
        }
        output_file = os.path.join("./downloads/google", file_name)
        start_time = time.time()
        req = requests.post(
            url, headers={"Authorization": f"Bearer {token}"}, data=json.dumps(data)
        )
        file_id = req.json()["selfLink"].split("/")[-1]
        req_content = (
            "https://www.googleapis.com/upload/drive/v2/files/"
            + file_id
            + "?uploadType=media"
        )
        with open("./downloads/" + origin + "/" + file_name, "rb") as file:
            content = BytesIO(file.read())
        req = requests.put(
            req_content, headers={"Authorization": f"Bearer {token}"}, data=content
        )
        total_time = time.time() - start_time
        file_size = os.path.getsize(output_file)
        os.remove("./downloads/" + origin + "/" + file_name)
        return make_response(
            jsonify({"title": file_name, "time": total_time, "size": file_size}), 200
        )
    except Exception as e:
        return make_response(jsonify({"error": f"upload error: {e}"}), 500)
