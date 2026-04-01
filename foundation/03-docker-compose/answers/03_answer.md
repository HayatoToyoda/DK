# 答え合わせ 03

## 課題 1: compose.yml の穴埋め

```yaml
services:
  wordpress:
    image: wordpress:latest
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wpuser
      WORDPRESS_DB_PASSWORD: wppass
      WORDPRESS_DB_NAME: wpdb
    depends_on:
      - db

  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: wpdb
      MYSQL_USER: wpuser
      MYSQL_PASSWORD: wppass
    volumes:
      - mysql-data:/var/lib/mysql

volumes:
  mysql-data:
```

---

## 課題 2: コマンドを答える

```bash
# 1. バックグラウンドで起動
docker compose up -d

# 2. 全サービスのリアルタイムログ
docker compose logs -f

# 3. db サービスのコンテナに入る
docker compose exec db bash

# 4. 停止してコンテナ・ボリュームも全削除
docker compose down -v
```

---

## 課題 3: サービス名で通信できる理由

Docker Compose は起動時に**自動でブリッジネットワーク**を作成し、すべてのサービスをそのネットワークに接続します。

Docker の内部 DNS が、サービス名をそのコンテナの IP アドレスに解決してくれるため、`db` や `wordpress` といったサービス名でそのままアクセスできます。

```
wordpress コンテナ → "db" という名前で DNS 解決 → db コンテナの IP → MySQL に接続
```

これにより、IP アドレスをハードコードする必要がなく、コンテナが再起動して IP が変わっても問題ありません。
