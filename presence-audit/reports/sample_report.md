# PRESENCE Audit Report: workplace_wellbeing_dashboard

- Risk level: **CRITICAL**
- PRESENCE score: **31**

## Detected Patterns
- `P1` Support-to-Assessment
- `P2` Self-Observation-to-Self-Surveillance
- `P3` Cue-to-Claim Escalation
- `P5` Temporary State-to-Persistent Record
- `P6` Health Signal-to-Productivity Label
- `P7` Care-to-Compliance
- `P8` Voluntary Reflection-to-Mandatory Monitoring
- `P9` Context Collapse
- `P10` Ambiguous State-to-Actionable Flag
- `P11` Individual Support-to-Group Benchmarking
- `P12` Non-Diagnostic Tool-to-Quasi-Diagnosis

## High-Risk Claims
- `C4` psychological: High stress detected
- `C5` productivity: Reduced work efficiency

## Claim-Flow
- `c1` heart_rate, keyboard_activity -> derived_feature -> psychological -> High stress detected -> C4 -> user_notification, manager_report, weekly_team_summary -> user, manager, employer, evaluator
- `c2` keyboard_activity -> derived_feature -> productivity -> Reduced work efficiency -> C5 -> user_notification, manager_report, weekly_team_summary -> user, manager, employer, evaluator

## Boundary Analysis
- Data boundary: `cloud`
- Authority boundary: `evaluator_visible`
- Interpretation boundary: `administrative_flag`

## Boundary Violations
- data crosses from local context into cloud processing
- self-observation claim crosses into authority-visible boundary
- system claim narrows or overrides user interpretation
- temporary state can become persistent record

## Recommended Mitigations
- remove manager/evaluator visibility
- separate self-support outputs from assessment systems
- cap feedback frequency
- avoid comparative scores
- make reflection user-controlled
- cap claims at C2 pattern-level cues
- show uncertainty and context limits
- disable long-term retention
- delete raw data by default
- prohibit productivity labels from health or unwellness signals
- separate care suggestions from compliance workflows
- make use voluntary with full opt-out
- preserve user interpretation space
- avoid single-state labels
- avoid actionable flags unless evidence and consent are strong
- remove group benchmarking for self-support data
- ban medical/psychological labels unless clinically validated and ethically governed
- make output self-only
