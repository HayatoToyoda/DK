# 答え合わせ 04

## 課題 1: クラスタを作って確認する

```bash
# 1. クラスタ作成
kind create cluster --name handson

# 2. ノード確認
kubectl get nodes
# NAME                    STATUS   ROLES           AGE   VERSION
# handson-control-plane   Ready    control-plane   2m    v1.32.x

# 3. kube-system のリソース確認
kubectl get all -n kube-system
# coredns, kube-proxy, kube-apiserver などが動いている

# 4. 接続先確認
kubectl config current-context
# kind-handson
```

---

## 課題 2: 用語の確認

**Cluster（クラスタ）**
Kubernetes の管理単位全体。Control Plane と複数の Node をまとめたもの。1つのシステムを動かす環境のまとまり。

**Node（ノード）**
コンテナが実際に動くサーバー（物理・仮想マシン）。kind では Docker コンテナ1つが Node として動く。

**Pod（ポッド）**
k8s でコンテナを実行する最小単位。1つ以上のコンテナを含む。Pod ごとに IP アドレスが割り当てられる。

**Control Plane（コントロールプレーン）**
クラスタ全体の頭脳。どの Node に Pod を配置するか（スケジューリング）、Pod が落ちたら再起動するか（コントローラ）、外部からの操作を受け付ける（API Server）などを担う。

---

## 課題 3: シナリオ例

**シナリオ:** ECサイトでセール期間中にアクセスが10倍になった

- **Docker Compose の場合:** 1台のサーバーにアプリコンテナが1つ。手動でサーバーを増やして `docker compose up` し直す必要がある。対応が遅れてサイトがダウン
- **Kubernetes の場合:** Horizontal Pod Autoscaler（HPA）を設定しておけば、CPU 使用率などのメトリクスに応じて自動でコンテナ数を増減してくれる。人手不要

他のシナリオ例:
- アプリコンテナがメモリリークでクラッシュ → k8s が自動再起動（セルフヒーリング）
- バージョンアップ中に新バージョンにバグ発見 → k8s のローリングアップデートなら旧バージョンに即ロールバック可能
