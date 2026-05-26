# Preregistration Draft

## Study

Study 1A is a within-subject 2 x 2 x 2 scenario-based factorial experiment.

## Research Question

When does presenteeism support become surveillance, evaluation, or imposed labeling as a function of processing location, third-party visibility, and output claim?

## Factors

| Factor | Levels |
| --- | --- |
| Processing Location | Cloud, Local |
| Third-party Visibility | Manager-visible, Self-only |
| Output Claim | Assertive Label, Non-assertive Cue |

## Primary Outcomes

- MFS: Monitoring Feeling Score.
- LIS: Label Imposition Score.
- SOUS: Self-Observation Utility Score.
- WU: Willingness to Use.
- WD: Willingness to Disclose.

## Manipulation Checks

- `manip_cloud`
- `manip_visibility`
- `manip_assertive`
- `manip_self_only`

## Exclusion Rule

Exclude from the primary analysis participants who fail five or more of the eight condition-level manipulation checks. Report sensitivity analyses with and without exclusions.

## Main Analysis

Fit mixed models with participant random intercepts:

```text
score ~ Processing * Visibility * Output + (1 | participant)
```

Use non-parametric robustness checks if model fit is unstable.

## Non-Inferiority

Evaluate SOUS non-inferiority for C8:

```text
SOUS(C8) >= SOUS(C7) - 0.5
SOUS(C8) >= SOUS(C1) - 0.5
```

## Claims Not Tested

This study does not test whether the system detects presenteeism, diagnoses stress, improves mental health, or increases productivity.

