# 演習 1: Prometheus + Grafana で監視を体験

## 課題

kind クラスタに Prometheus + Grafana をインストールし、ダッシュボードを構築してください。

### 要件

1. Helm を使って `kube-prometheus-stack` をインストール
2. Grafana にログインし、K8s クラスタのダッシュボードを表示
3. 以下の PromQL クエリを Grafana の Explore で実行し、結果を確認
   - ノードの CPU 使用率
   - ノードのメモリ使用量
   - Pod 数の推移

### PromQL ヒント

```promql
# CPU使用率
100 - (avg by(instance)(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# メモリ使用量
node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes

# Pod数
count(kube_pod_info)
```

### 発展課題

4. Grafana の Explore で **Loki** データソースを選択し、以下の LogQL を試す

```logql
{namespace="monitoring"}
```

### トラブルシューティング

- kind でリソースが足りない場合: `--set prometheus.prometheusSpec.resources.requests.memory=256Mi` で制限を下げる
- Grafana にアクセスできない場合: `kubectl get pods -n monitoring` で Pod の状態を確認

### 確認ポイント

- [ ] Grafana にログインできるか
- [ ] 組み込みダッシュボードが表示されるか
- [ ] PromQL クエリの結果がグラフで表示されるか
- [ ] （発展）Loki のログが Explore で表示されるか

答えは [answers/](../answers/) で確認できます。
