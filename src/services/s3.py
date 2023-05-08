import boto3
import os
import time

from ..utils.mymeType import getMymetype
from ..exception.exceptions import StorageAuthorizationException, StorageErrorException


class s3Service:
    token = ""

    def __init__(self, token):
        self.token = token

    def files_by_folder(self, folder):
        tk = self.token.split(" ")
        s3 = boto3.client(
            "s3",
            aws_access_key_id=tk[0],
            aws_secret_access_key=tk[1],
            region_name=tk[2],
        )

        files = s3.list_objects(Bucket=tk[3], Prefix=folder)
        num_of_files = len(files["Contents"]) - 1
        return num_of_files

    def list_files_by_folder(self, folder: str):
        try:
            tk = self.token.split(" ")
            s3 = boto3.client(
                "s3",
                aws_access_key_id=tk[0],
                aws_secret_access_key=tk[1],
                region_name=tk[2],
            )
            files = s3.list_objects(Bucket=tk[3], Prefix=folder + "/")
            obj_list = []
            for obj in files["Contents"]:
                if obj["Key"][-1] != "/":
                    obj_dict = {}
                    obj_dict["id"] = obj["Key"]
                    obj_dict["name"] = obj["Key"].split("/")[1]
                    obj_list.append(obj_dict)
            return obj_list
        except Exception as e:
            return {"error": f"list files error: {e}"}

    def download(self, fileID: str, fileName: str):
        try:
            tk = self.token.split(" ")
            s3 = boto3.client(
                "s3",
                aws_access_key_id=tk[0],
                aws_secret_access_key=tk[1],
                region_name=tk[2],
            )
            if not os.path.exists("./downloads/s3"):
                os.makedirs("./downloads/s3")
            local_folder_path = os.path.join(os.getcwd(), "downloads", "s3")
            local_file_path = os.path.join(local_folder_path, fileName)
            start_time = time.time()
            s3.download_file(tk[3], fileID, local_file_path)
            file_size = os.path.getsize(local_file_path)
            download_time = time.time() - start_time
            return {"title": fileName, "time": download_time, "size": file_size}
        except Exception:
            raise StorageErrorException("S3 download error")

    def upload(self, fileName: str, path: str, folder: str):
        try:
            tk = self.token.split(" ")
            s3 = boto3.client(
                "s3",
                aws_access_key_id=tk[0],
                aws_secret_access_key=tk[1],
                region_name=tk[2],
            )
            local_file_path = os.path.join(os.getcwd(), "downloads", path, fileName)
            content_type = getMymetype(local_file_path)[0]
            start_time = time.time()
            s3.upload_file(
                local_file_path,
                tk[3],
                folder + "/" + fileName,
                ExtraArgs={"ContentType": content_type},
            )
            upload_time = time.time() - start_time
            os.remove(local_file_path)
            return {"title": fileName, "time": upload_time}
        except Exception:
            raise StorageErrorException("S3 upload error")

    def remove_file(self, fileID: str, fileName: str, path: str):
        tk = self.token.split(" ")
        s3 = boto3.client(
            "s3",
            aws_access_key_id=tk[0],
            aws_secret_access_key=tk[1],
            region_name=tk[2],
        )
        try:
            s3.delete_object(Bucket=tk[3], Key=fileID)
            return {"message": "File successfully deleted."}
        except Exception:
            raise StorageErrorException("S3 delete error")

    def get_folder_name(self, folder_id: str) -> str:
        return folder_id
