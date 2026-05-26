# PRESENCE Guard Security / PRESENCE Guardのセキュリティ

## English

PRESENCE Guard is a security component and must be analyzed as one. The design follows deny-by-default enforcement, no network in the decision core, no dynamic policy evaluation, local policy pinning, prototype policy signing, and dependency minimization.

The main risks are policy tampering, bypass, misclassification, prompt/LLM injection, report leakage, supply-chain compromise, malicious policy update, log leakage, denial of service, and false sense of security.

In the implementation, these risks are addressed through a deny-by-default policy, signed policy bundle prototype, policy version pinning, no-network Rust/C decision core, no dynamic evaluation, invalid input rejection, fuzz negative tests, bypass tests for direct claim rendering, dependency-surface checks, and SBOM documentation. The browser demo was changed so that condition claims are not rendered directly; proposed state claims become user-visible only after a Guard decision.

## 日本語

PRESENCE Guardはセキュリティ部品であり、それ自体を分析対象にしなければならない。設計では、deny-by-default enforcement、decision coreのno network、dynamic policy evaluationの禁止、local policy pinning、prototype policy signing、依存の最小化を採用する。

主なリスクは、policy tampering、bypass、misclassification、prompt/LLM injection、report leakage、supply-chain compromise、malicious policy update、log leakage、denial of service、false sense of securityである。

実装では、deny-by-default policy、署名付きpolicy bundle prototype、policy version pinning、no-network Rust/C decision core、dynamic evaluation禁止、invalid input rejection、fuzz negative test、直接claim描画に対するbypass test、dependency-surface check、SBOM文書化によってこれらのリスクへ対応する。ブラウザdemoでは、condition claimを直接表示せず、提案された状態claimはGuard decision後にのみ利用者へ見える。

## 日本語

PRESENCE Guardはセキュリティ部品であり、それ自体を分析対象にしなければならない。設計では、deny-by-default enforcement、decision coreのno network、dynamic policy evaluation禁止、ローカルpolicy pinning、プロトタイプpolicy署名、依存最小化を採用する。

主要リスクは、policy tampering、bypass、misclassification、prompt/LLM injection、report leakage、supply-chain compromise、malicious policy update、log leakage、denial of service、false sense of securityである。
