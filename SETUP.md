# 環境セットアップ（Mac M4 / Apple Silicon）

このリポジトリで学ぶために必要なツールをインストールします。
所要時間の目安: **15〜30分**

---

## インストールするもの

| ツール | 用途 |
|---|---|
| Homebrew | Mac のパッケージマネージャー（他のツールの前提） |
| Docker Desktop | コンテナの実行環境 |
| kubectl | Kubernetes を操作する CLI |
| kind | Docker 上で動くローカル Kubernetes クラスタ |
| Python 3 | サンプルアプリ（Flask）の実行環境 |

---

## ステップ 1: Homebrew のインストール

ターミナルを開いて以下を実行します。

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

インストール後、指示に従って PATH を設定します（Apple Silicon の場合は `/opt/homebrew/bin` を PATH に追加）。

**確認:**
```bash
brew --version
# 例: Homebrew 4.x.x
```

---

## ステップ 2: Docker Desktop のインストール

Homebrew でインストールします。

```bash
brew install --cask docker
```

インストール後、**アプリケーション > Docker** を起動して、メニューバーにクジラのアイコンが表示されるまで待ちます。

**確認:**
```bash
docker --version
# 例: Docker version 27.x.x

docker run hello-world
# "Hello from Docker!" と表示されれば成功
```

> **補足:** Docker Desktop を初回起動すると、利用規約への同意が求められます。個人・学習用途は無料で使えます。

---

## ステップ 3: kubectl のインストール

```bash
brew install kubectl
```

**確認:**
```bash
kubectl version --client
# 例: Client Version: v1.xx.x
```

---

## ステップ 4: kind のインストール

kind（Kubernetes IN Docker）は Docker の中で Kubernetes クラスタを動かすツールです。

```bash
brew install kind
```

**確認:**
```bash
kind version
# 例: kind v0.xx.x go1.xx.x darwin/arm64
```

---

## ステップ 5: ローカル Kubernetes クラスタの作成

```bash
kind create cluster --name handson
```

クラスタが作成されたら、kubectl で接続できるか確認します。

```bash
kubectl get nodes
# NAME                    STATUS   ROLES           AGE   VERSION
# handson-control-plane   Ready    control-plane   ...   v1.xx.x
```

`STATUS` が `Ready` になれば成功です。

---

## ステップ 6: Python 3 のインストール（任意）

application 編で使います。まだ入っていない場合はインストールしてください。

```bash
brew install python
```

**確認:**
```bash
python3 --version
# 例: Python 3.12.x
```

---

## セットアップ完了チェックリスト

すべて `✓` になればスタートできます。

```
[ ] brew --version     → バージョンが表示される
[ ] docker run hello-world → "Hello from Docker!" が表示される
[ ] kubectl version --client → バージョンが表示される
[ ] kind version       → バージョンが表示される
[ ] kubectl get nodes  → handson-control-plane が Ready になっている
```

---

## クラスタの削除（学習後・不要になったとき）

```bash
kind delete cluster --name handson
```

---

## よくある問題

### `docker: command not found` が出る
→ Docker Desktop が起動していない。アプリを起動してから再試行。

### `kind create cluster` が失敗する
→ Docker Desktop が動いているか確認（`docker ps` でエラーが出なければOK）。

### `kubectl get nodes` で `NotReady` が続く
→ クラスタの起動に1〜2分かかることがあります。少し待ってから再実行。

---

準備ができたら [foundation/01-what-is-docker/README.md](./foundation/01-what-is-docker/README.md) から始めましょう。
