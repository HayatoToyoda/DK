# 03. Docker Compose

## この章で学ぶこと

- Docker Compose とは何か、なぜ必要か
- `compose.yml` の書き方
- 複数コンテナの起動・停止・ログ確認
- サービス間のネットワーク通信

所要時間の目安: **45〜60分**

---

## Docker Compose とは？

複数のコンテナを一度に定義・管理するツールです。

**なぜ必要か？**
Webアプリは「アプリ本体」「データベース」「キャッシュ」など、複数のコンテナで構成されることがほとんどです。
それらを毎回 `docker run` で起動するのは大変です。`compose.yml` に書いておけば、`docker compose up` 一発で全部起動できます。

```
docker run -d --name db -e POSTGRES_PASSWORD=secret postgres
docker run -d --name app --link db -p 8000:8000 my-app
# ↑ これを毎回打つのは辛い

# compose.yml に書けば:
docker compose up -d
# これだけで全部起動
```

---

## compose.yml の基本構造

```yaml
services:
  # サービス1（アプリ）
  app:
    build: .                    # Dockerfile からビルド
    ports:
      - "8000:8000"             # ホスト:コンテナ
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db                      # db が起動してから app を起動

  # サービス2（データベース）
  db:
    image: postgres:16          # Docker Hub のイメージをそのまま使う
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - db-data:/var/lib/postgresql/data   # データを永続化

volumes:
  db-data:    # 名前付きボリューム
```

---

## 主要な設定項目

| キー | 説明 |
|---|---|
| `image` | 使用するイメージ |
| `build` | Dockerfile のパス |
| `ports` | ポートマッピング（`ホスト:コンテナ`）|
| `environment` | 環境変数 |
| `depends_on` | 起動順序の依存関係 |
| `volumes` | データの永続化 |
| `networks` | カスタムネットワーク（省略時は自動作成）|

---

## サービス間通信

Compose で定義したサービスは、**サービス名でお互いを呼べます**。

```yaml
services:
  app:
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      #                                        ↑ サービス名 "db" でアクセスできる
  db:
    image: postgres:16
```

同じ Compose ファイル内のサービスは自動的に同じネットワークに属するため、IPアドレスを使わずにサービス名で通信できます。

---

## ハンズオン: nginx + HTML を Compose で動かす

### 1. ディレクトリを作る

```bash
mkdir ~/compose-practice && cd ~/compose-practice
```

### 2. 表示する HTML を作る

`html/index.html`:
```html
<!DOCTYPE html>
<html>
<head><title>Compose Practice</title></head>
<body>
  <h1>Hello from Docker Compose!</h1>
</body>
</html>
```

### 3. compose.yml を作る

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html:ro
```

### 4. 起動する

```bash
docker compose up -d
```

ブラウザで `http://localhost:8080` を開くと HTML が表示されます。

### 5. ログを確認する

```bash
# 全サービスのログ
docker compose logs

# リアルタイムでログを流す
docker compose logs -f

# 特定サービスのログ
docker compose logs web
```

### 6. 起動中のサービスを確認する

```bash
docker compose ps
```

### 7. 停止・削除する

```bash
# 停止（コンテナは残す）
docker compose stop

# 停止してコンテナも削除
docker compose down

# コンテナ・ネットワーク・ボリュームすべて削除
docker compose down -v
```

---

## コマンドまとめ

| コマンド | 説明 |
|---|---|
| `docker compose up -d` | バックグラウンドで起動 |
| `docker compose down` | 停止してコンテナを削除 |
| `docker compose ps` | サービスの状態確認 |
| `docker compose logs -f` | リアルタイムログ表示 |
| `docker compose exec <サービス> bash` | サービスのコンテナに入る |
| `docker compose build` | イメージを再ビルド |
| `docker compose restart` | 再起動 |

---

## 演習

[exercises/](./exercises/) に課題があります。

---

次の章: [04. Kubernetesとは？](../04-what-is-kubernetes/README.md)
