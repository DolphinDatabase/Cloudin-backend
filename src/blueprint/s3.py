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

# Cria a rota para listar o conteúdo do bucket
@s3bp.route('/list')
def list():
    # Lista todos os objetos do bucket
    response = s3.list_objects(Bucket=s3_bucket_name)
    # Extrai os nomes dos objetos e os retorna
    obj_names = [obj['Key'] for obj in response['Contents']]
    return jsonify({'objects': obj_names})




@s3bp.route('/download/<file_name>')
def download_file(file_name):
    try:    
        if not os.path.exists(FILE_PATH):
            os.makedirs(FILE_PATH)

        local_folder_path = os.path.join(os.getcwd(), 'downloads', 's3')
        local_file_name = file_name
        # Define o caminho completo do arquivo local
        local_file_path = os.path.join(local_folder_path, local_file_name)

        # Mede o tempo de download do arquivo
        start_time = time.time()

        # Faz o download do arquivo do S3
        s3.download_file(s3_bucket_name, file_name, local_file_path)

         # Obtém o tamanho do arquivo e o tipo MIME
        file_size = os.path.getsize(local_file_path)
        
        # Calcula o tempo de download
        download_time = time.time() - start_time
        
        return jsonify({
            'time': download_time,
            'size': file_size
        })

    except Exception as e:
        return str(e)
