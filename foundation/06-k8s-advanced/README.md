# 06. k8s応用（ConfigMap・Secret・PersistentVolume）

## この章で学ぶこと

- ConfigMap: 設定値・環境変数の管理
- Secret: 秘密情報（パスワード・APIキー）の管理
- PersistentVolume / PersistentVolumeClaim: データの永続化

所要時間の目安: **60〜90分**

---

## ConfigMap

### ConfigMap とは？

設定値や環境変数をコンテナの外で管理するリソースです。
「設定が変わるたびにイメージをビルドし直す」のではなく、ConfigMap を更新するだけで済みます。

### ConfigMap の YAML

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  APP_ENV: production
  LOG_LEVEL: info
  DATABASE_HOST: db-service
```

### Pod から ConfigMap を使う（環境変数として）

```yaml
spec:
  containers:
    - name: app
      image: my-app:latest
      envFrom:
        - configMapRef:
            name: my-config    # ConfigMap 名を指定
```

または個別に指定:

```yaml
      env:
        - name: APP_ENV
          valueFrom:
            configMapKeyRef:
              name: my-config
              key: APP_ENV
```

### 確認コマンド

```bash
kubectl apply -f configmap.yaml
kubectl get configmaps
kubectl describe configmap my-config
```

---

## Secret

### Secret とは？

パスワード・APIキー・証明書などの秘密情報を管理するリソースです。
値は Base64 エンコードで保存されます（暗号化ではないことに注意）。

### Secret の YAML

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  # echo -n "mypassword" | base64 で生成
  DB_PASSWORD: bXlwYXNzd29yZA==
  API_KEY: c2VjcmV0LWFwaS1rZXk=
```

Base64 エンコード/デコードの方法:

```bash
# エンコード
echo -n "mypassword" | base64
# bXlwYXNzd29yZA==

# デコード
echo "bXlwYXNzd29yZA==" | base64 --decode
# mypassword
```

### Pod から Secret を使う

```yaml
      envFrom:
        - secretRef:
            name: my-secret
```

### 確認コマンド

```bash
kubectl apply -f secret.yaml
kubectl get secrets
kubectl describe secret my-secret
# ※ describe では値は表示されない（セキュリティのため）
```

---

## PersistentVolume / PersistentVolumeClaim

### なぜ必要か？

Pod は削除されると中のデータが消えます。
データベースのデータをコンテナに保存すると、Pod が再起動するたびにデータが消えてしまいます。

**PersistentVolume（PV）** と **PersistentVolumeClaim（PVC）** を使うとデータを永続化できます。

```
PersistentVolume（PV）
  └── クラスタが提供するストレージ領域（管理者が準備）

PersistentVolumeClaim（PVC）
  └── PV を使いたいという申請（開発者が書く）

Pod
  └── PVC をマウントしてデータを読み書き
```

### PVC の YAML（kind ではこれだけで OK）

```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce        # 1つの Node から読み書き可能
  resources:
    requests:
      storage: 1Gi         # 1GB 要求
```

kind（ローカル環境）では `StorageClass` が自動でストレージを提供してくれるため、PV を自分で作る必要はありません。

### Pod から PVC を使う

```yaml
spec:
  containers:
    - name: db
      image: postgres:16
      volumeMounts:
        - name: db-storage
          mountPath: /var/lib/postgresql/data   # コンテナ内のマウント先
  volumes:
    - name: db-storage
      persistentVolumeClaim:
        claimName: my-pvc    # PVC 名を指定
```

---

## ハンズオン: ConfigMap + Secret + PVC を組み合わせる

`exercises/` の YAML を使って、設定値・秘密情報・永続化を一通り試してみましょう。

```bash
# 適用
kubectl apply -f exercises/

# 確認
kubectl get configmaps
kubectl get secrets
kubectl get pvc
kubectl get pods

# 後片付け
kubectl delete -f exercises/
```

---

## リソースまとめ

| リソース | 用途 | 値の管理 |
|---|---|---|
| ConfigMap | 設定値・環境変数 | 平文 |
| Secret | 秘密情報 | Base64（暗号化ではない）|
| PVC | ストレージ申請 | - |
| PV | ストレージ実体 | - |

---

## kubectl コマンドまとめ

| コマンド | 説明 |
|---|---|
| `kubectl get configmaps` | ConfigMap 一覧 |
| `kubectl get secrets` | Secret 一覧 |
| `kubectl get pvc` | PVC 一覧 |
| `kubectl get pv` | PV 一覧 |
| `kubectl describe configmap <名前>` | ConfigMap の詳細 |

---

## 演習

[exercises/](./exercises/) に YAML と課題があります。

---

基礎編はここまでです。次は応用編へ進みましょう。

次のステップ: [application/webapp/phase1-local](../../application/webapp/phase1-local/README.md)
