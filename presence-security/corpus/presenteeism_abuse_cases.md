# Presenteeism-Specific Abuse Case Corpus

## English

These abuse cases are used to keep PRESENCE Guard specific to presenteeism support instead of a generic privacy linter.

### Abuse Case A: Well-being Dashboard Drift

A self-only reflection tool is updated into a weekly manager dashboard.

PRESENCE should detect:

- `self_only` to `manager_visible`
- `session` cue to `weekly_summary`
- `C2` cue to `C5` productivity label

### Abuse Case B: Health Signal to Productivity Claim

Heart rate, input intervals, or idle time become "reduced work efficiency."

PRESENCE should deny:

- health or condition signal to productivity claim

### Abuse Case C: Non-Diagnostic Quasi-Diagnosis

A product says it is not diagnostic, but outputs "high stress", "danger", or "needs attention."

PRESENCE should deny or rewrite:

- non-diagnostic system to C4 psychological claim
- non-diagnostic system to C6 administrative claim

### Abuse Case D: Presenteeism Coercion

A voluntary reflection tool becomes expected or mandatory in class or work.

PRESENCE should detect:

- voluntary self-observation to mandatory monitoring
- missing exit/refusal possibility

### Abuse Case E: Context Collapse

User context such as challenge, temporary fatigue, or pre-task tension is collapsed into a single negative label.

PRESENCE should detect:

- ambiguous state to assertive psychological/productivity claim

## 日本語

これらのabuse caseは、PRESENCE Guardを汎用privacy linterではなく、プレゼンティーズム支援に特化した仕組みに保つためのcorpusである。

### Abuse Case A: Well-being Dashboard Drift

本人だけのreflection toolが、週次manager dashboardへ更新される。

PRESENCEが検出すべきこと:

- `self_only` から `manager_visible` への変化
- `session` cueから `weekly_summary` への変化
- `C2` cueから `C5` productivity labelへの変化

### Abuse Case B: Health Signal to Productivity Claim

心拍、入力間隔、無操作時間が「作業効率低下」に変換される。

PRESENCEがdenyすべきこと:

- health / condition signalからproductivity claimへの変換

### Abuse Case C: Non-Diagnostic Quasi-Diagnosis

製品は診断ではないと言いながら、「高ストレス」「危険」「要対応」を出す。

PRESENCEがdenyまたはrewriteすべきこと:

- non-diagnostic systemからC4 psychological claimへの変換
- non-diagnostic systemからC6 administrative claimへの変換

### Abuse Case D: Presenteeism Coercion

任意のreflection toolが、授業や職場で期待または義務になる。

PRESENCEが検出すべきこと:

- voluntary self-observationからmandatory monitoringへの変化
- exit/refusal possibilityの欠落

### Abuse Case E: Context Collapse

挑戦、一時的疲れ、作業前の緊張といった本人文脈が、単一の否定的labelへ潰される。

PRESENCEが検出すべきこと:

- ambiguous stateからassertive psychological/productivity claimへの変換
