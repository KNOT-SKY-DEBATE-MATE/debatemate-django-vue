# Python ベースイメージ
FROM python:3.12.8-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "daphne --bind 0.0.0.0 --port $DJANGO_PORT $DJANGO_ASGI_MODULE:application"]
