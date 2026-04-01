# Phase 4: Kubernetes にデプロイする

## この章で学ぶこと

- Docker イメージを kind クラスタにロードする
- ConfigMap・Secret・PVC・Deployment・Service を組み合わせてアプリをデプロイする
- `livenessProbe` / `readinessProbe` でヘルスチェックを設定する
- initContainer で起動順序を制御する

所要時間の目安: **60〜90分**

---

## ファイル構成

```
phase4-k8s/
├── app.py             # /health エンドポイントを追加（k8s のProbe用）
├── requirements.txt
├── Dockerfile
├── README.md
└── k8s/
    ├── configmap.yaml      # DB接続情報（非秘密）
    ├── secret.yaml         # DBパスワード
    ├── pvc.yaml            # PostgreSQL のストレージ申請
    ├── db-deployment.yaml  # PostgreSQL の Deployment
    ├── db-service.yaml     # PostgreSQL の Service（ClusterIP）
    ├── app-deployment.yaml # TODO アプリの Deployment
    └── app-service.yaml    # TODO アプリの Service（NodePort）
```

---

## アーキテクチャ

```
外部アクセス
    │
    ▼
app-service（NodePort: 30500）
    │
    ▼
app-deployment（Pod × 2）
  ├── ConfigMap → 環境変数（DB_HOST, DB_NAME, DB_USER）
  ├── Secret    → 環境変数（DB_PASSWORD）
  └── initContainer → db-service が起動するまで待機
    │
    ▼
db-service（ClusterIP）
    │
    ▼
db-deployment（Pod × 1）
  ├── ConfigMap → 環境変数（POSTGRES_DB, POSTGRES_USER）
  ├── Secret    → 環境変数（POSTGRES_PASSWORD）
  └── PVC       → /var/lib/postgresql/data にマウント
```

---

## 手順

### 1. kind クラスタが起動していることを確認する

```bash
kubectl get nodes
# handson-control-plane が Ready であること
```

### 2. Docker イメージをビルドする

```bash
cd application/webapp/phase4-k8s

docker build -t todo-app:phase4 .
```

### 3. イメージを kind クラスタにロードする

kind はローカルの Docker デーモンと分離しているため、ビルドしたイメージを明示的にロードする必要があります。

```bash
kind load docker-image todo-app:phase4 --name handson
```

### 4. k8s リソースをすべて適用する

```bash
kubectl apply -f k8s/
```

### 5. 起動状況を確認する

```bash
# Pod の起動を確認（全部 Running になるまで待つ）
kubectl get pods -w

# 各リソースの確認
kubectl get deployments
kubectl get services
kubectl get pvc
```

### 6. アプリにアクセスする

ポートフォワードで接続します。

```bash
kubectl port-forward service/app-service 5000:5000
```

別ターミナルで API を試します：

```bash
curl http://localhost:5000/

curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "k8sでアプリをデプロイした！"}'

curl http://localhost:5000/tasks
```

### 7. Pod を削除して自動復旧を確認する

```bash
# app Pod を1つ削除
kubectl delete pod -l app=todo-app --wait=false

# すぐに確認（新しい Pod が起動される）
kubectl get pods -w
```

### 8. ログを確認する

```bash
# app の全 Pod のログ
kubectl logs -l app=todo-app

# db のログ
kubectl logs -l app=db
```

### 9. 後片付け

```bash
kubectl delete -f k8s/
```

---

## Phase 3（Compose）との比較

| | Phase 3（Compose）| Phase 4（k8s）|
|---|---|---|
| 起動コマンド | `docker compose up` | `kubectl apply -f k8s/` |
| スケール | 手動 | `kubectl scale` / 自動スケール可 |
| ヘルスチェック | `healthcheck:` | `livenessProbe` / `readinessProbe` |
| DB 待機 | `depends_on: condition: healthy` | `initContainer` |
| 設定管理 | `environment:` | ConfigMap + Secret |
| データ永続化 | `volumes:` | PVC + PV |
| 外部アクセス | `-p 5000:5000` | NodePort / port-forward |

---

## 学習のまとめ

おめでとうございます！ここまで来たあなたは以下を習得しました：

- Docker でアプリをコンテナ化する
- Docker Compose で複数コンテナを管理する
- Kubernetes の主要リソース（Pod / Deployment / Service / ConfigMap / Secret / PVC）を使いこなす
- 実際のアプリを段階的にコンテナ化し、k8s にデプロイする

次のステップとして以下を学ぶと実務に近づきます：
- Ingress（HTTP ルーティング）
- Horizontal Pod Autoscaler（自動スケール）
- Helm（k8s パッケージマネージャー）
- CI/CD パイプライン（GitHub Actions + k8s）
