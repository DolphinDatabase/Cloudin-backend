from src.app import app, db
import pytest


@pytest.fixture(scope="session")
def init_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

    yield db

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="session")
def test_client():
    with app.app_context():
        flask_app = app
        flask_app.testing = True
        testing_client = flask_app.test_client()
        ctx = flask_app.app_context()
        ctx.push()
        yield testing_client
        ctx.pop()
