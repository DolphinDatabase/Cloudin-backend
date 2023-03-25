from flask import Flask, jsonify,send_file,Blueprint, request
import boto3
import os
import time
import mimetypes


s3bp = Blueprint('s3', __name__, url_prefix='/s3')


# Define as credenciais da AWS
# aws_access_key_id = 'AKIA4VVR7RPQYTILT3MO'
# aws_secret_access_key = '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'
# aws_region_name = 'us-east-1'
# s3_bucket_name = 'cloudin-bucket'


#Define caminho para download
FILE_PATH = "downloads/s3"



@s3bp.route('/list')
def list():
    token = request.headers.get('token')
    tk = token.split(" ")

    s3 = boto3.client(
        's3',
        aws_access_key_id=tk[0],
        aws_secret_access_key=tk[1],
        region_name=tk[2]
    )

    # Lista todos os objetos do bucket
    response = s3.list_objects(Bucket=tk[3])
    # Extrai as informações dos objetos e os retorna
    obj_list = []
    for obj in response['Contents']:
        obj_dict = {}
        obj_dict['id'] = obj['Key']
        obj_dict['name'] = obj['Key']
        obj_dict['size'] = s3.head_object(Bucket=tk[3], Key=obj['Key'])['ContentLength']
        obj_list.append(obj_dict)
    return jsonify({'result': obj_list})



@s3bp.route('/download/<file_name>')
def download_file(file_id,file_name,token):
    tk = token.split(" ")
    s3 = boto3.client(
        's3',
        aws_access_key_id=tk[0],
        aws_secret_access_key=tk[1],
        region_name=tk[2]
    )
    try:    
        if not os.path.exists(FILE_PATH):
            os.makedirs(FILE_PATH)
        local_folder_path = os.path.join(os.getcwd(), 'downloads', 's3')
        local_file_name = file_name
        local_file_path = os.path.join(local_folder_path, local_file_name)
        start_time = time.time()
        s3.download_file(tk[3], file_name, local_file_path)
        file_size = os.path.getsize(local_file_path)
        download_time = time.time() - start_time
        return {'time': download_time,'size': file_size}
    except Exception as e:
        return {'error':f'download error: {e}'}



@s3bp.route('/upload/<file_name>')
def upload_file(file_name,token,origin):
    tk = token.split(" ")
    s3 = boto3.client(
        's3',
        aws_access_key_id=tk[0],
        aws_secret_access_key=tk[1],
        region_name=tk[2]
    )
    try:
        if not os.path.exists(FILE_PATH):
            os.makedirs(FILE_PATH)
        local_file_path = os.path.join(os.getcwd(), 'downloads', origin, file_name)
        content_type, encoding = mimetypes.guess_type(local_file_path)
        start_time = time.time()
        s3.upload_file(local_file_path, tk[3], file_name, ExtraArgs={'ContentType': content_type})
        upload_time = time.time() - start_time
        os.remove(local_file_path)
        return {'time': upload_time}
    except Exception as e:
        return {'error':f'upload error: {e}'}
