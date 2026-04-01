# 答え合わせ 06

## 課題 1: ConfigMap の値を確認する

```bash
kubectl apply -f configmap.yaml
kubectl describe configmap app-config

# test-pod を作って環境変数を確認
kubectl apply -f test-pod.yaml
kubectl exec -it test-pod -- sh
env | grep APP_ENV
# APP_ENV=development
```

---

## 課題 2: Secret の値をデコードする

```bash
kubectl apply -f secret.yaml
kubectl get secret app-secret -o yaml
# data:
#   DB_PASSWORD: c3VwZXJzZWNyZXQ=
#   API_KEY: bXktYXBpLWtleS0xMjM0NQ==

echo "c3VwZXJzZWNyZXQ=" | base64 --decode
# supersecret
```

元の値は `supersecret` です。

---

## 課題 3: PVC を作って状態を確認する

```bash
kubectl apply -f pvc.yaml
kubectl get pvc
# NAME      STATUS   VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
# app-pvc   Bound    ...      512Mi      RWO            standard       10s

kubectl describe pvc app-pvc
```

`STATUS: Bound` になっていれば、ストレージが確保されています。

---

## 課題 4: 考えてみよう

**1. ConfigMap と Secret の使い分け**

| ConfigMap | Secret |
|---|---|
| 公開しても問題ない設定値 | 漏れると困る情報 |
| アプリの環境名・ログレベル・URLなど | パスワード・APIキー・証明書など |

迷ったら: 「この値が git に入っても問題ないか？」→ 問題ない → ConfigMap、問題ある → Secret

**2. Secret が「暗号化でない」理由と注意点**

Base64 は「エンコード（符号化）」であり「暗号化」ではありません。
誰でも簡単にデコードできるため、Base64 にしても秘密情報を隠す効果はありません。

```bash
echo "c3VwZXJzZWNyZXQ=" | base64 --decode
# supersecret  ← 誰でも読める
```

**なぜ Secret を使うのか？**
- YAML に平文で書かずに済む（kubectl describe でも値が非表示になる）
- アクセス制御（RBAC）で「Secret を読める人を制限」できる
- etcd（k8s のデータストア）の暗号化設定と組み合わせると実際に保護できる

本番では Secret の値をそのまま git に commit しないこと。
外部シークレット管理ツール（AWS Secrets Manager、Vault など）との連携が推奨されます。
