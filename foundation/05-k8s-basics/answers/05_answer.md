# 答え合わせ 05

## 課題 1〜3: コマンド手順

```bash
# 1. 適用
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# 2. Pod 確認
kubectl get pods
# NAME                             READY   STATUS    RESTARTS   AGE
# my-deployment-xxxxxxxxx-xxxxx   1/1     Running   0          30s
# my-deployment-xxxxxxxxx-yyyyy   1/1     Running   0          30s

# 3. Deployment 詳細
kubectl describe deployment my-deployment

# 4. ポートフォワード
kubectl port-forward service/my-service 8080:80
# → http://localhost:8080 で nginx 確認

# セルフヒーリング確認
kubectl delete pod <Pod名>
kubectl get pods    # すぐに新しい Pod が Running になる

# スケール変更
kubectl scale deployment my-deployment --replicas=4
kubectl get pods    # 4つになる
kubectl scale deployment my-deployment --replicas=1
```

---

## 課題 4: YAML の穴埋め

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: httpd
          image: httpd:alpine
          ports:
            - containerPort: 80
```

**ポイント:**
- `selector.matchLabels` と `template.metadata.labels` のラベルは**必ず一致**させる
- 一致していないと Deployment が Pod を管理できずエラーになる
- `apiVersion: apps/v1` は Deployment に必要（Pod は `v1`、Deployment は `apps/v1`）
