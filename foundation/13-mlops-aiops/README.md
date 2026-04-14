# 13. MLOps / AIOps — AI 時代のインフラ運用

> ⏱ 所要時間目安: 2〜3 時間（読み物 + 概念演習）
>
> **本章の構成**: 幅広いトピックを扱います。すべてを一度に覚える必要はありません。
> - **Track A**: MLOps の基本概念（データサイエンスに関心がある人向け）
> - **Track B**: システム設計・DR・カオスエンジニアリング（インフラに集中したい人向け）
> - 両方を学ぶのが理想ですが、興味のある Track から始めてください。

## この章で学ぶこと

- MLOps の概念と DevOps との関係
- ML パイプラインの構築
- モデルのバージョン管理とデプロイ
- AIOps によるインテリジェントな運用
- AI インフラストラクチャの基本（GPU / LLM サービング）
- Platform Engineering への進化

---

## DevOps → MLOps → AIOps の進化

```mermaid
flowchart TB
    DevOps["DevOps<br/>アプリケーションの<br/>CI/CD 自動化"]
    MLOps["MLOps<br/>ML モデルの<br/>ライフサイクル管理"]
    AIOps["AIOps<br/>AI による<br/>インフラ運用自動化"]
    PlatEng["Platform Engineering<br/>開発者プラットフォーム<br/>の構築・運用"]

    DevOps --> MLOps
    DevOps --> AIOps
    DevOps --> PlatEng
    MLOps --> AIInfra["AI Infrastructure<br/>GPU クラスタ / LLM サービング"]
    AIOps --> AIInfra

    style DevOps fill:#2196F3,color:#fff
    style MLOps fill:#9C27B0,color:#fff
    style AIOps fill:#E91E63,color:#fff
    style PlatEng fill:#FF9800,color:#fff
    style AIInfra fill:#F44336,color:#fff
```

| 領域 | 目的 | 代表的なスキル |
|------|------|-------------|
| **DevOps** | アプリの迅速な開発・デプロイ | CI/CD, IaC, K8s, GitOps |
| **MLOps** | ML モデルの実験→学習→デプロイ→監視 | ML パイプライン, モデルレジストリ |
| **AIOps** | AI で運用作業を自動化・最適化 | 異常検知, 予測スケーリング, 自動修復 |
| **Platform Engineering** | 開発者向けセルフサービスプラットフォーム | IDP, Backstage, ゴールデンパス |

---

## MLOps とは

### ML ライフサイクル

```mermaid
flowchart LR
    Data["データ収集<br/>& 前処理"]
    Train["モデル<br/>学習"]
    Eval["評価<br/>& 検証"]
    Registry["モデル<br/>レジストリ"]
    Deploy["モデル<br/>デプロイ"]
    Monitor["モデル<br/>監視"]

    Data --> Train --> Eval --> Registry --> Deploy --> Monitor
    Monitor -. "データドリフト<br/>検出 → 再学習" .-> Data

    style Data fill:#2196F3,color:#fff
    style Train fill:#4CAF50,color:#fff
    style Eval fill:#FF9800,color:#fff
    style Registry fill:#9C27B0,color:#fff
    style Deploy fill:#F44336,color:#fff
    style Monitor fill:#E91E63,color:#fff
```

### DevOps と MLOps の比較

| 観点 | DevOps | MLOps |
|------|--------|-------|
| **バージョン管理** | コード | コード + データ + モデル |
| **テスト** | ユニット / 結合テスト | モデル精度 / データ品質テスト |
| **ビルド** | Docker イメージ | モデルアーティファクト |
| **デプロイ** | コンテナ → K8s | モデルサーバー → 推論エンドポイント |
| **監視** | レイテンシ / エラー率 | 精度劣化 / データドリフト |

### MLOps ツール

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 20, 'rankSpacing': 30, 'subgraphTitleMargin': 8}}}%%
flowchart LR
    subgraph Exp["実験"]
        MLflow["MLflow"]
        W_B["W&B"]
    end

    subgraph Pipe["パイプライン"]
        Kubeflow["Kubeflow"]
        Airflow["Airflow"]
    end

    subgraph Serve["サービング"]
        KServe["KServe"]
        Seldon["Seldon"]
    end

    subgraph Data["データ管理"]
        DVC["DVC"]
        LakeFS["LakeFS"]
    end

    style Exp fill:#e8f5e9
    style Pipe fill:#e3f2fd
    style Serve fill:#fff3e0
    style Data fill:#fce4ec
