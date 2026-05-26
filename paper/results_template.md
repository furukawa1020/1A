# Results Template / 結果テンプレート

## English

### Tool Evaluation

Report:

- P1-P12 misuse-case detection results.
- Policy mutation test results.
- Runtime Guard fixture decisions.
- Static scanner results for app/SDK and positive bypass fixture.
- Public-information reference benchmark results.
- Third-party quickstart result.
- Demo HTTP/screenshot smoke-test result.
- WASM build, TypeScript typecheck, Rust tests, C embedded demo, and minimal logging checks.

### Benchmark Profiles

Report six profiles:

- `presenteeism_survey_dashboard`
- `employee_app_manager_dashboard`
- `health_data_labor_risk_dashboard`
- `stress_check_high_risk_extraction`
- `productivity_loss_visualization`
- `noticer_local_low_risk`

State that the profiles are derived from public feature descriptions and are not vendor-specific risk claims.

### Human Validation Path

Paper 1B, not Paper 1A, will report manipulation checks, reliability, mixed models, and non-inferiority for MFS, LIS, SOUS, WU, and WD.

## 日本語

### Tool Evaluation

次を報告する。

- P1-P12 misuse-case detection結果。
- Policy mutation test結果。
- Runtime Guard fixture decision。
- app/SDKとpositive bypass fixtureに対するstatic scanner結果。
- Public-information reference benchmark結果。
- Third-party quickstart結果。
- Demo HTTP/screenshot smoke-test結果。
- WASM build、TypeScript typecheck、Rust test、C embedded demo、minimal logging check。

### Benchmark Profiles

6つのprofileを報告する。

- `presenteeism_survey_dashboard`
- `employee_app_manager_dashboard`
- `health_data_labor_risk_dashboard`
- `stress_check_high_risk_extraction`
- `productivity_loss_visualization`
- `noticer_local_low_risk`

これらのprofileは公開機能説明から抽象化したものであり、特定vendorに対するrisk claimではないと明記する。

### Human Validation Path

MFS、LIS、SOUS、WU、WDのmanipulation check、reliability、mixed model、non-inferiorityはPaper 1AではなくPaper 1Bで報告する。

## 日本語

### 操作チェック

次を報告する。

- クラウド処理の知覚で Cloud > Local となったか。
- 第三者可視性の知覚で Manager-visible > Self-only となったか。
- 断定性の知覚で Assertive > Non-assertive となったか。
- 本人のみ保持の知覚で Self-only > Manager-visible となったか。

### 信頼性

MFS、LIS、SOUS、WU、WDについて、alpha と omega/近似omega を報告する。

### 主効果と交互作用

次について混合モデルの結果を報告する。

- MFS。
- LIS。
- SOUS。
- WU。
- WD。

### 非劣性

暫定マージン0.5のもとで、C8がC7およびC1に対してSOUSで非劣性かを報告する。

### ESS

ESSは参加者評価アウトカムではなく、設計監査の文脈として報告する。
