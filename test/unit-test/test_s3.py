import os
import sys
import pytest
from unittest.mock import MagicMock,patch
from src.services.s3 import s3Service
from src.app import app, db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture(scope="session")
def init_database():
    engine = create_engine("sqlite:///:memory:")
    db.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()

def test_files_by_folder():
    boto3_client = MagicMock(name= 'boto3.client')
    boto3_client.list_objects.return_value = {
        'Contents':["folder","file1","file2"]
    }
    with patch('boto3.client', return_value=boto3_client):
        service = s3Service("token token token token")
        result = service.files_by_folder(None)
    assert result == 2

def test_list_files_by_folder():
    boto3_client = MagicMock(name= 'boto3.client')
    boto3_client.list_objects.return_value = {
        'Contents': [
            {'Key': 'folder/file1.txt'},
            {'Key': 'folder/file2.txt'},
            {'Key': 'folder/subfolder/file3.txt'}
        ]
    }
    with patch('boto3.client', return_value=boto3_client):
        service = s3Service("token token token token")
        result = service.list_files_by_folder(folder='folder')
    assert result == [
        {'id': 'folder/file1.txt', 'name': 'file1.txt'},
        {'id': 'folder/file2.txt', 'name': 'file2.txt'},
        {'id': 'folder/subfolder/file3.txt', 'name': 'subfolder'}
    ]

def test_list_folders_valid_token():
    boto3_client = MagicMock(name= 'boto3.client')
    boto3_client.list_objects.return_value = { 
        "CommonPrefixes": [
            {"Prefix":"teste1/"},
            {"Prefix":"teste2/"},
        ]
    }
    with patch('boto3.client', return_value=boto3_client):
        client = app.test_client()
        result = client.get("/s3/list/folder", headers={"token":"token token token token"})
    assert result.status_code == 200
    assert result.json == {
        "result": [
            {"id":"teste1", "name":"teste1"},
            {"id":"teste2", "name":"teste2"},
        ]
    }
