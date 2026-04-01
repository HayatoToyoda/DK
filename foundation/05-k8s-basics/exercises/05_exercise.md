# 演習 05: Pod・Deployment・Service を動かす

---

## 課題 1: Deployment + Service を適用する

1. `deployment.yaml` と `service.yaml` を `kubectl apply` で適用する
2. Pod が2つ起動したことを確認する
3. `kubectl describe deployment my-deployment` でレプリカの状態を確認する
4. ポートフォワードで `http://localhost:8080` にアクセスして nginx を確認する

```bash
kubectl port-forward service/my-service 8080:80
```

---

## 課題 2: セルフヒーリングを確認する

1. 起動中の Pod の名前を `kubectl get pods` で確認する
2. Pod を1つ削除する（`kubectl delete pod <Pod名>`）
3. すぐに `kubectl get pods` を実行して、新しい Pod が自動で補充されることを確認する

---

## 課題 3: スケールを変えてみる

1. レプリカ数を `4` に変更する
2. `kubectl get pods` で Pod が4つになることを確認する
3. レプリカ数を `1` に戻す

---

## 課題 4: YAML の穴埋め

以下の Deployment YAML の `???` を埋めてください。
「`httpd:alpine` イメージを使った Pod を2つ、ラベル `app: web` で管理する」構成です。

```yaml
???: apps/v1
???: Deployment
metadata:
  name: web-deployment
spec:
  ???: 2
  selector:
    matchLabels:
      app: ???
  template:
    metadata:
      labels:
        app: ???
    spec:
      containers:
        - name: httpd
          ???: httpd:alpine
          ports:
            - containerPort: 80
```

---

## 後片付け

```bash
kubectl delete -f ./
```
