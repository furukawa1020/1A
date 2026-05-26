# Analysis Plan

## Main Models

Use linear mixed models for the primary analysis:

```text
MFS  ~ Processing * Visibility * Output + (1 | participant)
LIS  ~ Processing * Visibility * Output + (1 | participant)
SOUS ~ Processing * Visibility * Output + (1 | participant)
WU   ~ Processing * Visibility * Output + (1 | participant)
WD   ~ Processing * Visibility * Output + (1 | participant)
```

If the sample is too small or model assumptions are weak, use non-parametric Friedman/Wilcoxon analyses as robustness checks.

## Hypotheses

- H1: Cloud increases MFS and privacy concern relative to Local.
- H2: Manager-visible increases MFS and decreases WU/WD relative to Self-only.
- H3: Assertive labels increase LIS relative to Non-assertive cues.
- H4: C8 has low MFS/LIS and does not meaningfully reduce SOUS.
- H5: Manager-visible and Assertive Label interact, increasing LIS and MFS.

## Manipulation Checks

Expected:

- Cloud > Local on `manip_cloud`.
- Manager-visible > Self-only on `manip_visibility`.
- Assertive > Non-assertive on `manip_assertive`.
- Self-only > Manager-visible on `manip_self_only`.

Participants who fail at least five of eight condition-level checks should be excluded from the primary analysis. Analyses should be reported both before and after exclusion.

## Reliability

For each scale:

- Cronbach's alpha.
- McDonald's omega or a clearly labeled one-factor approximation when exact omega tooling is unavailable.

Minimum target:

```text
alpha or omega >= .70
```

If reliability is below this threshold, treat the scale-score interpretation cautiously and report item-level or exploratory analyses.

## Non-Inferiority

SOUS should be analyzed as non-inferiority, not superiority:

```text
SOUS(C8) >= SOUS(C7) - 0.5
SOUS(C8) >= SOUS(C1) - 0.5
```

The provisional margin is 0.5 on a 7-point scale.

