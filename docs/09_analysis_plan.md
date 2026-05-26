# Analysis Plan / 分析計画

## English

### Main Models

Use linear mixed models for the primary analysis:

```text
MFS  ~ Processing * Visibility * Output + (1 | participant)
LIS  ~ Processing * Visibility * Output + (1 | participant)
SOUS ~ Processing * Visibility * Output + (1 | participant)
WU   ~ Processing * Visibility * Output + (1 | participant)
WD   ~ Processing * Visibility * Output + (1 | participant)
```

If the sample is too small or model assumptions are weak, use non-parametric Friedman/Wilcoxon analyses as robustness checks.

### Hypotheses

- H1: Cloud increases MFS and privacy concern relative to Local.
- H2: Manager-visible increases MFS and decreases WU/WD relative to Self-only.
- H3: Assertive labels increase LIS relative to Non-assertive cues.
- H4: C8 has low MFS/LIS and does not meaningfully reduce SOUS.
- H5: Manager-visible and Assertive Label interact, increasing LIS and MFS.

### Manipulation Checks

Expected:

- Cloud > Local on `manip_cloud`.
- Manager-visible > Self-only on `manip_visibility`.
- Assertive > Non-assertive on `manip_assertive`.
- Self-only > Manager-visible on `manip_self_only`.

Participants who fail at least five of eight condition-level checks should be excluded from the primary analysis. Analyses should be reported both before and after exclusion.

### Reliability

For each scale:

- Cronbach's alpha.
- McDonald's omega or a clearly labeled one-factor approximation when exact omega tooling is unavailable.

Minimum target:

```text
alpha or omega >= .70
```

If reliability is below this threshold, treat the scale-score interpretation cautiously and report item-level or exploratory analyses.

### Non-Inferiority

SOUS should be analyzed as non-inferiority, not superiority:

```text
SOUS(C8) >= SOUS(C7) - 0.5
SOUS(C8) >= SOUS(C1) - 0.5
```

The provisional margin is 0.5 on a 7-point scale.

### Audit Outputs

Before participant analysis, compute:

```text
python analysis/scripts/08_compute_ess.py
python analysis/scripts/09_policy_audit.py
```

These outputs are not participant outcomes. They document the design exposure and policy-relevant findings for each condition.

## 日本語

### 主分析モデル

主分析では線形混合モデルを用いる。

```text
MFS  ~ Processing * Visibility * Output + (1 | participant)
LIS  ~ Processing * Visibility * Output + (1 | participant)
SOUS ~ Processing * Visibility * Output + (1 | participant)
WU   ~ Processing * Visibility * Output + (1 | participant)
WD   ~ Processing * Visibility * Output + (1 | participant)
```

サンプルが小さい場合やモデル仮定が弱い場合は、頑健性確認としてノンパラメトリックなFriedman/Wilcoxon分析を用いる。

### 仮説

- H1: Cloud は Local より MFS とプライバシー懸念を高める。
- H2: Manager-visible は Self-only より MFS を高め、WU/WD を下げる。
- H3: Assertive label は Non-assertive cue より LIS を高める。
- H4: C8 は MFS/LIS が低く、SOUS を大きく損なわない。
- H5: Manager-visible と Assertive Label は交互作用し、LIS と MFS を高める。

### 操作チェック

期待される結果は次である。

- `manip_cloud` で Cloud > Local。
- `manip_visibility` で Manager-visible > Self-only。
- `manip_assertive` で Assertive > Non-assertive。
- `manip_self_only` で Self-only > Manager-visible。

8条件中5条件以上で条件レベルの操作チェックに失敗した参加者は、主分析から除外する。除外前後の分析を両方報告する。

### 信頼性

各尺度について次を計算する。

- Cronbach's alpha。
- McDonald's omega。ただし、正確なomega計算環境がない場合は、明示的にラベル付けした一因子近似を用いる。

最低目標は次である。

```text
alpha or omega >= .70
```

信頼性がこの閾値を下回る場合、合成得点としての解釈は慎重に扱い、項目別分析または探索的分析として報告する。

### 非劣性分析

SOUSは優越性ではなく非劣性として分析する。

```text
SOUS(C8) >= SOUS(C7) - 0.5
SOUS(C8) >= SOUS(C1) - 0.5
```

暫定マージンは7件法で0.5とする。

### 監査出力

参加者分析の前に次を計算する。

```text
python analysis/scripts/08_compute_ess.py
python analysis/scripts/09_policy_audit.py
```

これらの出力は参加者アウトカムではない。各条件の設計曝露とポリシー上重要な所見を記録するものである。
