# PRESENCE Guard Threat Model / PRESENCE Guard脅威モデル

## English

PRESENCE Guard is itself a security component. Its threat model must include attacks against the guard, policy, logs, and integration path.

| ID | Threat | Description |
| --- | --- | --- |
| T1 | Policy tampering | An attacker or developer weakens the policy to allow dangerous claims. |
| T2 | Bypass | The app renders claims directly without calling PRESENCE Guard. |
| T3 | Misclassification | A dangerous claim is labeled as low severity. |
| T4 | Prompt / LLM injection | Generated text evades claim classification. |
| T5 | Report leakage | Audit reports expose sensitive system details or examples. |
| T6 | Supply-chain attack | SDK, CLI, or dependencies are modified. |
| T7 | Malicious policy update | A policy update relaxes enforcement. |
| T8 | Log leakage | Audit or runtime logs reveal user state. |
| T9 | Denial of service | Guard failure prevents support UI from operating. |
| T10 | False sense of security | Teams treat PRESENCE adoption as proof of safety. |

## 日本語

PRESENCE Guard自身もセキュリティ部品である。脅威モデルには、Guard、policy、log、統合経路への攻撃を含めなければならない。

| ID | 脅威 | 内容 |
| --- | --- | --- |
| T1 | Policy tampering | 攻撃者または開発者がpolicyを弱め、危険claimを許可する。 |
| T2 | Bypass | アプリがPRESENCE Guardを呼ばずにclaimを直接表示する。 |
| T3 | Misclassification | 危険なclaimが低severityとして分類される。 |
| T4 | Prompt / LLM injection | 生成文がclaim分類をすり抜ける。 |
| T5 | Report leakage | 監査レポートが機微なシステム詳細や例文を漏らす。 |
| T6 | Supply-chain attack | SDK、CLI、依存関係が改ざんされる。 |
| T7 | Malicious policy update | policy更新によりenforcementが緩む。 |
| T8 | Log leakage | audit logやruntime logがユーザー状態を漏らす。 |
| T9 | Denial of service | Guard故障により支援UIが動作しなくなる。 |
| T10 | False sense of security | PRESENCE導入だけで安全だと誤認される。 |

