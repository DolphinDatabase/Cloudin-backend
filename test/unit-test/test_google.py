import os
import sys
import pytest

from unittest import mock
from src.app import app
from src.controller.google import download_file, upload_file

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@mock.patch("requests.get")
def test_list_files_valid_token(mock_get):
    mock_get.return_value.json.return_value = {
        "files": [
            {"id": "123", "name": "file1", "size": 100},
            {"id": "456", "name": "file2", "size": 200},
        ]
    }
    client = app.test_client()
    response = client.get("/google/list", headers={"token": "valid_token"})
    assert response.status_code == 200
    assert response.json == {
        "result": [
            {"id": "123", "name": "file1", "size": 100},
            {"id": "456", "name": "file2", "size": 200},
        ]
    }


def test_list_files_invalid_token():
    client = app.test_client()
    response = client.get("/google/list", headers={"token": "invalid_token"})
    assert response.status_code == 500


@mock.patch("requests.get")
def test_download_file(mock_get):
    # Define o retorno simulado da requisição feita pelo requests.get()
    mock_get.return_value.iter_content.return_value = [b"test content"]
    mock_get.return_value.status_code = 200
    # Define as variáveis necessárias para a rota
    file_id = "123"
    file_name = "test_file"
    token = "valid_token"

    # Faz a requisição para a rota
    with app.app_context():
        response = download_file(file_id, file_name, token)
        # Verifica se a resposta é bem-sucedida e possui o conteúdo esperado
        assert response.status_code == 200
        assert response.json == {
            "title": file_name,
            "time": pytest.approx(0, abs=0.1),  # Verifica que o tempo é próximo de zero
            "size": len(b"test content"),
        }
        # Verifica se o arquivo foi criado corretamente
        assert os.path.exists(f"./downloads/google/{file_name}")
        with open(f"./downloads/google/{file_name}", "rb") as f:
            assert f.read() == b"test content"
        os.remove(f"./downloads/google/{file_name}")
        assert not os.path.exists(f"./downloads/google/{file_name}")


@mock.patch("requests.post")
@mock.patch("requests.put")
def test_upload_file(mock_put, mock_post):
    # Define o retorno simulado da requisição feita pelo requests.post()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "selfLink": "https://www.googleapis.com/drive/v2/files/123"
    }

    # Define o retorno simulado da requisição feita pelo requests.put()
    mock_put.return_value.status_code = 200

    # Define as variáveis necessárias para a rota
    file_name = "test_file"
    token = "valid_token"
    origin = "google"

    # Cria um arquivo de teste
    if not os.path.exists(f"./downloads/{origin}"):
        os.makedirs(f"./downloads/{origin}")
    with open(f"./downloads/{origin}/{file_name}", "wb") as f:
        f.write(b"test content")

    # Faz a requisição para a rota
    with app.app_context():
        response = upload_file(file_name, token, origin)

        # Verifica se a resposta é bem-sucedida e possui o conteúdo esperado
        assert response.status_code == 200
        assert response.json == {
            "title": file_name,
            "time": pytest.approx(0, abs=0.1),  # Verifica que o tempo é próximo de zero
            "size": len(b"test content"),
        }
        # Verifica se o arquivo foi removido corretamente
        assert not os.path.exists(f"./downloads/{origin}/{file_name}")
