# Phase 2: Docker でアプリを動かす

## この章で学ぶこと

- Phase 1 のアプリを Dockerfile でコンテナ化する
- `docker build` と `docker run` の実践
- コンテナで動くアプリと、ローカルで動くアプリの違いを体感する

所要時間の目安: **30〜45分**

---

## ファイル構成

```
phase2-docker/
├── app.py            # Phase 1 と同じアプリ
├── requirements.txt  # Flask の依存
├── Dockerfile        # イメージのビルド手順
└── README.md
```

---

## Dockerfile の解説

```dockerfile
FROM python:3.12-slim      # ① 軽量な Python イメージをベースにする

WORKDIR /app               # ② 作業ディレクトリを /app に設定

COPY requirements.txt .    # ③ 依存定義ファイルを先にコピー
RUN pip install --no-cache-dir -r requirements.txt  # ④ ライブラリをインストール

COPY app.py .              # ⑤ アプリ本体をコピー（コードが変わっても④のキャッシュが使える）

EXPOSE 5000                # ⑥ ポート 5000 を使うことを宣言

CMD ["python", "app.py"]   # ⑦ コンテナ起動時に実行するコマンド
```

③④ を先に、⑤ を後にする理由は [foundation/02-dockerfile](../../../foundation/02-dockerfile/README.md) で学んだ「レイヤーキャッシュ」です。

---

## 手順

### 1. イメージをビルドする

```bash
cd application/webapp/phase2-docker

docker build -t todo-app:phase2 .
```

ビルドログに `Successfully built` が表示されれば成功です。

### 2. イメージを確認する

```bash
docker images | grep todo-app
```

### 3. コンテナを起動する

```bash
docker run -d -p 5000:5000 --name todo-phase2 todo-app:phase2
```

### 4. API を試す

```bash
# ヘルスチェック
curl http://localhost:5000/

# タスクを追加
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Dockerでアプリを動かした！"}'

# タスク一覧
curl http://localhost:5000/tasks
```

### 5. コンテナのログを確認する

```bash
docker logs todo-phase2
```

### 6. コンテナを再起動してデータが消えることを確認する

```bash
docker restart todo-phase2
curl http://localhost:5000/tasks
# {"tasks": []} ← データが消えている
```

Phase 3 で PostgreSQL を使ってこの問題を解決します。

### 7. 後片付け

```bash
docker stop todo-phase2
docker rm todo-phase2
```

---

## Phase 1 との違い

| | Phase 1（ローカル） | Phase 2（Docker）|
|---|---|---|
| 実行環境 | Mac の Python | コンテナ内の Python |
| セットアップ | venv + pip install | docker build のみ |
| 環境の再現性 | Macに依存 | どこでも同じ |
| データの永続化 | なし | なし（次のフェーズで解決）|

---

次のステップ: [Phase 3: Composeでデータベースと連携する](../phase3-compose/README.md)
