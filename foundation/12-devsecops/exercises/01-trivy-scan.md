# 演習 1: Trivy でコンテナイメージをスキャン

## 課題

phase2-docker の Docker イメージをビルドし、Trivy でセキュリティスキャンを実施してください。

### 要件

1. `application/webapp/phase2-docker/` のイメージをビルド
2. Trivy でフルスキャンを実行し、脆弱性の一覧を確認
3. HIGH / CRITICAL のみにフィルタして再スキャン
4. 結果を JSON 形式で出力
5. （発展）検出された脆弱性を 1 つ選び、修正方法を調査

### コマンドヒント

```bash
trivy image <image-name>
trivy image --severity HIGH,CRITICAL <image-name>
trivy image --format json --output results.json <image-name>
```

### 確認ポイント

- [ ] スキャン結果が表示されるか
- [ ] 脆弱性の重大度（CRITICAL / HIGH / MEDIUM / LOW）が分類されているか
- [ ] JSON 出力がファイルに保存されるか
