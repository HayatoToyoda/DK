# 演習 06: ConfigMap・Secret・PVC を使う

---

## 課題 1: ConfigMap の値を確認する

1. `configmap.yaml` を適用する
2. `kubectl describe configmap app-config` で値を確認する
3. 以下の Pod を作って、環境変数が渡っているか確認する

```yaml
# test-pod.yaml として保存して apply する
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
    - name: test
      image: alpine
      command: ["sh", "-c", "env && sleep 3600"]
      envFrom:
        - configMapRef:
            name: app-config
```

Pod に入って `env | grep APP_ENV` を実行してみてください。

---

## 課題 2: Secret の値をデコードする

1. `secret.yaml` を適用する
2. `kubectl get secret app-secret -o yaml` で Base64 の値を確認する
3. 以下のコマンドで `DB_PASSWORD` をデコードしてみる

```bash
echo "c3VwZXJzZWNyZXQ=" | base64 --decode
```

元の値は何でしたか？

---

## 課題 3: PVC を作って状態を確認する

1. `pvc.yaml` を適用する
2. `kubectl get pvc` で `STATUS` が `Bound` になっていることを確認する
3. `kubectl describe pvc app-pvc` で詳細を確認する

---

## 課題 4: 考えてみよう

1. ConfigMap と Secret の使い分けはどうすればいい？
2. Secret の値は Base64 エンコードされているが、これは「暗号化」ではない。なぜ安全と言えないのか？
   （ヒント: Base64 は簡単にデコードできる）

---

## 後片付け

```bash
kubectl delete -f ./
kubectl delete pod test-pod
```
