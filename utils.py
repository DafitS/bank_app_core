import uuid
from nanoid import generate
from passlib.context import CryptContext

def generate_nanoid():
    return generate(size=10)

def generate_unique_account_number():
    return uuid.uuid4().int % (10**26)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
