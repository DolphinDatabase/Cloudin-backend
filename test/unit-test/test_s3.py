import os
import sys

from unittest.mock import MagicMock,patch
from src.services.s3 import s3Service

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_filesByFolder():
    boto3_client = MagicMock(name= 'boto3.client')
    boto3_client.list_objects.return_value = {
        'Contents':["folder","file1","file2"]
    }
    with patch('boto3.client', return_value=boto3_client):
        service = s3Service("token token token token")
        result = service.files_by_folder(None)
    assert result == 2

# def test_listFilesByFolder():


# @mock.patch('boto3.client')
# def test_list_folders_valid_token(mock_get):
#     mock_get.list_objects.return_value = { 
#         "CommonPrefixes": [
#             {"Prefix":"teste1/"},
#             {"Prefix":"teste2/"},
#         ]
#     }
#     client = app.test_client()
#     response = client.get("/s3/list/folder", headers={"token":"teste teste teste teste"})
#     assert response.status_code == 200
#     assert response.json != {
#         "result": [
#             {"id":"teste1", "name":"teste1"},
#             {"id":"teste2", "name":"teste2"},
#         ]
#     }
