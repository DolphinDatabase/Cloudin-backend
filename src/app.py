from flask import Flask, jsonify
import os
import requests
from .utils import google_drive
import os

app = Flask(__name__)

@app.route("/")
def helloWorld():
    return "Hello World!"


@app.route('/auth/google')
def authenticate():
    return google_drive.authenticate()
    

@app.route('/auth/google/refresh-token')
def refresh_token():
    return google_drive.refresh_token()


@app.route('/google/files')
def list_files(access_token=''):
    return google_drive.list_files(access_token)


@app.route('/google/download')
def download_item(access_token='', file_id=''):
 
    return google_drive.download_file(access_token, file_id)
