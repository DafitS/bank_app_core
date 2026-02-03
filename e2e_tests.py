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
        "email": "test@local.cm",
        "password": "Aa123456!"
    }
    response = requests.post("http://127.0.0.1:8000/register", json=payload)
    assert response.status_code in [200, 201, 204]


def test_list_users():
    payload = {
        "email": "test22@local.cm",
        "password": "Aa123456!"
    }
    requests.post("http://127.0.0.1:8000/register", json=payload)

    response = requests.get("http://127.0.0.1:8000/users")
    assert response.status_code == 200

    users = response.json()
    assert any(u["email"] == "test22@local.com" for u in users)


def test_create_account():
    payload = {
        "email": "test33@local.cm",
        "password": "Aa123456!"
    }
    requests.post("http://127.0.0.1:8000/register", json=payload)

    users = requests.get("http://127.0.0.1:8000/users").json()
    user_id = users[-1]["id"]

    payload = {"user_id": user_id}
    response = requests.post("http://127.0.0.1:8000/account", json=payload)
    assert response.status_code in [200, 201, 204]
