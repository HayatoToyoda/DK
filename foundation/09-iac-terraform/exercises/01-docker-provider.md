# 演習 1: Docker プロバイダで Terraform を体験

## 課題

Terraform の Docker プロバイダを使って、以下のインフラを構築してください。

### 要件

1. `nginx:alpine` イメージを pull する
2. nginx コンテナを起動し、ホストのポート `8888` にマッピングする
3. コンテナ名を `my-terraform-nginx` にする
4. `output` でコンテナ ID と接続 URL を出力する

### ヒント

- `resource "docker_image"` と `resource "docker_container"` を使う
- `ports` ブロックで `internal` と `external` を指定
- `terraform plan` で事前確認してから `terraform apply`

### 確認ポイント

- [ ] `terraform plan` が差分を正しく表示するか
- [ ] `curl localhost:8888` で nginx のレスポンスが返るか
- [ ] `terraform destroy` で正しくクリーンアップされるか

答えは [answers/](../answers/) で確認できます。
