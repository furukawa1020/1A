# presence-bench

## English

`presence-bench` is a public-information benchmark for PRESENCE Guard.

It does not audit, attack, or rank real vendors. Instead, it abstracts feature patterns visible in public documentation for workplace health management, employee well-being, stress-check, and presenteeism-visualization services into reference profiles.

The benchmark asks whether PRESENCE Guard can detect claim-flow risks in those profiles:

- health or stress signal to productivity claim
- self-observation claim to manager/organization visibility
- temporary or survey state to persistent records
- psychological label or high-risk extraction
- exportable claim-level records
- economic/productivity valuation of health state

Run:

```powershell
python presence-bench\run_benchmark.py --output presence-bench\reports\benchmark_report.md
```

## 日本語

`presence-bench` は、PRESENCE Guardのための公開情報ベースのベンチマークである。

これは実在ベンダーを監査・攻撃・順位付けするものではない。健康経営、従業員ウェルビーイング、ストレスチェック、プレゼンティーズム可視化系サービスの公開資料に見られる機能パターンを抽象化し、reference profileとして再構成する。

ベンチマークで確認するclaim-flow riskは次の通りである。

- health/stress signalからproductivity claimへの変換
- self-observation claimからmanager/organization visibilityへの越境
- 一時状態やsurvey状態のpersistent record化
- psychological labelやhigh-risk extraction
- claim-level recordのexport可能性
- health stateのeconomic/productivity valuation

実行:

```powershell
python presence-bench\run_benchmark.py --output presence-bench\reports\benchmark_report.md
```
