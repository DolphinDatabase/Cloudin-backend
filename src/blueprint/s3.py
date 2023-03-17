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



# Cria a rota para listar o conteúdo do bucket
@s3bp.route('/list')
def list():
    # Lista todos os objetos do bucket
    response = s3.list_objects(Bucket=s3_bucket_name)
    # Extrai os nomes dos objetos e os retorna
    obj_names = [obj['Key'] for obj in response['Contents']]
    return jsonify({'objects': obj_names})

