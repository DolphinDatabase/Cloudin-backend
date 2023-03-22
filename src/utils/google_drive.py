# import json
# import os
# import requests
# import time
# import psutil

# from flask import jsonify, session
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from googleapiclient.errors import HttpError
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload


# FILE_PATH_DOWNLOAD = "downloads\google"
# FILE_PATH_UPLOAD = "downloads\\google\\remake_big_data.png"

# ACCESS_TOKEN = "OVERRIDE THIS TO YOUR ACCESS TOKEN"
# FILE_ID = "OVERRIDE THIS TO YOUR FILE ID"
# FOLDER_ID = "OVERRIDE THIS TO YOUR FOLDER ID"

# FILE_NAME_DOWNLOAD = "test.pdf"
# FILE_NAME_UPLOAD = "remake_big_data.png"

# SCOPES = ['https://www.googleapis.com/auth/drive']
# API_SERVICE_NAME = 'drive'
# API_VERSION = 'v3'

# CLIENT_SECRET_FILE = 'client_secret.json'
# ACCESS_TOKEN_FILE = 'access_token.txt'

# def authenticate():

#     flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
#     creds = flow.run_local_server(port=0)
#     session['token'] = creds.to_json()
#     with open('access_token.txt', 'w') as f:
#         f.write(creds.to_json())

#     return 'Autenticação realizada com sucesso!'

# def refresh_token():
#     with open(ACCESS_TOKEN_FILE, 'r') as f:
#         credentials_json = json.load(f)
#         credentials = Credentials.from_authorized_user_info(info=credentials_json)
#         if credentials.expired and credentials.refresh_token:
#             request = Request()
#             credentials.refresh(request)
#     with open(ACCESS_TOKEN_FILE, 'w') as f:
#         f.write(credentials.to_json())

#     return jsonify({'success': True})


# def read_access_token():
#     try:
#         with open(ACCESS_TOKEN_FILE, 'r') as f:
#             token_info = json.load(f)
#             access_token = token_info.get('access_token')
#             if not access_token:
#                 raise ValueError('Token de acesso não encontrado no arquivo')
#             return access_token
#     except FileNotFoundError:
#         raise FileNotFoundError('Arquivo de token não encontrado. Faça a autenticação antes de listar os arquivos.')


# def list_files(access_token):
#     if access_token == '':
#         access_token = ACCESS_TOKEN
#     try:
#         headers = {
#             'Authorization': f'Bearer {access_token}'
#         }
#         response = requests.get('https://www.googleapis.com/drive/v3/files', headers=headers)

#         return response.json()
#     except FileNotFoundError as e:
#         return str(e)
#     except Exception as e:
#         return f'Erro: {str(e)}'


# def download_file(access_token, file_id):
#     try:
#         if access_token == '':
#             access_token = ACCESS_TOKEN
#         if file_id == '':
#             file_id = FILE_ID
#         file_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
#         start_time = time.time()
#         response = requests.get(file_url, headers={"Authorization": f"Bearer {access_token}"}, stream=True)
#         if not os.path.exists(FILE_PATH_DOWNLOAD):
#             os.makedirs(FILE_PATH_DOWNLOAD)

#         output_file = os.path.join(FILE_PATH_DOWNLOAD, "teste.pdf")
#         with open(output_file, 'wb') as output:
#             for chunk in response.iter_content(chunk_size=1024):
#                 if chunk:
#                     output.write(chunk)
#                     # Obter informações do sistema e da rede
#                     total_time = time.time() - start_time
#                     bytes_recv = psutil.net_io_counters().bytes_recv
#                     bytes_sent = psutil.net_io_counters().bytes_sent
#                     print(f"Tempo total: {total_time:.2f}s, Bytes recebidos: {bytes_recv}, Bytes enviados: {bytes_sent}")

#         # Obter informações do arquivo baixado
#         file_size = os.path.getsize(output_file)
#         print(f"Tamanho do arquivo baixado: {file_size} bytes")

#         return jsonify({'metadados':f'File downloaded successfully to {output_file}'})
#     except Exception as e:
#             print(f"Erro ao fazer download do arquivo: {str(e)}")
#             return "Erro ao fazer download do arquivo", 500


# def upload_file_to_drive():
#     creds = Credentials.from_authorized_user_file(ACCESS_TOKEN_FILE)
#     service = build('drive', 'v3', credentials=creds)

#     try:
#         if os.path.exists(FILE_PATH_UPLOAD):
#             print("File exists!")
#         else:
#             print("File does not exist.")
#         file_metadata = {'name': os.path.basename(FILE_PATH_UPLOAD), 'parents': [FOLDER_ID]}
#         media = MediaFileUpload(FILE_PATH_UPLOAD, resumable=True)
#         start_time = time.time()
#         file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#         total_time = time.time() - start_time

#         # Obter informações do sistema e da rede
#         bytes_recv = psutil.net_io_counters().bytes_recv
#         bytes_sent = psutil.net_io_counters().bytes_sent
#         print(f"Tempo total: {total_time:.2f}s, Bytes recebidos: {bytes_recv}, Bytes enviados: {bytes_sent}")
#         media.stream().close() 

#         # Obter informações do arquivo enviado
#         file_size = os.path.getsize(FILE_PATH_UPLOAD)
#         print(f"Tamanho do arquivo enviado: {file_size} bytes")
#         os.remove(FILE_PATH_UPLOAD)
#         return jsonify("Arquivo enviado com sucesso! ID:", file.get("id"))
    
#     except HttpError as error:
#         print(F'Um erro ocorreu: {error}')
#         return "Erro ao fazer download do arquivo", 500


# def get_folder_path(service, folder_ids):
#     """
#     Returns the full path of each folder in the list folder_ids, starting from the root folder.
#     """
#     folder_paths = []

#     for folder_id in folder_ids:
#         folder_path = []
#         folder = service.files().get(fileId=folder_id, fields='id, name, parents').execute()
        
#         folder_path.append(folder['name'])
        
#         while 'parents' in folder:
#             parent_id = folder['parents'][0]
#             parent = service.files().get(fileId=parent_id, fields='id, name, parents').execute()
#             folder_path.append(parent['name'])
#             folder = parent
        
#         folder_path.reverse()
        
#         folder_paths.append(folder_path)
    
#     return folder_paths
