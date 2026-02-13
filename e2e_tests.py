import os
import time
import uuid

import pytest
import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").strip()
if not API_URL:
    raise RuntimeError("API_URL nie jest ustawione! Sprawdź secrets w GitHub Actions.")


@pytest.fixture(scope="session", autouse=True)
def wait_for_api():
    """Czeka, aż API będzie dostępne przed uruchomieniem testów."""
    for i in range(20):
        try:
            response = requests.get(f"{API_URL}/health")
            if response.status_code == 200:
                print("API jest gotowe!")
                return
        except requests.exceptions.ConnectionError:
            pass
        print(f"Czekam na API... ({i + 1}/20)")
        time.sleep(2)
    pytest.fail("API nie wystartowało w ciągu 40 sekund")


def test_create_user():
    """Testuje endpoint rejestracji użytkownika z unikalnym emailem."""
    unique_email = f"test-{uuid.uuid4()}@local.com"
    payload = {
        "email": unique_email,
        "password": "AAa123456!#"
    }
    response = requests.post(f"{API_URL}/register", json=payload)
    assert response.status_code in [200, 201, 204]
    print(f"Utworzono użytkownika: {unique_email}")
