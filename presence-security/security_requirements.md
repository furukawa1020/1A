# PRESENCE Guard Security Requirements / セキュリティ要件

## English

| ID | Requirement | Implementation status |
| --- | --- | --- |
| SG-01 | Deny by default | Implemented in default policy and SDK/CLI decisions. |
| SG-02 | No network in core | Rust/C decision core is scanned for network APIs; browser policy loading is outside the core. |
| SG-03 | Memory-safe core | Rust no-network core implemented with unit tests; C ABI sketch remains a thin embedded interface. |
| SG-04 | No dynamic eval | Policies are JSON/YAML data; no eval or plugins. |
| SG-05 | Policy signing | Prototype HMAC bundle signing in CLI. |
| SG-06 | Version pinning | Policy includes `policy_version`; app can pin local policy file. |
| SG-07 | Secure update path | Documented future requirement. |
| SG-08 | SBOM generation | Prototype CycloneDX SBOM included; dependency surface checked in evaluation. |
| SG-09 | Supply-chain hardening | CI gate, static scanner, no runtime dependencies in core path, and signed policy prototype. |
| SG-10 | Secure development baseline | Misuse fixtures, mutation tests, fuzz negative tests, bypass tests, static scan, and Rust unit tests included; full SSDF mapping remains future work. |

## 日本語

| ID | 要件 | 実装状況 |
| --- | --- | --- |
| SG-01 | Deny by default | 標準policyとSDK/CLI判定に実装済み。 |
| SG-02 | No network in core | Rust/C decision coreをnetwork API scanの対象にする。browser policy loadingはcore外。 |
| SG-03 | Memory-safe core | Rust no-network coreをunit test付きで実装済み。C ABI sketchはembedded向けの薄いinterface。 |
| SG-04 | No dynamic eval | policyはJSON/YAML dataであり、evalやpluginを使わない。 |
| SG-05 | Policy signing | CLIに研究用HMAC policy bundle署名を実装済み。 |
| SG-06 | Version pinning | policyに`policy_version`を含め、アプリはlocal policyを固定できる。 |
| SG-07 | Secure update path | 今後の要件として文書化。 |
| SG-08 | SBOM generation | Prototype CycloneDX SBOMを含め、evaluationでdependency surfaceを確認する。 |
| SG-09 | Supply-chain hardening | CI gate、static scanner、core pathのruntime依存なし、signed policy prototypeを含む。 |
| SG-10 | Secure development baseline | misuse fixture、mutation test、fuzz negative test、bypass test、static scan、Rust unit testを含む。完全なSSDF対応表は今後の課題。 |

## 日本語

| ID | 要件 | 実装状態 |
| --- | --- | --- |
| SG-01 | Deny by default | 標準policyとSDK/CLI判定に実装済み。 |
| SG-02 | No network in core | SDK/coreはローカル判定のみを行う。 |
| SG-03 | Memory-safe core | 現在はJS/Pythonプロトタイプ。Rust coreは今後のhardening。 |
| SG-04 | No dynamic eval | policyはJSON/YAMLデータであり、evalやpluginを使わない。 |
| SG-05 | Policy signing | CLIに研究用HMAC policy bundle署名を実装。 |
| SG-06 | Version pinning | policyに`policy_version`を含め、アプリはローカルpolicyを固定できる。 |
| SG-07 | Secure update path | 今後の要件として文書化。 |
| SG-08 | SBOM generation | プロトタイプ用SBOM placeholderを含める。 |
| SG-09 | Supply-chain hardening | CI例とcore pathのruntime依存なしで対応。 |
| SG-10 | Secure development baseline | テストとnegative fixtureを含む。完全なSSDF対応表は今後。 |
