# Public Reference Profiles

## English

The Paper 1A benchmark uses reference profiles derived from public feature descriptions of workplace health management, employee well-being, stress-check, and presenteeism-visualization services.

This is not a vulnerability assessment. The benchmark does not log into real services, scrape private screens, probe APIs, or claim that specific vendors are unsafe. It abstracts feature patterns into reproducible YAML profiles:

- `presenteeism_survey_dashboard`
- `employee_app_manager_dashboard`
- `health_data_labor_risk_dashboard`
- `stress_check_high_risk_extraction`
- `productivity_loss_visualization`
- `noticer_local_low_risk`

Run:

```powershell
python presence-bench\run_benchmark.py --output presence-bench\reports\benchmark_report.md
```

The benchmark demonstrates whether PRESENCE detects claim-flow risks in realistic design patterns, while preserving ethical distance from vendor-specific claims.

## 日本語

Paper 1Aのbenchmarkでは、健康経営、従業員well-being、stress check、presenteeism可視化系serviceの公開機能説明から抽象化したreference profileを用いる。

これは脆弱性診断ではない。benchmarkは実serviceへloginせず、private screenをscrapeせず、API探索を行わず、特定vendorが危険であるとは主張しない。公開機能パターンを再現可能なYAML profileへ抽象化する。

- `presenteeism_survey_dashboard`
- `employee_app_manager_dashboard`
- `health_data_labor_risk_dashboard`
- `stress_check_high_risk_extraction`
- `productivity_loss_visualization`
- `noticer_local_low_risk`

実行:

```powershell
python presence-bench\run_benchmark.py --output presence-bench\reports\benchmark_report.md
```

このbenchmarkは、現実的な設計パターンにおいてPRESENCEがclaim-flow riskを検出できるかを示す。同時に、vendor-specific claimから倫理的距離を保つ。
