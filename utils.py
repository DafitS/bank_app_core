import uuid
from nanoid import generate

def generate_nanoid():
    return generate(size=10)

def generate_unique_account_number():
    return uuid.uuid4().int % (10**26)