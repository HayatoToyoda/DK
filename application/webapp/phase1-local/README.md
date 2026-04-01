# Phase 1: ローカルでアプリを動かす

## この章で学ぶこと

- サンプルアプリ（Flask TODO API）の構成を理解する
- ローカル環境（Python 仮想環境）で動かす
- API の動作を確認する

所要時間の目安: **20〜30分**

---

## アプリの概要

シンプルな TODO アプリの REST API です。

| エンドポイント | メソッド | 内容 |
|---|---|---|
| `/` | GET | ヘルスチェック・タスク数確認 |
| `/tasks` | GET | タスク一覧を取得 |
| `/tasks` | POST | タスクを追加 |
| `/tasks/<id>` | PATCH | タスクを完了にする |

**Phase 1 の特徴:** データはメモリ上に保存するため、アプリを再起動するとデータが消えます。
（Phase 3 で PostgreSQL を使ってデータを永続化します）

---

## ローカルで起動する

### 1. Python 仮想環境を作る

```bash
cd application/webapp/phase1-local

python3 -m venv .venv
source .venv/bin/activate
```

### 2. 依存パッケージをインストールする

```bash
pip install -r requirements.txt
```

### 3. アプリを起動する

```bash
python app.py
```

`Running on http://0.0.0.0:5000` と表示されれば起動成功です。

---

## API を試す

別のターミナルで以下を実行してください。

### ヘルスチェック

```bash
curl http://localhost:5000/
# {"message": "TODO App is running!", "tasks_count": 0}
```

### タスクを追加する

```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Dockerを学ぶ"}'
# {"done": false, "id": 1, "title": "Dockerを学ぶ"}

curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Kubernetesを学ぶ"}'
```

### タスク一覧を取得する

```bash
curl http://localhost:5000/tasks
# {"tasks": [{"done": false, "id": 1, "title": "Dockerを学ぶ"}, ...]}
```

### タスクを完了にする

```bash
curl -X PATCH http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

---

## 確認してみよう

アプリを `Ctrl+C` で止めてから再起動してみてください。
タスクのデータが消えることを確認してください。

これが「データの永続化」が必要な理由です。
Phase 3 で PostgreSQL を使って解決します。

---

次のステップ: [Phase 2: Dockerで動かす](../phase2-docker/README.md)
