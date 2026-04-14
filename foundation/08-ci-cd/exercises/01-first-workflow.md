# 演習 1: 初めてのワークフロー

## 課題

以下の要件を満たす GitHub Actions ワークフローを作成してください。

### 要件

1. `main` ブランチへの push と PR 時にトリガーされる
2. Python 3.12 環境をセットアップする
3. `requirements.txt` から依存関係をインストールする
4. `pytest` でテストを実行する
5. テスト成功後に Docker イメージをビルドする

### ヒント

- ファイルは `.github/workflows/ci.yml` に配置
- `needs` キーワードで Job 間の依存関係を定義
- `actions/checkout@v4` と `actions/setup-python@v5` を使用

### 確認ポイント

- [ ] ワークフローが正しい YAML 構文で書かれているか
- [ ] Job 間の依存関係が正しく設定されているか
- [ ] 成功・失敗の両方のケースを考慮しているか

答えは [answers/](../answers/) で確認できます。
