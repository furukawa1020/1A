# PRESENCE Audit Report: team_health_analytics

- Risk level: **CRITICAL**
- PRESENCE score: **30**

## Detected Patterns
- `P1` Support-to-Assessment
- `P2` Self-Observation-to-Self-Surveillance
- `P3` Cue-to-Claim Escalation
- `P5` Temporary State-to-Persistent Record
- `P7` Care-to-Compliance
- `P10` Ambiguous State-to-Actionable Flag
- `P11` Individual Support-to-Group Benchmarking

## High-Risk Claims
- `C4` group_benchmark: Team stress above baseline

## Claim-Flow
- `c1` self_report, application_usage -> derived_feature -> group_benchmark -> Team stress above baseline -> C4 -> team_benchmark, manager_report, weekly_team_summary -> user, manager, employer, supporter

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
- avoid actionable flags unless evidence and consent are strong
- remove group benchmarking for self-support data
- make output self-only
