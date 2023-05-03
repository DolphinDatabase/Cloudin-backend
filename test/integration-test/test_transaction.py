import json
import pytest

from src.model.config import Config
from src.app import app, db

DATA_PATH = "test/config/data.json"


def return_data():
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data


DATA = return_data()


@pytest.fixture(scope="module")
def init_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

    yield db

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def test_client():
    with app.app_context():
        flask_app = app
        flask_app.testing = True
        testing_client = flask_app.test_client()
        ctx = flask_app.app_context()
        ctx.push()
        yield testing_client
        ctx.pop()


def test_config(init_database, test_client):
    with app.test_client() as test_client:
        json_config = {
            "origin": "google",
            "destiny": "s3",
            "originFolder": "google_folder",
            "destinyFolder": "s3_folder",
            "originToken": "google_token",
            "destinyToken": "s3_token",
        }

        response = test_client.post("/config", json=json_config)

        assert 200 == response.status_code

        config = db.session.query(Config).first()
        assert config is not None
        assert config.origin == "google"
        assert config.destiny == "s3"
        assert config.originFolder == "google_folder"
        assert config.destinyFolder == "s3_folder"
        assert config.originToken == "google_token"
        assert config.destinyToken == "s3_token"
