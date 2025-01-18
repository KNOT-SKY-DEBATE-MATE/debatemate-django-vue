# Python ベースイメージ
FROM python:3.12.8-slim

# 作業ディレクトリを作成
WORKDIR /app

# システム依存パッケージをインストール
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Python パッケージをインストール
COPY requirements.txt .

# Python パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# コンテナ起動時のデフォルトコマンド
CMD ["sh", "-c", "daphne --bind 0.0.0.0 --port $DJANGO_PORT $DJANGO_ASGI_MODULE:application"]
