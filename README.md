# Docker & Kubernetes ハンズオン

入社2年目のインフラエンジニアが Docker / Kubernetes を「何がわからないかもわからない」状態から、実務でコンテナを作成・デプロイできるレベルまで成長するための学習リポジトリです。

---

## このリポジトリの使い方

1. まず **[SETUP.md](./SETUP.md)** を読んで環境を整える
2. **foundation（基礎編）** でステップバイステップに概念と操作を学ぶ
3. **application（応用編）** で実際のアプリを動かしながら理解を深める

---

## 学習ロードマップ

```
[SETUP.md] 環境構築（Homebrew / Docker Desktop / kubectl / kind）
     ↓
[foundation/01] Dockerとは？（コンテナの概念・基本コマンド）
[foundation/02] Dockerfileの書き方（イメージのビルド）
[foundation/03] Docker Compose（複数コンテナの連携）
     ↓
[application/phase1] サンプルアプリをローカルで動かす
[application/phase2] サンプルアプリをDockerで動かす
[application/phase3] Composeを使ってDB込みで動かす
     ↓
[foundation/04] Kubernetesとは？（なぜDockerだけでは足りないか）
[foundation/05] k8s基礎（Pod / Deployment / Service）
[foundation/06] k8s応用（ConfigMap / Secret / PersistentVolume）
     ↓
[application/phase4] サンプルアプリをk8sにデプロイ
     ↓
[foundation/07] DevOps ロードマップ 2026（全体像の把握）
[foundation/08] CI/CD（GitHub Actions でパイプライン構築）
[foundation/09] IaC（Terraform でインフラをコード管理）
[foundation/10] GitOps（ArgoCD でクラスタ自動同期）
[foundation/11] 監視と可観測性（Prometheus + Grafana + Loki）
[foundation/12] DevSecOps（セキュリティのシフトレフト）
[foundation/13] MLOps / AIOps（AI 時代のインフラ運用）
```

---

## ディレクトリ構成

```
DK/
├── README.md          # このファイル
├── SETUP.md           # 環境セットアップ手順
│
├── foundation/        # 基礎編（ステップバイステップ）
│   ├── 01-what-is-docker/
│   ├── 02-dockerfile/
│   ├── 03-docker-compose/
│   ├── 04-what-is-kubernetes/
│   ├── 05-k8s-basics/
│   ├── 06-k8s-advanced/
│   ├── 07-devops-roadmap/    # DevOps ロードマップ 2026
│   ├── 08-ci-cd/             # CI/CD（GitHub Actions）
│   ├── 09-iac-terraform/     # IaC（Terraform）
│   ├── 10-gitops/            # GitOps（ArgoCD / Flux）
│   ├── 11-monitoring-observability/  # 監視と可観測性
│   ├── 12-devsecops/         # DevSecOps
│   └── 13-mlops-aiops/       # MLOps / AIOps
│
└── application/       # 応用編（実アプリで学ぶ）
    └── webapp/        # Python Flask + PostgreSQL TODOアプリ
        ├── phase1-local/
        ├── phase2-docker/
        ├── phase3-compose/
        └── phase4-k8s/
```

各章の `README.md` にその章で学ぶことと手順が書かれています。`exercises/` で手を動かし、`answers/` で答え合わせができます。

> **Docker & Kubernetes を学び終えたら、07 以降の DevOps セクションに進みましょう。** 2026 年のインフラエンジニアに求められる CI/CD、IaC、GitOps、監視、セキュリティ、MLOps までを体系的に学べます。

---

## 対象環境

- Mac M4 (Apple Silicon)
- セットアップは SETUP.md を参照

---

## 困ったとき

- エラーメッセージをそのままコピーして調べる
- `docker logs <コンテナ名>` / `kubectl describe pod <Pod名>` でログを確認する
- わからないことはそのままにせず、「なぜそうなるか」まで調べることが上達の近道
