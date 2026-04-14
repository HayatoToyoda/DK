# 演習 2: インフラ視点の MLOps 体験（ハンズオン）

## 課題

MLOps のインフラ側を体験するために、MLflow を Docker Compose で起動してみましょう。

### 要件

1. 以下の `compose.yml` を使って MLflow Tracking Server を起動する
2. ブラウザで MLflow UI にアクセスする
3. Python スクリプトで簡単な実験ログを記録する

### Step 1: compose.yml の作成

```yaml
services:
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.16.0
    ports:
      - "5000:5000"
    command: mlflow server --host 0.0.0.0 --port 5000
```

```bash
docker compose up -d
```

### Step 2: MLflow UI にアクセス

ブラウザで `http://localhost:5000` にアクセス。

### Step 3: 実験を記録する Python スクリプト

```python
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("devops-learning")

with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("epochs", 100)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("loss", 0.05)
    print("実験ログを記録しました。MLflow UI で確認してください。")
```

```bash
pip install mlflow
python log_experiment.py
```

### 確認ポイント

- [ ] MLflow UI が表示されるか
- [ ] 実験ログが記録されるか
- [ ] パラメータとメトリクスが UI で確認できるか

### 発展: K8s で GPU ノードを確認する（クラウド環境がある場合）

```bash
# ノードのラベルを確認（GPU ノードには特別なラベルが付いている）
kubectl get nodes --show-labels | grep -i gpu

# GPU リソースの確認
kubectl describe node <node-name> | grep -A 5 "Allocatable"
```

答えは [answers/](../answers/) で確認できます。
