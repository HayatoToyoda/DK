# 演習 03: Docker Compose を書いてみる

---

## 課題 1: compose.yml の穴埋め

WordPress + MySQL の構成です。`???` を埋めてください。

```yaml
???:
  wordpress:
    ???: wordpress:latest
    ports:
      - "8080:80"
    ???:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wpuser
      WORDPRESS_DB_PASSWORD: wppass
      WORDPRESS_DB_NAME: wpdb
    depends_on:
      - ???

  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: wpdb
      MYSQL_USER: wpuser
      MYSQL_PASSWORD: wppass
    ???:
      - mysql-data:/var/lib/mysql

???: 
  mysql-data:
```

---

## 課題 2: コマンドを答える

以下の操作をするコマンドを書いてください。

1. compose.yml のサービスをバックグラウンドで起動する
2. 全サービスのリアルタイムログを見る
3. `db` サービスのコンテナに bash で入る
4. サービスを停止してコンテナとボリュームも含めて全削除する

---

## 課題 3: 考えてみよう

compose.yml でサービス名を使ってサービス間通信ができるのはなぜですか？
Docker の何という機能が関係していますか？
