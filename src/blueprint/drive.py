from flask import Blueprint
from ..utils import google_drive

drivebp = Blueprint('google', __name__, url_prefix='/google')

@drivebp.route('/auth')
def authenticate():
    return google_drive.authenticate()
    

@drivebp.route('/auth/refresh-token')
def refresh_token():
    return google_drive.refresh_token()


@drivebp.route('/files')
def list_files(access_token=''):
    return google_drive.list_files(access_token)


@drivebp.route('/download')
def download_item(access_token='', file_id=''):
 
    return google_drive.download_file(access_token, file_id)


@drivebp.route('/upload')
def upload_item():
 
    return google_drive.upload_file_to_drive()