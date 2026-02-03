import os
import pytest
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orm import Base

value = os.getenv("URL").strip()
engine = create_engine(value)
Session = sessionmaker(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_user():
    payload = {
        "email": "test6@local.com",
        "password": "AAa123456!#"
    }
    response = requests.post("http://127.0.0.1:8000/register", json=payload)
    assert response.status_code in [200, 201, 204]


