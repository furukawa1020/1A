# Preregistration Draft / 事前登録草案

## English

### Study

Study 1A is a within-subject 2 x 2 x 2 scenario-based factorial experiment.

### Research Question

When does presenteeism support become surveillance, evaluation, or imposed labeling as a function of processing location, third-party visibility, and output claim?

### Factors

| Factor | Levels |
| --- | --- |
| Processing Location | Cloud, Local |
| Third-party Visibility | Manager-visible, Self-only |
| Output Claim | Assertive Label, Non-assertive Cue |

### Primary Outcomes

- MFS: Monitoring Feeling Score.
- LIS: Label Imposition Score.
- SOUS: Self-Observation Utility Score.
- WU: Willingness to Use.
- WD: Willingness to Disclose.

### Manipulation Checks

- `manip_cloud`
- `manip_visibility`
- `manip_assertive`
- `manip_self_only`

### Exclusion Rule

Exclude from the primary analysis participants who fail five or more of the eight condition-level manipulation checks. Report sensitivity analyses with and without exclusions.

### Main Analysis

Fit mixed models with participant random intercepts:

```text
score ~ Processing * Visibility * Output + (1 | participant)
```

Use non-parametric robustness checks if model fit is unstable.

### Non-Inferiority

Evaluate SOUS non-inferiority for C8:

```text
SOUS(C8) >= SOUS(C7) - 0.5
SOUS(C8) >= SOUS(C1) - 0.5
```

### Claims Not Tested

This study does not test whether the system detects presenteeism, diagnoses stress, improves mental health, or increases productivity.

## 日本語

### 研究

Study 1A は、2 x 2 x 2 の被験者内シナリオベース因子実験である。

### 研究問い

プレゼンティーズム支援は、処理場所、第三者可視性、出力主張の違いによって、いつ監視・評価・ラベル押し付けへ転化するのか。

### 因子

| 因子 | 水準 |
| --- | --- |
| 処理場所 | Cloud, Local |
| 第三者可視性 | Manager-visible, Self-only |
| 出力主張 | Assertive Label, Non-assertive Cue |

### 主要アウトカム

- MFS: Monitoring Feeling Score。
- LIS: Label Imposition Score。
- SOUS: Self-Observation Utility Score。
- WU: Willingness to Use。
- WD: Willingness to Disclose。

### 操作チェック

- `manip_cloud`
- `manip_visibility`
- `manip_assertive`
- `manip_self_only`

### 除外基準

8条件中5条件以上で条件レベルの操作チェックに失敗した参加者は、主分析から除外する。除外あり・なしの感度分析を両方報告する。

### 主分析

参加者ランダム切片を持つ混合モデルを当てはめる。

```text
score ~ Processing * Visibility * Output + (1 | participant)
```

モデル当てはめが不安定な場合は、ノンパラメトリックな頑健性確認を行う。

### 非劣性

C8のSOUS非劣性を評価する。

```text
SOUS(C8) >= SOUS(C7) - 0.5
SOUS(C8) >= SOUS(C1) - 0.5
```

### 検証しない主張

この研究は、システムがプレゼンティーズムを検出できるか、ストレスを診断できるか、メンタルヘルスを改善できるか、生産性を高められるかを検証しない。

