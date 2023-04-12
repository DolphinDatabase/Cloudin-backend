import json
from src.app import app, db
from src.model.transaction import Transaction
from src.model.file import File
import pytest

DATA_PATH = "test/config/data.json"


def return_data():
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data


DATA = return_data()


@pytest.fixture(scope="module")
def test_client():
    with app.app_context():
        flask_app = app
        testing_client = flask_app.test_client()
        ctx = flask_app.app_context()
        ctx.push()
        yield testing_client
        ctx.pop()


@pytest.fixture(scope="module")
def init_database():
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


def test_create_transaction(init_database, test_client):
    response = test_client.post(
        "/transaction/", data=json.dumps(DATA["body"]), headers=DATA["headers"]
    )
    assert response.status_code == 200
    assert response.content_type == "application/json"

    transaction_data = json.loads(response.data)

    # Verifica se a transação foi salva no banco de dados
    transaction = Transaction.query.filter_by(origin="google", destiny="s3").first()
    assert transaction is not None
    assert transaction.status == "Concluido"
    assert len(transaction.file) == 1

    # Verifica se os arquivos foram salvos no banco de dados
    for f in transaction.file:
        assert f.name in ["SeminÃ¡rio de S.O"]
        assert f.time is not None
        assert f.size is not None