```

| カテゴリ | ツール | 概要 |
|---------|--------|------|
| **実験管理** | MLflow, W&B | パラメータ・メトリクス・モデルの追跡 |
| **パイプライン** | Kubeflow, Airflow | データ前処理→学習→デプロイの自動化 |
| **モデルサービング** | KServe, Seldon | K8s 上でモデルを推論APIとして公開 |
| **データ管理** | DVC, LakeFS | データセットのバージョン管理 |

---

## AIOps とは

AIOps は **AI/ML を使ってインフラ運用を自動化・最適化** する手法です。

```mermaid
flowchart TB
    Data["運用データ<br/>メトリクス / ログ / トレース"]

    Data --> Anomaly["異常検知<br/>通常パターンからの<br/>逸脱を自動検出"]
    Data --> RCA["根本原因分析<br/>障害の原因を<br/>AI が特定"]
    Data --> Predict["予測<br/>リソース需要の<br/>予測・自動スケール"]
    Data --> Auto["自動修復<br/>既知パターンの<br/>障害を自動復旧"]

    style Data fill:#2196F3,color:#fff
    style Anomaly fill:#FF9800,color:#fff
    style RCA fill:#4CAF50,color:#fff
    style Predict fill:#9C27B0,color:#fff
    style Auto fill:#F44336,color:#fff
```

### AIOps の活用例

| ユースケース | 説明 | ツール例 |
|------------|------|---------|
| **異常検知** | メトリクスの異常パターンを自動検出 | Prometheus + ML モデル |
| **ログ分析** | 大量のログからインシデントを自動分類 | Loki + LLM |
| **予測スケーリング** | トラフィック予測に基づく事前スケール | KEDA + カスタムメトリクス |
| **自動修復** | 既知障害パターンの自動対応 | Kubernetes Operator |
| **インシデント管理** | アラートの重複排除・優先度付け | PagerDuty / Opsgenie |

---

## AI インフラストラクチャ

2026 年、**AI / LLM のインフラ構築** は DevOps エンジニアの新たな重要スキルです。

### GPU クラスタの管理

```mermaid
flowchart TB
    User["ML エンジニア"]
    K8s["Kubernetes クラスタ"]
    GPU["GPU ノードプール<br/>NVIDIA A100 / H100"]
    Scheduler["GPU スケジューラ<br/>リソース配分"]
    Train["学習ジョブ"]
    Serve["推論サーバー"]

    User --> K8s
    K8s --> GPU
    GPU --> Scheduler
    Scheduler --> Train
    Scheduler --> Serve

    style K8s fill:#326CE5,color:#fff
    style GPU fill:#76B900,color:#fff
```

### LLM サービングの構成

```mermaid
flowchart LR
    Client["クライアント"]
    LB["ロードバランサ"]
    Gateway["API Gateway /<br/>AI Gateway"]
    Serve1["vLLM<br/>Instance 1"]
    Serve2["vLLM<br/>Instance 2"]
    Model["モデルストレージ<br/>S3 / GCS"]

    Client --> LB --> Gateway
    Gateway --> Serve1
    Gateway --> Serve2
    Model --> Serve1
    Model --> Serve2

    style Client fill:#2196F3,color:#fff
    style Gateway fill:#FF9800,color:#fff
    style Serve1 fill:#4CAF50,color:#fff
    style Serve2 fill:#4CAF50,color:#fff
```

| 技術 | 概要 |
|------|------|
| **vLLM** | 高スループットの LLM 推論エンジン |
| **NVIDIA Triton** | マルチモデル推論サーバー |
| **KServe** | K8s ネイティブの ML モデルサービング |
| **Ray Serve** | 分散 ML サービングフレームワーク |

---

## Platform Engineering

DevOps の進化形が **Platform Engineering** です。

```mermaid
flowchart TB
    Dev["開発者"]
    IDP["Internal Developer<br/>Platform（IDP）"]

    Dev -- "セルフサービスで<br/>インフラを利用" --> IDP

    IDP --> K8s["Kubernetes"]
    IDP --> CI["CI/CD<br/>パイプライン"]
    IDP --> Obs["可観測性<br/>スタック"]
    IDP --> Sec["セキュリティ<br/>ポリシー"]

    IDP --> Backstage["Backstage<br/>（Spotify OSS）"]
    IDP --> Crossplane["Crossplane<br/>（K8s ネイティブ IaC）"]
    IDP --> Kratix["Kratix<br/>（プラットフォーム API）"]

    style Dev fill:#2196F3,color:#fff
    style IDP fill:#FF9800,color:#fff
    style Backstage fill:#e8f5e9
    style Crossplane fill:#e8f5e9
    style Kratix fill:#e8f5e9
```

### Platform Engineering の目的

- 開発者が **インフラの詳細を知らなくても** アプリをデプロイできる
- **ゴールデンパス** を提供し、ベストプラクティスをデフォルトにする
- チケット駆動のインフラ申請を **セルフサービス** に変える

---

## システム設計とDR / カオスエンジニアリング

### システム設計の基本概念

DevOps エンジニアが知るべきシステム設計の要素：

| 概念 | 説明 |
|------|------|
| **可用性（Availability）** | 99.9% = 年間 8.76 時間のダウンタイム |
| **スケーラビリティ** | 水平スケール（Pod 追加） vs 垂直スケール（リソース増強） |
| **レジリエンス** | 障害が発生しても機能を維持する能力 |
| **冗長性** | マルチ AZ / マルチリージョンでの配置 |

### Disaster Recovery（DR）

```mermaid
flowchart LR
    subgraph Primary["プライマリ（東京）"]
        P_App["アプリ"]
        P_DB["DB"]
    end

    subgraph DR["DR サイト（大阪）"]
        D_App["アプリ<br/>（スタンバイ）"]
        D_DB["DB<br/>（レプリカ）"]
    end

    P_DB -- "非同期レプリケーション" --> D_DB
    Primary -. "障害発生時に<br/>フェイルオーバー" .-> DR

    style Primary fill:#e8f5e9
    style DR fill:#fff3e0
