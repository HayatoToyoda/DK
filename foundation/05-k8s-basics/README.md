# 05. k8s基礎（Pod・Deployment・Service）

## この章で学ぶこと

- Pod / Deployment / Service の役割と YAML の書き方
- `kubectl apply` / `get` / `describe` / `logs` / `delete`
- Service でコンテナにアクセスする方法

所要時間の目安: **60〜90分**

---

## 前提

04章で作った `handson` クラスタが起動していることを確認してください。

```bash
kubectl get nodes
# handson-control-plane が Ready であること
```

---

## Pod

### Pod とは？

k8s でコンテナを動かす最小単位です。1つ以上のコンテナを含みます。

**重要:** Pod を直接作ることは少なく、通常は Deployment を通して管理します。まずは Pod を理解するために直接作ってみましょう。

### Pod の YAML

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    app: my-app
spec:
  containers:
    - name: nginx
      image: nginx:alpine
      ports:
        - containerPort: 80
```

### Pod を作る

```bash
kubectl apply -f pod.yaml
```

### Pod の状態を確認する

```bash
# 一覧
kubectl get pods

# 詳細（イベント・エラー確認に有用）
kubectl describe pod my-pod

# ログ確認
kubectl logs my-pod

# Pod の中に入る
kubectl exec -it my-pod -- sh
```

### Pod を削除する

```bash
kubectl delete pod my-pod
# または
kubectl delete -f pod.yaml
```

---

## Deployment

### Deployment とは？

Pod の数や更新を管理するリソースです。
「Pod を3つ常に動かし続けて、1つ落ちたら自動で補充する」といった管理ができます。

```
Deployment
  └── ReplicaSet（Pod を指定数維持する）
        ├── Pod
        ├── Pod
        └── Pod
```

### Deployment の YAML

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  replicas: 3          # Pod を3つ起動する
  selector:
    matchLabels:
      app: my-app      # このラベルを持つ Pod を管理する
  template:
    metadata:
      labels:
        app: my-app    # Pod に付けるラベル
    spec:
      containers:
        - name: nginx
          image: nginx:alpine
          ports:
            - containerPort: 80
```

### Deployment を作る

```bash
kubectl apply -f deployment.yaml
```

### 確認する

```bash
# Deployment の確認
kubectl get deployments

# Pod が3つ起動しているか確認
kubectl get pods

# Pod を1つ削除してみる（自動で補充されるか確認）
kubectl delete pod <Pod名>
kubectl get pods   # すぐに新しい Pod が作られる
```

### スケールを変える

```bash
# レプリカ数を5に変更
kubectl scale deployment my-deployment --replicas=5
kubectl get pods
```

---

## Service

### Service とは？

Pod へのネットワークアクセスを提供するリソースです。
Pod は再起動するたびに IP が変わりますが、Service は固定の名前・IP でアクセスできる窓口を提供します。

### Service の種類

| 種類 | 用途 |
|---|---|
| `ClusterIP` | クラスタ内部からのアクセス（デフォルト）|
| `NodePort` | ホストのポートを通じて外部からアクセス |
| `LoadBalancer` | クラウドのロードバランサー経由でアクセス |

ローカル学習では `NodePort` を使います。

### Service の YAML

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  selector:
    app: my-app        # このラベルを持つ Pod に転送する
  ports:
    - port: 80         # Service が受け付けるポート
      targetPort: 80   # Pod の何番ポートに転送するか
      nodePort: 30080  # ホストの何番ポートで受け付けるか（30000-32767）
```

### Service を作る

```bash
kubectl apply -f service.yaml
```

### kind でローカルからアクセスする

kind クラスタに NodePort でアクセスするには、ポートフォワードを使います。

```bash
kubectl port-forward service/my-service 8080:80
```

ブラウザで `http://localhost:8080` にアクセスすると nginx が表示されます。

### 確認する

```bash
kubectl get services
kubectl describe service my-service
```

---

## ハンズオン: Deployment + Service を動かす

```bash
# 1. exercises/ の YAML を適用する
kubectl apply -f exercises/

# 2. Pod の起動を確認
kubectl get pods -w    # -w でリアルタイム更新

# 3. ポートフォワードでアクセス
kubectl port-forward service/my-service 8080:80

# 4. ブラウザで http://localhost:8080 を確認

# 5. 後片付け
kubectl delete -f exercises/
```

---

## kubectl コマンドまとめ

| コマンド | 説明 |
|---|---|
| `kubectl apply -f <ファイル>` | YAML からリソースを作成・更新 |
| `kubectl get <リソース>` | リソース一覧 |
| `kubectl describe <リソース> <名前>` | リソースの詳細（イベント含む）|
| `kubectl logs <Pod名>` | Pod のログ |
| `kubectl exec -it <Pod名> -- sh` | Pod の中に入る |
| `kubectl delete -f <ファイル>` | YAML のリソースを削除 |
| `kubectl scale deployment <名前> --replicas=N` | レプリカ数を変更 |
| `kubectl port-forward service/<名前> <ローカル>:<リモート>` | ポートフォワード |

---

## 演習

[exercises/](./exercises/) に YAML と課題があります。

---

次の章: [06. k8s応用（ConfigMap・Secret・PV）](../06-k8s-advanced/README.md)
