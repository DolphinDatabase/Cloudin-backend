import os
import sys
import pytest 
import boto3

from unittest import mock
from src.app import app
from src.controller.s3 import download_file, upload_file

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@mock.patch('boto3.client')
def test_list_folders_valid_token(mock_get):
    mock_get.list_objects.return_value = { 
        "CommonPrefixes": [
            {"Prefix":"teste1/"},
            {"Prefix":"teste2/"},
        ]
    }
    client = app.test_client()
    response = client.get("/s3/list/folder", headers={"token":"teste teste teste teste"})
    assert response.status_code == 200
    assert response.json != {
        "result": [
            {"id":"teste1", "name":"teste1"},
            {"id":"teste2", "name":"teste2"},
        ]
    }