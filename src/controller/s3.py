from flask import jsonify, Blueprint, request, make_response
import boto3
import os
import time
import mimetypes


s3_blueprint = Blueprint("s3", __name__, url_prefix="/s3")

FILE_PATH = "downloads/s3"


def filesByFolderS3(token, folder):
    tk = token.split(" ")
    s3 = boto3.client(
        "s3", aws_access_key_id=tk[0], aws_secret_access_key=tk[1], region_name=tk[2]
    )

    files = s3.list_objects(Bucket=tk[3], Prefix=folder)
    num_of_files = len(files["Contents"]) - 1
    return num_of_files


@s3_blueprint.route("/list/folder", strict_slashes=False)
def list_folders():
    token = request.headers.get("token")
    tk = token.split(" ")

    s3 = boto3.client(
        "s3", aws_access_key_id=tk[0], aws_secret_access_key=tk[1], region_name=tk[2]
    )

    # Lista todos os objetos do bucket
    response = s3.list_objects(Bucket=tk[3], Delimiter="/")
    # Extrai as informações dos objetos e os retorna
    obj_list = []
    for i in response.get("CommonPrefixes"):
        obj_list.append({'id':i["Prefix"].replace("/", ""),'name':i["Prefix"].replace("/", "")})
    return make_response(jsonify({'result':obj_list}), 200)


@s3_blueprint.route("/list", strict_slashes=False)
def list():
    token = request.headers.get("token")
    tk = token.split(" ")

    s3 = boto3.client(
        "s3", aws_access_key_id=tk[0], aws_secret_access_key=tk[1], region_name=tk[2]
    )

    # Lista todos os objetos do bucket
    response = s3.list_objects(Bucket=tk[3])
    # Extrai as informações dos objetos e os retorna
    obj_list = []
    for obj in response["Contents"]:
        obj_dict = {}
        obj_dict["id"] = obj["Key"]
        obj_dict["name"] = obj["Key"]
        obj_dict["size"] = s3.head_object(Bucket=tk[3], Key=obj["Key"])["ContentLength"]
        obj_list.append(obj_dict)
    response_body = {"result": obj_list}
    return make_response(jsonify(response_body), 200)


@s3_blueprint.route("/download/<file_name>", strict_slashes=False)
def download_file(file_id, file_name, token):
    try:
        tk = token.split(" ")
        s3 = boto3.client(
            "s3",
            aws_access_key_id=tk[0],
            aws_secret_access_key=tk[1],
            region_name=tk[2],
        )
        if not os.path.exists(FILE_PATH):
            os.makedirs(FILE_PATH)
        local_folder_path = os.path.join(os.getcwd(), "downloads", "s3")
        local_file_name = file_name
        local_file_path = os.path.join(local_folder_path, local_file_name)
        start_time = time.time()
        s3.download_file(tk[3], file_name, local_file_path)
        file_size = os.path.getsize(local_file_path)
        download_time = time.time() - start_time
        response_body = {"time": download_time, "size": file_size}
        return make_response(jsonify(response_body), 200)
    except Exception as e:
        response_body = {"error": f"download error: {e}"}
        return make_response(jsonify(response_body), 400)


@s3_blueprint.route("/upload/<file_name>", strict_slashes=False)
def upload_file(file_name, token, origin):
    try:
        tk = token.split(" ")
        s3 = boto3.client(
            "s3",
            aws_access_key_id=tk[0],
            aws_secret_access_key=tk[1],
            region_name=tk[2],
        )
        if not os.path.exists(FILE_PATH):
            os.makedirs(FILE_PATH)
        local_file_path = os.path.join(os.getcwd(), "downloads", origin, file_name)
        content_type, encoding = mimetypes.guess_type(local_file_path)
        start_time = time.time()
        s3.upload_file(
            local_file_path, tk[3], file_name, ExtraArgs={"ContentType": content_type}
        )
        upload_time = time.time() - start_time
        os.remove(local_file_path)
        response_body = {"time": upload_time}
        return make_response(jsonify(response_body), 200)
    except Exception as e:
        response_body = {"error": f"upload error: {e}"}
        return make_response(jsonify(response_body), 400)
