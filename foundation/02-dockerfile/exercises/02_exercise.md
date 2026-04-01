# 演習 02: Dockerfile を書いてみる

---

## 課題 1: Dockerfile の穴埋め

以下の Dockerfile の `???` を埋めてください。
Node.js アプリをコンテナ化する想定です。

```dockerfile
# Node.js 20 の軽量版をベースにする
??? node:20-slim

# 作業ディレクトリを /app に設定する
??? /app

# package.json と package-lock.json をコピーする
??? package*.json .

# 依存パッケージをインストールする
??? npm ci

# 残りのファイルをすべてコピーする
??? . .

# ポート 3000 を使うことを明示する
??? 3000

# node server.js で起動する
??? ["node", "server.js"]
```

答えは [answers/](./answers/) で確認してください。

---

## 課題 2: .dockerignore を作る

以下のプロジェクト構成で、イメージに含めたくないものを `.dockerignore` に書いてください。

```
my-app/
├── node_modules/    ← コンテナ内で npm ci するので不要
├── .git/            ← git の履歴は不要
├── .env             ← 秘密情報なので絶対に含めない
├── *.log            ← ログファイルは不要
├── src/
│   └── index.js
└── package.json
```

---

## 課題 3: レイヤーの順番を考える

以下の 2 つの Dockerfile、どちらがビルドのキャッシュを有効活用できますか？理由も考えてください。

**Dockerfile A:**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

**Dockerfile B:**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```
