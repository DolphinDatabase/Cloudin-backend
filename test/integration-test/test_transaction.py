import json
import os
from src.app import app, db

from src.model.config import Config
from src.services.google import GoogleService
from src.services.s3 import s3Service
from time import sleep

DATA_PATH = "test/config/data.json"

FOLDER_GOOGLE = os.environ.get("GOOGLE_FOLDER")
FOLDER_S3 = os.environ.get("S3_FOLDER")

TOKEN_GOOGLE = os.environ.get("GOOGLE_TOKEN")
TOKEN_S3 = os.environ.get("S3_TOKEN")


def return_data():
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data


def pre_operation(originName):
    path = f"downloads/{originName}/test_{originName}.txt"
    conteudo = "Este é o conteúdo do arquivo."

    # Cria o diretório se ele não existir
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Cria o arquivo no caminho especificado
    with open(path, "w") as arquivo:
        arquivo.write(conteudo)

    file_name = f"test_{originName}.txt"
    return file_name


def assert_list_contains(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    assert set1.intersection(set2) == set1


DATA = return_data()


def test_create_config(init_database, test_client):
    with app.test_client() as test_client:
        json_config = {
            "origin": "google",
            "destiny": "s3",
            "originFolder": FOLDER_GOOGLE,
            "destinyFolder": FOLDER_S3,
            "originToken": TOKEN_GOOGLE,
            "destinyToken": TOKEN_S3,
        }

        response = test_client.post("/config", json=json_config)

        assert 200 == response.status_code

        config = db.session.query(Config).first()
        assert config is not None
        assert config.origin == "google"
        assert config.destiny == "s3"
        assert config.originFolder == FOLDER_GOOGLE
        assert config.destinyFolder == FOLDER_S3
        assert config.originToken == TOKEN_GOOGLE
        assert config.destinyToken == TOKEN_S3


def test_upload_file_to_google():
    file_name = pre_operation("google")
    google_service = GoogleService(refreshToken=TOKEN_GOOGLE)
    google_service.upload(file_name, "google", FOLDER_GOOGLE)
    files = google_service.list_files_by_folder(FOLDER_GOOGLE)
    file_exists = False
    for file in files:
        if file["name"] == file_name:
            file_exists = True
            break
    assert file_exists


def test_transaction_from_google_to_s3(test_client):
    google_service = GoogleService(refreshToken=TOKEN_GOOGLE)

    s3_service = s3Service(token=TOKEN_S3)
    previous_files = google_service.list_files_by_folder(FOLDER_GOOGLE)

    assert previous_files != []

    json_config = {
        "origin": "google",
        "destiny": "s3",
        "originFolder": FOLDER_GOOGLE,
        "destinyFolder": FOLDER_S3,
        "originToken": TOKEN_GOOGLE,
        "destinyToken": TOKEN_S3,
    }

    response = test_client.post("/config", json=json_config)
    assert response.status_code == 200

    sleep(120)

    current_files = google_service.list_files_by_folder(FOLDER_GOOGLE)
    assert current_files == []

    google_files_names = []
    for file in previous_files:
        google_files_names.append(file["name"])

    s3_files = s3_service.list_files_by_folder(FOLDER_S3)
    s3_files_names = []

    for file in s3_files:
        s3_files_names.append(file["name"])

    assert_list_contains(google_files_names, s3_files_names)
