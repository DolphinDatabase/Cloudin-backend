from src.app import app, db
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session")
def init_database():
    engine = create_engine("sqlite:///:memory:")
    db.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()


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
