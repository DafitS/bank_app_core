FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Katalog główny aplikacji
WORKDIR /app

# Kopiuj pliki projektu do /app
COPY pyproject.toml .

# Zainstaluj narzędzia do budowania i zbuduj pakiet
RUN pip install --no-cache-dir build
RUN python -m build

# Zainstaluj utworzony pakiet
RUN pip install --no-cache-dir dist/bank_app-0.1.0-py3-none-any.whl

# Skopiuj cały folder bank_app do obrazu
COPY bank_app ./bank_app

# Domyślne polecenie uruchomienia
CMD ["uvicorn", "bank_app.api.main:api", "--host", "0.0.0.0", "--port", "8000"]