# 演習 1: ArgoCD で自動デプロイを体験

## 課題

kind クラスタに ArgoCD をインストールし、phase4-k8s のマニフェストを自動同期してください。

### 要件

1. ArgoCD を `argocd` namespace にインストール
2. Application リソースを作成し、`application/webapp/phase4-k8s/k8s` のマニフェストを同期対象にする
3. 自動同期（`automated`）と自動修復（`selfHeal`）を有効にする
4. K8s マニフェストを変更して Git にプッシュし、ArgoCD が自動で同期することを確認する

### ヒント

- `kubectl port-forward` で ArgoCD UI にアクセス可能
- `kubectl -n argocd get applications` で Application の状態を確認
- 手動同期は `argocd app sync todo-app` でも可能

### 確認ポイント

- [ ] ArgoCD UI で Application が `Synced` & `Healthy` になっているか
- [ ] K8s マニフェストを変更後、自動で同期されるか
- [ ] Pod を手動削除しても自動復旧するか

答えは [answers/](../answers/) で確認できます。
