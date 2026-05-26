# PRESENCE Guard Security Requirements / セキュリティ要件

## English

| ID | Requirement | Implementation status |
| --- | --- | --- |
| SG-01 | Deny by default | Implemented in default policy and SDK/CLI decisions. |
| SG-02 | No network in core | SDK/core performs local decisions only. |
| SG-03 | Memory-safe core | JS/Python prototype; Rust core remains future hardening. |
| SG-04 | No dynamic eval | Policies are JSON/YAML data; no eval or plugins. |
| SG-05 | Policy signing | Prototype HMAC bundle signing in CLI. |
| SG-06 | Version pinning | Policy includes `policy_version`; app can pin local policy file. |
| SG-07 | Secure update path | Documented future requirement. |
| SG-08 | SBOM generation | Placeholder SBOM included for prototype. |
| SG-09 | Supply-chain hardening | CI example and no runtime dependencies in core path. |
| SG-10 | Secure development baseline | Tests and negative fixtures included; full SSDF mapping remains future work. |

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

