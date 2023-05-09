import os
import sys
import pytest

from datetime import time
from src.utils.database import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.model.file import File

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    db.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()

def test_person_model(db_session):
    # Create a new person
    file = File()
    file.name = 'teste'
    file.size = 3.14
    file.time = time(hour=12,minute=12,second=12)

    # Add the person to the session and commit
    db_session.add(file)
    db_session.commit()

    # Query the person from the database
    result = db_session.query(File).filter_by(name='teste').first()

    # Check the result
    assert result is not None
    assert result.id == 1