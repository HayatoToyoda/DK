# Docker & Kubernetes ハンズオンリポジトリ 設計ドキュメント

**作成日:** 2026-04-02  
**対象者:** Docker/Kubernetes 未経験の入社2年目インフラエンジニア  
**目的:** 概念理解と実践スキルを両立するハンズオン学習環境の構築

---

## 背景と目的

Docker・Kubernetes の知識が「何がわからないかもわからない」状態から、実務でコンテナを作成・デプロイできるレベルまで成長するための学習リポジトリ。
ステップバイステップの基礎編と、実際に動くサンプルアプリを使った応用編を組み合わせることで、技術の「なぜ必要か」を体感しながら学べる構成とする。

---

## 対象環境

- OS: Mac M4 (Apple Silicon)
- 初期状態: 何もインストールされていない
- インストール対象: Homebrew / Docker Desktop / kubectl / kind / Python 3

---

## リポジトリ構造

```
DK/
├── README.md                              # 全体ガイド・学習ロードマップ
├── SETUP.md                               # Mac M4 環境セットアップ手順
├── .gitignore
│
├── foundation/                            # ステップバイステップ基礎編
│   ├── 01-what-is-docker/
│   │   ├── README.md
│   │   ├── exercises/
│   │   └── answers/
│   ├── 02-dockerfile/
│   ├── 03-docker-compose/
│   ├── 04-what-is-kubernetes/
│   ├── 05-k8s-basics/
│   └── 06-k8s-advanced/
│
├── application/
│   └── webapp/                            # Python Flask + PostgreSQL TODOアプリ
│       ├── phase1-local/
│       ├── phase2-docker/
│       ├── phase3-compose/
│       └── phase4-k8s/
│
└── docs/
    └── superpowers/
        └── specs/
            └── 2026-04-02-docker-kubernetes-handson-design.md
```

---

## 学習ロードマップ

```
[SETUP.md] 環境構築
     ↓
[foundation/01] Dockerとは？
[foundation/02] Dockerfileの書き方
[foundation/03] Docker Compose
     ↓
[application/phase1] アプリをローカルで動かす
[application/phase2] アプリをDockerで動かす
[application/phase3] Composeで複数コンテナ連携
     ↓
[foundation/04] Kubernetesとは？
[foundation/05] k8s基礎（Pod・Deployment・Service）
[foundation/06] k8s応用（ConfigMap・Secret・PV）
     ↓
[application/phase4] アプリをk8sにデプロイ
```

DockerをひととおりやったあとにアプリでDockerを使い、その後k8sに進む。
「なぜk8sが必要か」をアプリを動かした後に学ぶことで、必要性を実感しやすくする。

---

## Foundation 各章の内容

| 章 | タイトル | 学ぶこと |
|---|---|---|
| 01 | Dockerとは？ | コンテナ vs VM、イメージとコンテナの違い、`docker run/ps/stop/rm` |
| 02 | Dockerfile | `FROM/RUN/COPY/CMD`、ビルドと実行、レイヤーの仕組み |
| 03 | Docker Compose | `compose.yml` の文法、複数コンテナの起動・停止・ログ確認 |
| 04 | Kubernetesとは？ | なぜDockerだけでは本番が辛いか、クラスタ構成図、kindでクラスタ作成 |
| 05 | k8s基礎 | Pod・Deployment・Service のYAML、`kubectl apply/get/describe/logs` |
| 06 | k8s応用 | ConfigMap・Secret（環境変数管理）、PersistentVolume（データ永続化） |

### 各章の構成

```
README.md     ← 概念説明（図も含む）＋ハンズオン手順（コマンド付き）
exercises/    ← 穴埋め問題・「自分でやってみよう」課題
answers/      ← 完成形ファイル（答え合わせ用）
```

---

## Application 各フェーズの内容

**サンプルアプリ:** Python Flask + PostgreSQL の TODOアプリ（タスクの追加・一覧表示）

| フェーズ | 内容 |
|---|---|
| phase1-local | `app.py` + `requirements.txt`、ローカルで実行 |
| phase2-docker | `Dockerfile` を書いてコンテナ化、`docker build & run` |
| phase3-compose | `docker-compose.yml`（Flask + PostgreSQL）、環境変数・ネットワーク |
| phase4-k8s | Deployment / Service / ConfigMap / Secret / PersistentVolume の全YAML |

---

## ツール選定の理由

| ツール | 採用理由 |
|---|---|
| Docker Desktop | Apple Silicon 対応、GUI で状態が見やすく初心者に優しい |
| kind | Docker内でk8sを動かす軽量ツール。M4対応済み、minikubeより軽い |
| Python Flask | シンプルで説明しやすい。k8sで複数コンテナを学ぶのに適切な規模 |
| PostgreSQL | 本番でよく使われるDB。PersistentVolumeの学習にも最適 |
