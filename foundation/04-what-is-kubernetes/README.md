# 04. Kubernetesとは？

## この章で学ぶこと

- なぜ Docker だけでは本番運用が辛いのか
- Kubernetes が解決すること
- クラスタの構成と主要な概念
- kind でローカルクラスタを作る

所要時間の目安: **45〜60分**

---

## なぜ Kubernetes が必要か？

Docker Compose で複数コンテナを管理できるようになりました。
しかし、本番環境では以下のような問題が起きます。

### 問題 1: コンテナが落ちたら？

```
コンテナがクラッシュ → 手動で再起動が必要 → サービス停止
```

### 問題 2: アクセスが増えたら？

```
アクセス急増 → 1台のサーバーでは捌ききれない → スケールアップが大変
```

### 問題 3: サーバーが死んだら？

```
サーバー1台が障害 → その上のコンテナがすべて停止 → 完全ダウン
```

### Kubernetes が解決すること

| 問題 | Kubernetes の解決策 |
|---|---|
| コンテナが落ちる | 自動で再起動（セルフヒーリング）|
| アクセスが増える | コンテナ数を自動で増減（オートスケール）|
| サーバーが死ぬ | 別のサーバーでコンテナを自動起動（フェイルオーバー）|
| デプロイが怖い | ローリングアップデート（無停止でバージョンアップ）|

---

## Kubernetes の構成

```
┌─────────────────── Cluster ───────────────────────┐
│                                                    │
│  ┌─── Control Plane ───┐                          │
│  │  API Server          │                          │
│  │  Scheduler           │                          │
│  │  Controller Manager  │                          │
│  └─────────────────────┘                          │
│                                                    │
│  ┌── Node 1 ──┐  ┌── Node 2 ──┐  ┌── Node 3 ──┐ │
│  │ Pod Pod Pod │  │ Pod Pod    │  │ Pod        │ │
│  └────────────┘  └────────────┘  └────────────┘ │
└────────────────────────────────────────────────────┘
```

| 用語 | 説明 |
|---|---|
| **Cluster** | k8s の管理単位。Control Plane と Node の集まり |
| **Control Plane** | クラスタ全体を管理する頭脳。スケジューリングや状態管理を担う |
| **Node** | コンテナが実際に動くサーバー（物理・仮想どちらでも可）|
| **Pod** | k8s でコンテナを動かす最小単位。1つ以上のコンテナを含む |

---

## 主要なリソース（概念の整理）

この章では概念だけ紹介します。実際の操作は 05 章で行います。

| リソース | 役割 |
|---|---|
| **Pod** | コンテナの実行単位 |
| **Deployment** | Pod の数や更新を管理 |
| **Service** | Pod へのネットワークアクセスを提供 |
| **ConfigMap** | 設定値を管理（環境変数など）|
| **Secret** | 秘密情報を管理（パスワード・APIキー）|
| **PersistentVolume** | データの永続化 |

---

## ハンズオン: kind でクラスタを作る

### 1. クラスタを作成する

```bash
kind create cluster --name handson
```

作成には1〜2分かかります。

### 2. クラスタの状態を確認する

```bash
# ノードの確認
kubectl get nodes

# 出力例:
# NAME                    STATUS   ROLES           AGE   VERSION
# handson-control-plane   Ready    control-plane   1m    v1.32.x
```

`STATUS` が `Ready` になれば成功です。

### 3. クラスタの詳細情報を見る

```bash
kubectl cluster-info
```

### 4. 全リソースの確認（最初は何もない）

```bash
# デフォルト namespace のリソース
kubectl get all

# システム用 namespace のリソース
kubectl get all -n kube-system
```

### 5. kind のクラスタ一覧

```bash
kind get clusters
```

### 6. kubectl の接続先確認

```bash
kubectl config current-context
# kind-handson と表示されれば OK
```

---

## Docker と Kubernetes の使い分け

| 用途 | Docker Compose | Kubernetes |
|---|---|---|
| 開発環境 | ✓ 向いている | △ 複雑すぎる |
| 小規模本番 | △ 手動管理が必要 | ✓ 向いている |
| 大規模本番 | ✗ 向かない | ✓ 向いている |
| 学習コスト | 低い | 高い |

開発環境は Docker Compose、本番環境は Kubernetes という使い分けが一般的です。

---

## コマンドまとめ

| コマンド | 説明 |
|---|---|
| `kind create cluster --name <名前>` | クラスタ作成 |
| `kind delete cluster --name <名前>` | クラスタ削除 |
| `kind get clusters` | クラスタ一覧 |
| `kubectl get nodes` | ノード一覧 |
| `kubectl cluster-info` | クラスタ情報 |
| `kubectl config current-context` | 現在の接続先 |

---

## 演習

[exercises/](./exercises/) に課題があります。

---

次の章: [05. k8s基礎（Pod・Deployment・Service）](../05-k8s-basics/README.md)
