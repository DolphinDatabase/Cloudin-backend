import json
import os

from flask import jsonify, session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import os
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

FILE_PATH = "OVERRIDE THIS TO YOUR FILE PATH"
ACCESS_TOKEN = "OVERRIDE THIS TO YOUR ACCESS TOKEN"
FILE_ID = "OVERRIDE THIS TO YOUR FILE ID"
FOLDER_ID = "OVERRIDE THIS TO YOUR FOLDER ID"
FILE_NAME = "OVERRIDE THIS TO YOUR FILE NAME"

SCOPES = ['https://www.googleapis.com/auth/drive']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'

CLIENT_SECRET_FILE = 'client_secret.json'
ACCESS_TOKEN_FILE = 'access_token.txt'

def authenticate():

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    session['token'] = creds.to_json()
    with open('access_token.txt', 'w') as f:
        f.write(creds.to_json())

    return 'Autenticação realizada com sucesso!'

def refresh_token():
    with open(ACCESS_TOKEN_FILE, 'r') as f:
        credentials_json = json.load(f)
        credentials = Credentials.from_authorized_user_info(info=credentials_json)
        if credentials.expired and credentials.refresh_token:
            request = Request()
            credentials.refresh(request)
    with open(ACCESS_TOKEN_FILE, 'w') as f:
        f.write(credentials.to_json())

    return jsonify({'success': True})


def read_access_token():
    try:
        with open(ACCESS_TOKEN_FILE, 'r') as f:
            token_info = json.load(f)
            access_token = token_info.get('access_token')
            if not access_token:
                raise ValueError('Token de acesso não encontrado no arquivo')
            return access_token
    except FileNotFoundError:
        raise FileNotFoundError('Arquivo de token não encontrado. Faça a autenticação antes de listar os arquivos.')


def list_files(access_token):
    if access_token == '':
        access_token = ACCESS_TOKEN
    try:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get('https://www.googleapis.com/drive/v3/files', headers=headers)

        return response.json()
    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f'Erro: {str(e)}'


def download_file(access_token, file_id):
    try:
        if access_token == '':
            access_token = ACCESS_TOKEN
        if file_id == '':
            file_id = FILE_ID
        file_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
        response = requests.get(file_url, headers={"Authorization": f"Bearer {access_token}"})
        if not os.path.exists(FILE_PATH):
            os.makedirs(FILE_PATH)

        output_file = os.path.join(FILE_PATH, "teste.pdf")
        with open(output_file, 'wb') as output:
            output.write(response.content)

        return jsonify({'metadados':f'File downloaded successfully to {output_file}'})
    except Exception as e:
            print(f"Erro ao fazer download do arquivo: {str(e)}")
            return "Erro ao fazer download do arquivo", 500


def upload_file_to_drive():
    creds = Credentials.from_authorized_user_file(ACCESS_TOKEN_FILE)
    service = build('drive', 'v3', credentials=creds)

    try:
        file_metadata = {'name': FILE_NAME, 'parents': [FOLDER_ID]}
        media = MediaFileUpload(FILE_NAME, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print("Arquivo enviado com sucesso! ID:", file.get("id"))
        media.stream().close() 
        os.remove(FILE_PATH)
        return jsonify("Arquivo enviado com sucesso! ID:", file.get("id"))
    
    except HttpError as error:
        print(F'Um erro ocorreu: {error}')
        return "Erro ao fazer download do arquivo", 500


def get_folder_path(service, folder_ids):
    """
    Returns the full path of each folder in the list folder_ids, starting from the root folder.
    """
    folder_paths = []

    for folder_id in folder_ids:
        folder_path = []
        folder = service.files().get(fileId=folder_id, fields='id, name, parents').execute()
        
        folder_path.append(folder['name'])
        
        while 'parents' in folder:
            parent_id = folder['parents'][0]
            parent = service.files().get(fileId=parent_id, fields='id, name, parents').execute()
            folder_path.append(parent['name'])
            folder = parent
        
        folder_path.reverse()
        
        folder_paths.append(folder_path)
    
    return folder_paths