```

| DR 戦略 | RTO | RPO | コスト |
|---------|-----|-----|-------|
| **Backup & Restore** | 数時間 | 数時間 | 低 |
| **Pilot Light** | 数十分 | 数分 | 中 |
| **Warm Standby** | 数分 | 秒単位 | 高 |
| **Multi-Site Active** | ゼロ | ゼロ | 最高 |

### カオスエンジニアリング

> 本番環境に **意図的に障害を注入** し、システムの回復力を検証する。

```mermaid
flowchart LR
    Steady["定常状態を<br/>定義"]
    Hypothesis["仮説を<br/>立てる"]
    Inject["障害を<br/>注入"]
    Observe["観察 &<br/>分析"]
    Improve["改善"]

    Steady --> Hypothesis --> Inject --> Observe --> Improve
    Improve -. "次の実験" .-> Steady

    style Inject fill:#F44336,color:#fff
    style Improve fill:#4CAF50,color:#fff
```

| ツール | 概要 |
|--------|------|
| **Chaos Mesh** | K8s ネイティブのカオスエンジニアリング |
| **Litmus** | CNCF プロジェクト、K8s 向けカオス実験 |
| **Gremlin** | エンタープライズ向けカオスプラットフォーム |

---

## 学習リソース

### 書籍

| 書籍 | 対象 |
|------|------|
| 『SRE サイトリライアビリティエンジニアリング』（Google） | SRE の教科書 |
| 『Designing Data-Intensive Applications』 | システム設計の名著 |
| 『Team Topologies』 | Platform Engineering の組織論 |

### 認定資格

| 資格 | 発行 | 内容 |
|------|------|------|
| **CKA** | CNCF | Kubernetes 管理者 |
| **CKS** | CNCF | Kubernetes セキュリティ |
| **HashiCorp Terraform Associate** | HashiCorp | Terraform の基礎 |
| **AWS Solutions Architect** | AWS | クラウドアーキテクチャ |
| **GitHub Actions Certification** | GitHub | CI/CD パイプライン |

### オンラインリソース

| リソース | URL | 内容 |
|---------|-----|------|
| **CNCF Landscape** | [https://landscape.cncf.io](https://landscape.cncf.io) | クラウドネイティブツールの全体マップ |
| **DevOps Roadmap** | [https://roadmap.sh/devops](https://roadmap.sh/devops) | インタラクティブな学習ロードマップ |
| **KillerCoda** | [https://killercoda.com](https://killercoda.com) | ブラウザで K8s ハンズオン |
| **Terraform Learn** | [https://developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform) | 公式チュートリアル |

---

## まとめ：2026 年の DevOps エンジニアに必要なもの

```mermaid
flowchart TB
    Core["DevOps 2026"]

    Core --> Container["コンテナ<br/>Docker / K8s"]
    Core --> CICD["CI/CD<br/>GitHub Actions"]
    Core --> Infra["IaC<br/>Terraform / GitOps"]
    Core --> Obs["監視<br/>Prometheus /<br/>Grafana + Loki"]
    Core --> Sec["セキュリティ<br/>DevSecOps /<br/>Supply Chain"]
    Core --> AI["AI / ML<br/>MLOps / AIOps /<br/>LLM Infra"]
    Core --> Design["設計<br/>DR / カオス<br/>エンジニアリング"]
    Core --> Soft["ソフトスキル<br/>Platform Thinking /<br/>Developer Experience"]

    style Core fill:#2196F3,color:#fff
    style Container fill:#4CAF50,color:#fff
    style CICD fill:#4CAF50,color:#fff
    style Infra fill:#4CAF50,color:#fff
    style Obs fill:#FF9800,color:#fff
    style Sec fill:#F44336,color:#fff
    style AI fill:#9C27B0,color:#fff
    style Design fill:#9C27B0,color:#fff
    style Soft fill:#607D8B,color:#fff
```

> **DevOps で止まるな。** MLOps、AIOps、AI インフラ — そこに仕事、報酬、そして未来がある。

---

## 演習問題

[exercises/](./exercises/) ディレクトリに演習があります。

---

## お疲れさまでした！

ここまで学んだあなたは、2026 年の DevOps エンジニアとして必要なスキルの全体像を把握しています。
あとは **実践あるのみ** です。手を動かし、壊し、直し、AI を使い倒して、最速で成長しましょう。
