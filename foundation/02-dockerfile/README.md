# 02. Dockerfile の書き方

## この章で学ぶこと

- Dockerfile とは何か
- 主要な命令: `FROM` / `RUN` / `COPY` / `WORKDIR` / `CMD`
- イメージのビルドと実行
- レイヤーの仕組み

所要時間の目安: **45〜60分**

---

## Dockerfile とは？

イメージを作るための「レシピ」です。
「どのOSをベースにして、何をインストールして、どのファイルをコピーして、どのコマンドで起動するか」を記述します。

```dockerfile
# ベースイメージを指定
FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存ファイルをコピー
COPY requirements.txt .

# ライブラリをインストール
RUN pip install -r requirements.txt

# アプリのコードをコピー
COPY . .

# コンテナ起動時に実行するコマンド
CMD ["python", "app.py"]
```

---

## 主要な命令

| 命令 | 説明 |
|---|---|
| `FROM <イメージ>` | ベースイメージを指定（必ず最初に書く） |
| `WORKDIR <パス>` | 作業ディレクトリを設定（以降のコマンドはここで実行される） |
| `COPY <src> <dest>` | ホストからコンテナにファイルをコピー |
| `RUN <コマンド>` | イメージビルド時にコマンドを実行（レイヤーが増える） |
| `CMD ["コマンド"]` | コンテナ起動時に実行するデフォルトコマンド |
| `ENV KEY=VALUE` | 環境変数を設定 |
| `EXPOSE <ポート>` | コンテナが使うポートを明示（ドキュメント的な意味合い） |

---

## レイヤーの仕組み

Dockerfile の各命令は「レイヤー」を作ります。
レイヤーはキャッシュされるため、変わっていない部分は再ビルド時にスキップされます。

```
FROM python:3.12-slim   ← レイヤー1（ベース）
WORKDIR /app            ← レイヤー2
COPY requirements.txt . ← レイヤー3
RUN pip install ...     ← レイヤー4（時間がかかる）
COPY . .                ← レイヤー5
CMD [...]               ← レイヤー6
```

**重要なポイント:** 変化の少ないもの（requirements.txt）を先にコピーし、変化の多いもの（コード）を後にすることで、再ビルドが速くなります。

---

## ハンズオン: シンプルな Python アプリをコンテナ化する

### 1. アプリファイルを作る

```bash
mkdir ~/docker-practice && cd ~/docker-practice
```

`app.py` を作成:
```python
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello from Docker!")

HTTPServer(("", 8000), Handler).serve_forever()
```

`requirements.txt` を作成（今回は空でOK）:
```
# no dependencies
```

### 2. Dockerfile を作る

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "app.py"]
```

### 3. イメージをビルドする

```bash
docker build -t my-python-app .
```

- `-t my-python-app`: イメージに名前（タグ）をつける
- `.`: Dockerfile のある場所（カレントディレクトリ）

### 4. コンテナを起動する

```bash
docker run -d -p 8000:8000 --name my-app my-python-app
```

ブラウザで `http://localhost:8000` を開くと `Hello from Docker!` が表示されます。

### 5. イメージの詳細を確認する

```bash
# イメージの一覧
docker images

# イメージのレイヤー構造を確認
docker history my-python-app
```

### 6. 後片付け

```bash
docker stop my-app
docker rm my-app
docker rmi my-python-app
```

---

## .dockerignore

`.gitignore` のようなファイルです。ビルド時にコンテナに送らないファイルを指定します。

```
# .dockerignore
__pycache__/
*.pyc
.venv/
.git/
```

これを作っておくと、不要なファイルがイメージに含まれず、ビルドが速くなります。

---

## コマンドまとめ

| コマンド | 説明 |
|---|---|
| `docker build -t <名前> .` | Dockerfile からイメージをビルド |
| `docker images` | イメージ一覧 |
| `docker history <イメージ>` | イメージのレイヤー構造を確認 |
| `docker rmi <イメージ>` | イメージを削除 |

---

## 演習

[exercises/](./exercises/) に課題があります。やってみましょう。

---

次の章: [03. Docker Compose](../03-docker-compose/README.md)
