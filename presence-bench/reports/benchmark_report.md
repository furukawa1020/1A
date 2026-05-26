# PRESENCE Benchmark Report

This benchmark uses reference profiles abstracted from public feature documentation. It does not assert that any named service is unsafe or non-compliant.

| Profile | Risk | Score | Passed | Patterns | Missing |
| --- | --- | ---: | --- | --- | --- |
| `employee_app_manager_dashboard` | `CRITICAL` | 32 | no | P1, P10, P12, P2, P3, P5, P7, P9 | P8 |
| `health_data_labor_risk_dashboard` | `CRITICAL` | 34 | yes | P1, P10, P2, P3, P5, P7, P8, P9 | - |
| `noticer_local_low_risk` | `LOW` | 3 | yes | - | - |
| `presenteeism_survey_dashboard` | `CRITICAL` | 31 | no | P1, P10, P12, P2, P3, P5, P6, P7, P8, P9 | P11 |
| `productivity_loss_visualization` | `CRITICAL` | 31 | yes | P1, P10, P11, P2, P3, P5, P6, P7, P8, P9 | - |
| `stress_check_high_risk_extraction` | `CRITICAL` | 34 | yes | P1, P10, P2, P3, P5, P7, P8, P9 | - |

## Recommended Mitigations
### employee_app_manager_dashboard
- remove manager/evaluator visibility
- separate self-support outputs from assessment systems
- cap feedback frequency
- avoid comparative scores
- make reflection user-controlled
- cap claims at C2 pattern-level cues
- show uncertainty and context limits
- disable long-term retention

### health_data_labor_risk_dashboard
- remove manager/evaluator visibility
- separate self-support outputs from assessment systems
- cap feedback frequency
- avoid comparative scores
- make reflection user-controlled
- cap claims at C2 pattern-level cues
- show uncertainty and context limits
- disable long-term retention

### noticer_local_low_risk
- none

### presenteeism_survey_dashboard
- remove manager/evaluator visibility
- separate self-support outputs from assessment systems
- cap feedback frequency
- avoid comparative scores
- make reflection user-controlled
- cap claims at C2 pattern-level cues
- show uncertainty and context limits
- disable long-term retention

### productivity_loss_visualization
- remove manager/evaluator visibility
- separate self-support outputs from assessment systems
- cap feedback frequency
- avoid comparative scores
- make reflection user-controlled
- cap claims at C2 pattern-level cues
- show uncertainty and context limits
- disable long-term retention

### stress_check_high_risk_extraction
- remove manager/evaluator visibility
- separate self-support outputs from assessment systems
- cap feedback frequency
- avoid comparative scores
- make reflection user-controlled
- cap claims at C2 pattern-level cues
- show uncertainty and context limits
- disable long-term retention

## 日本語

このbenchmarkは、公開機能資料から抽象化したreference profileを用いる。実在サービスが危険または非準拠であるとは主張しない。

評価対象は、claim severity、authority boundary、interpretation boundary、retention、secondary use、productivity/administrative claimへの転化である。
