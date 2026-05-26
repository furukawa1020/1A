# PRESENCE Audit Report: local_assertive_app

- Risk level: **MEDIUM**
- PRESENCE score: **12**

## Detected Patterns
- `P2` Self-Observation-to-Self-Surveillance
- `P3` Cue-to-Claim Escalation
- `P9` Context Collapse
- `P12` Non-Diagnostic Tool-to-Quasi-Diagnosis

## High-Risk Claims
- `C4` psychological: High stress tendency

## Claim-Flow
- `c1` keyboard_activity, mouse_activity -> derived_feature -> psychological -> High stress tendency -> C4 -> user_notification, recommended_break -> user

## Boundary Analysis
- Data boundary: `local`
- Authority boundary: `self_only`
- Interpretation boundary: `system_label`

## Boundary Violations
- system claim narrows or overrides user interpretation

## Recommended Mitigations
- cap feedback frequency
- avoid comparative scores
- make reflection user-controlled
- cap claims at C2 pattern-level cues
- show uncertainty and context limits
- preserve user interpretation space
- avoid single-state labels
- ban medical/psychological labels unless clinically validated and ethically governed
