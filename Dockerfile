# 1. Oficjalny obraz Pythona
FROM python:3.12-slim

# 2. Ustawienia środowiska
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Instalacja zależności systemowych
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. Katalog aplikacji
WORKDIR /app


# 6. Instalacja zależności Pythona
COPY . .
RUN pip install --no-cache-dir .



# 8. Uruchamianie FastAPI przez Uvicorn
CMD ["uvicorn", "api:api", "--host", "0.0.0.0", "--port", "8000"]
