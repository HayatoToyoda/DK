# 答え合わせ 02

## 課題 1: Dockerfile の穴埋め

```dockerfile
FROM node:20-slim
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

---

## 課題 2: .dockerignore

```
node_modules/
.git/
.env
*.log
```

**ポイント:**
- `node_modules/` はコンテナ内で `npm ci` を実行するので不要。コピーすると逆に遅くなる
- `.env` は秘密情報（APIキー・パスワード等）が含まれることが多いため、**絶対にイメージに含めない**
- `.git/` を含めると不要なデータでイメージが大きくなる

---

## 課題 3: レイヤーの順番

**正解: Dockerfile B**

理由:

```dockerfile
# Dockerfile B
COPY requirements.txt .   ← requirements.txt が変わらない限りキャッシュが使われる
RUN pip install ...        ← ↑ がキャッシュヒットなら、ここもスキップされる（時間節約！）
COPY . .                   ← コードだけ変わっても pip install は再実行されない
```

```dockerfile
# Dockerfile A（非効率）
COPY . .                   ← コードを1行変えるだけでこのレイヤーが無効化される
RUN pip install ...        ← コードが変わるたびに毎回 pip install が実行される（遅い！）
```

**原則:** 変化の少ないもの（設定ファイル・依存定義）を先に、変化の多いもの（アプリコード）を後にする。
