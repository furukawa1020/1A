# Factorial Design

Study 1A uses a 2 x 2 x 2 within-subject factorial scenario experiment.

| Factor | Level 1 | Level 2 |
| --- | --- | --- |
| Processing Location | Cloud | Local |
| Third-party Visibility | Manager-visible | Self-only |
| Output Claim | Assertive Label | Non-assertive Cue |

## Conditions

| ID | Processing | Visibility | Output |
| --- | --- | --- | --- |
| C1 | Cloud | Manager-visible | Assertive |
| C2 | Cloud | Manager-visible | Non-assertive |
| C3 | Cloud | Self-only | Assertive |
| C4 | Cloud | Self-only | Non-assertive |
| C5 | Local | Manager-visible | Assertive |
| C6 | Local | Manager-visible | Non-assertive |
| C7 | Local | Self-only | Assertive |
| C8 | Local | Self-only | Non-assertive |

The proposed lower-risk configuration is C8. The high-risk reference configuration is C1.

## Order

The app assigns a balanced Latin-square-like sequence based on the participant ID. The participant ID is generated randomly by default, so participants are distributed across order rows while preserving logged reproducibility.

The exported response includes:

- `condition_order`
- `condition_sequence`
- `order_strategy`

