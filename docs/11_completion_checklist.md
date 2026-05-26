# Completion Checklist / 完成条件チェックリスト

## English

This file maps the implementation to the strict Paper 1A completion criteria.

| Criterion | Current status | Evidence |
| --- | --- | --- |
| Presenteeism is not reduced to concentration decline | Implemented | Common scenario avoids diagnosing concentration or productivity. |
| Threat actors include managers, schools, providers, and the system itself | Implemented | `docs/02_threat_model.md` |
| 2 x 2 x 2 conditions are implemented | Implemented | `app/conditions/conditions_2x2x2.json` |
| UI differences are limited to the three factors | Implemented | `app/src/condition_renderer/renderer.js` |
| Manipulation checks exist | Implemented | `app/src/manipulation_check/items.js` |
| ESS is a design audit score, not a subjective scale | Implemented | `app/audit.html`, `analysis/scripts/08_compute_ess.py` |
| MFS/LIS/SOUS/WU/WD are implemented | Implemented | `app/src/questionnaire/items.js` |
| Analysis scripts exist | Implemented | `analysis/scripts/` |
| Exclusion criteria are written | Implemented | `analysis/preregistration.md`, `docs/09_analysis_plan.md` |
| Ethics document exists | Implemented draft | `docs/08_ethics_statement.md` |
| Abstract/Intro/Method templates exist | Implemented draft | `paper/` |
| Submission targets are scoped | Implemented | `docs/10_submission_strategy.md` |

### Remaining Before Paper Submission

- Collect real participant data.
- Confirm manipulation checks empirically.
- Report reliability and sensitivity analyses.
- Complete related work with citations.
- Convert templates into a submission-ready paper.

## 日本語

このファイルは、実装とPaper 1Aの厳しい完成条件を対応づける。

| 条件 | 現在の状態 | 根拠 |
| --- | --- | --- |
| プレゼンティーズム定義が集中低下に落ちていない | 実装済み | 共通シナリオは集中力・生産性を診断しない。 |
| 脅威主体に管理者・学校・提供者・システム自身を含む | 実装済み | `docs/02_threat_model.md` |
| 2 x 2 x 2 条件が実装されている | 実装済み | `app/conditions/conditions_2x2x2.json` |
| UI差分が3因子に限定されている | 実装済み | `app/src/condition_renderer/renderer.js` |
| 操作チェックがある | 実装済み | `app/src/manipulation_check/items.js` |
| ESSが主観尺度ではなく設計監査指標になっている | 実装済み | `app/audit.html`, `analysis/scripts/08_compute_ess.py` |
| MFS/LIS/SOUS/WU/WDが実装されている | 実装済み | `app/src/questionnaire/items.js` |
| 分析スクリプトがある | 実装済み | `analysis/scripts/` |
| 除外基準が事前に書かれている | 実装済み | `analysis/preregistration.md`, `docs/09_analysis_plan.md` |
| 倫理文書がある | ドラフト実装済み | `docs/08_ethics_statement.md` |
| Abstract/Intro/Methodの雛形がある | ドラフト実装済み | `paper/` |
| 投稿先が明確に切られている | 実装済み | `docs/10_submission_strategy.md` |

### 論文投稿前に残ること

- 実参加者データを収集する。
- 操作チェックが実際に効くことを確認する。
- 信頼性分析と感度分析を報告する。
- 引用付きの関連研究を完成させる。
- 雛形を投稿可能な論文本体へ仕上げる。

