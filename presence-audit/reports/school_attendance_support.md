# PRESENCE Audit Report: school_attendance_support

- Risk level: **CRITICAL**
- PRESENCE score: **34**

## Detected Patterns
- `P1` Support-to-Assessment
- `P2` Self-Observation-to-Self-Surveillance
- `P3` Cue-to-Claim Escalation
- `P5` Temporary State-to-Persistent Record
- `P7` Care-to-Compliance
- `P8` Voluntary Reflection-to-Mandatory Monitoring
- `P9` Context Collapse
- `P10` Ambiguous State-to-Actionable Flag

## High-Risk Claims
- `C6` administrative: Attention needed

## Claim-Flow
- `c1` attendance, self_report -> derived_feature -> administrative -> Attention needed -> C6 -> teacher_flag, attendance_follow_up, weekly_summary -> user, teacher, supporter, evaluator

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
- separate care suggestions from compliance workflows
- make use voluntary with full opt-out
- preserve user interpretation space
- avoid single-state labels
- avoid actionable flags unless evidence and consent are strong
- make output self-only
