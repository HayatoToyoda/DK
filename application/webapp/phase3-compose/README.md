# Phase 3: Docker Compose で PostgreSQL と連携する

## この章で学ぶこと

- PostgreSQL コンテナとアプリコンテナを Compose で連携させる
- 環境変数でデータベース接続情報を渡す
- ボリュームでデータを永続化する
- `healthcheck` と `depends_on` でサービス起動順序を制御する

所要時間の目安: **45〜60分**

---

## Phase 2 からの変化

| | Phase 2 | Phase 3 |
|---|---|---|
| データ保存先 | メモリ（再起動で消える）| PostgreSQL（永続化）|
| コンテナ数 | 1つ（app）| 2つ（app + db）|
| 起動方法 | `docker run` | `docker compose up` |

---

## ファイル構成

```
phase3-compose/
├── app.py           # PostgreSQL に接続するよう改修
├── requirements.txt # psycopg2-binary を追加
├── Dockerfile
├── compose.yml      # app + db の2サービス構成
└── README.md
```

---

## compose.yml の解説

```yaml
services:
  app:
    build: .
    environment:
      DB_HOST: db          # ← サービス名 "db" でDBに接続できる
      DB_NAME: tododb
      DB_USER: todouser
      DB_PASSWORD: todopass
    depends_on:
      db:
        condition: service_healthy  # ← DB の healthcheck が通るまで待つ

  db:
    image: postgres:16-alpine
    volumes:
      - db-data:/var/lib/postgresql/data  # ← データを永続化
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U todouser -d tododb"]
      interval: 5s
      retries: 5

volumes:
  db-data:   # ← 名前付きボリューム（コンテナを削除してもデータが残る）
```

---

## 手順

### 1. 起動する

```bash
cd application/webapp/phase3-compose

docker compose up -d
```

DB の healthcheck が通るまで app の起動が待機されます（初回は少し時間がかかります）。

### 2. ログで起動を確認する

```bash
docker compose logs -f
# app が "Running on http://0.0.0.0:5000" と表示されれば起動完了
```

`Ctrl+C` でログの追跡を止められます（コンテナは止まりません）。

### 3. API を試す

```bash
curl http://localhost:5000/

curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "PostgreSQLでデータを永続化した！"}'

curl http://localhost:5000/tasks
```

### 4. データ永続化を確認する

アプリコンテナを再起動してもデータが残ることを確認してください。

```bash
docker compose restart app
curl http://localhost:5000/tasks
# データが残っている！
```

### 5. PostgreSQL に直接接続してみる

```bash
docker compose exec db psql -U todouser -d tododb

# psql の中で
\dt          # テーブル一覧
SELECT * FROM tasks;
\q           # 終了
```

### 6. ボリュームを確認する

```bash
docker volume ls | grep phase3
```

### 7. 後片付け

```bash
# コンテナのみ削除（ボリュームは残る）
docker compose down

# コンテナ + ボリュームも削除（データが消える）
docker compose down -v
```

---

## app.py の変化ポイント

Phase 2 との主な違い:

1. `psycopg2` で PostgreSQL に接続
2. `init_db()` で起動時にテーブルを作成
3. `os.environ` で環境変数からDB接続情報を取得
4. データをメモリでなく DB に保存・取得

---

次のステップ: [Phase 4: Kubernetes にデプロイする](../phase4-k8s/README.md)
