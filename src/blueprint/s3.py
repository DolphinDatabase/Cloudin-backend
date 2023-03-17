from flask import Flask, jsonify,send_file,Blueprint
#Boto3 é uma biblioteca Python que fornece uma interface de programação de aplicativos (API) para acessar serviços da AWS (Amazon Web Services)
import boto3
import os
import time
import mimetypes


s3bp = Blueprint('s3', __name__, url_prefix='/s3')


# Define as credenciais da AWS
aws_access_key_id = 'AKIA4VVR7RPQYTILT3MO'
aws_secret_access_key = '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'
aws_region_name = 'us-east-1'
s3_bucket_name = 'cloudin-bucket'

# Um cliente do S3 é criado com a função boto3.client(), que recebe como parâmetros 
# #o serviço que se deseja utilizar ('s3' no caso do S3), as chaves de acesso e a região da AWS

s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region_name
)


#Define caminho para download
FILE_PATH = "downloads/s3"
 


@s3bp.route('/upload/<file_name>')
def upload_file(file_name):
    try:
        if not os.path.exists(FILE_PATH):
            os.makedirs(FILE_PATH)
            
        # Define o caminho completo do arquivo local
        local_file_path = os.path.join(os.getcwd(), 'downloads', 's3', file_name)

        # Obtém o tamanho do arquivo e o tipo MIME
        file_size = os.path.getsize(local_file_path)
        content_type, encoding = mimetypes.guess_type(local_file_path)

        # Mede o tempo de upload do arquivo
        start_time = time.time()

        # Faz o upload do arquivo para o S3
        s3.upload_file(local_file_path, s3_bucket_name, file_name, ExtraArgs={'ContentType': content_type})

        # Calcula o tempo de upload
        upload_time = time.time() - start_time

        # Retorna o tamanho e tipo do arquivo, e o tempo de upload
        return jsonify({
            'file_size': file_size,
            'content_type': content_type,
            'upload_time': upload_time
        })
    except Exception as e:
        return str(e)