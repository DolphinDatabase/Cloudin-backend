import json
import os

from flask import jsonify, session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests


SCOPES = ['https://www.googleapis.com/auth/drive']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'

CLIENT_SECRET_FILE = 'src/utils/secrets/google_client_secret.json'
ACCESS_TOKEN_FILE = 'src/utils/secrets/access_token.txt'
FILE_PATH = "downloads\google"
ACCESS_TOKEN = "OVERRIDE THIS TO YOUR ACCESS TOKEN"
FILE_ID = "OVERRIDE THIS TO YOUR FILE ID"


def authenticate():
    creds = None
    if 'token' in session:
        creds = Credentials.from_authorized_user_info(session['token'])

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        session['token'] = creds.to_json()

        with open(ACCESS_TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())

    return jsonify({'success': True})


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


def get_folder_path(service, folder_ids):
    """
    Returns the full path of each folder in the list folder_ids, starting from the root folder.
    """
    folder_paths = []

    for folder_id in folder_ids:
        folder_path = []
        folder = service.files().get(fileId=folder_id, fields='id, name, parents').execute()
        
        # Add folder name to folder path
        folder_path.append(folder['name'])
        
        # Recursively find and add parent folder names to folder path
        while 'parents' in folder:
            parent_id = folder['parents'][0]
            parent = service.files().get(fileId=parent_id, fields='id, name, parents').execute()
            folder_path.append(parent['name'])
            folder = parent
        
        # Reverse the folder path list to start from the root folder
        folder_path.reverse()
        
        folder_paths.append(folder_path)
    
    return folder_paths
