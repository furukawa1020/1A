# Method / 方法

## English

### Design

Paper 1A is a security middleware systems paper. We define PRESENCE Guard, implement runtime claim enforcement, and retain static auditing through `presence-audit`.

### Audit Procedure

The audit procedure is:

1. Write the target system use case.
2. Describe data signals, processing, retention, and identifiability.
3. Describe visibility to users, supporters, managers, teachers, employers, and evaluators.
4. List system-generated claims and assign claim severity.
5. List actions and controls.
6. Enforce or audit claim-flow, boundary analysis, surveillance transmutation patterns, PRESENCE score, and mitigations.
7. At runtime, call `requestClaim()` before rendering any state claim.

### 1B Validation Path

The 2 x 2 x 2 participant-facing scenario experiment is retained as the validation path for Paper 1B, not as the primary artifact of Paper 1A.

## 日本語

### デザイン

Paper 1Aはセキュリティミドルウェアのシステム論文である。PRESENCE Guardを定義し、runtime claim enforcementを実装し、`presence-audit`による静的監査も保持する。

### 監査手順

監査手順は次である。

1. 対象システムのuse caseを書く。
2. データ信号、処理場所、保持、識別可能性を書く。
3. ユーザー、支援者、管理者、教員、雇用者、評価者への可視性を書く。
4. システム生成claimを列挙し、claim severityを割り当てる。
5. actionとcontrolを書く。
6. claim-flow、boundary analysis、surveillance transmutation patterns、PRESENCE score、mitigationを強制または監査する。
7. 実行時には、状態claimを表示する前に必ず `requestClaim()` を呼ぶ。

### 1B妥当性検証への接続

2 x 2 x 2 の参加者向けシナリオ実験は、Paper 1Aの主成果物ではなく、Paper 1Bでの妥当性検証経路として残す。
