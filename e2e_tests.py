import os
import pytest
import requests
import time
import uuid
from sqlalchemy import create_engine
from orm import Base  # tam gdzie masz Users, Accounts, Transactions

# URL do bazy i API
DATABASE_URL = os.getenv("URLFORTEST")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").strip()

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL nie jest ustawione! Sprawdź secrets w GitHub Actions.")
if not API_URL:
    raise RuntimeError("API_URL nie jest ustawione!")

# ---------------------------
# Fixture: Tworzy bazę na start
# ---------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Tworzy wszystkie tabele w bazie przed testami e2e."""
    engine = create_engine(DATABASE_URL)
    print("Resetuję bazę testową...")
    Base.metadata.drop_all(bind=engine)  # opcjonalnie usuwa stare tabele
    Base.metadata.create_all(bind=engine)
    yield
    print("Sprzątam po testach...")
    Base.metadata.drop_all(bind=engine)  # opcjonalnie usuwa tabele po testach

# ---------------------------
# Fixture: Czeka aż API będzie gotowe
# ---------------------------
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
        print(f"Czekam na API... ({i+1}/20)")
        time.sleep(2)
    pytest.fail("API nie wystartowało w ciągu 40 sekund")

# ---------------------------
# Test: Tworzenie użytkownika
# ---------------------------
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
