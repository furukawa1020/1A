# Completion Checklist / 完成条件チェックリスト

## English

This file maps the implementation to the strict Paper 1A completion criteria.

| Criterion | Current status | Evidence |
| --- | --- | --- |
| Claim is treated as a security/privacy asset | Implemented | `presence-audit/schema/presence.schema.json`, `paper/framework.md` |
| Claim-flow graph is machine-generated | Implemented | `presence-audit/cli/presence_audit.py`, `presence-audit/reports/sample_report.md` |
| Authority boundary is modeled | Implemented | `presence-audit/cli/presence_audit.py` |
| Interpretation boundary is modeled | Implemented | `presence-audit/cli/presence_audit.py` |
| Claim severity ladder C0-C6 is defined | Implemented | `app/audit_specs/presence_framework.json`, `presence-audit/schema/presence.schema.json` |
| 12 surveillance transmutation patterns are cataloged | Implemented | `app/audit_specs/presence_framework.json`, `presence-audit/cli/presence_audit.py` |
| Machine-readable audit spec exists | Implemented | `presence-audit/schema/presence.schema.json`, `presence-audit/examples/*.yaml` |
| CLI audit tool exists | Implemented | `presence-audit/cli/presence_audit.py` |
| Report generator exists | Implemented | `presence-audit/reports/sample_report.md` |
| CI integration example exists | Implemented | `.github/workflows/presence-audit.yml`, `presence-audit/action/action.yml` |
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

- Tighten the scoring rationale and thresholds.
- Expand case-study discussion and compare outputs.
- Complete related work with citations.
- Convert templates into a submission-ready paper.
- In Paper 1B, collect real participant data and validate high/medium/low PRESENCE risk levels.

## 日本語

このファイルは、実装とPaper 1Aの厳しい完成条件を対応づける。

| 条件 | 現在の状態 | 根拠 |
| --- | --- | --- |
| claimをセキュリティ/プライバシー資産として扱う | 実装済み | `presence-audit/schema/presence.schema.json`, `paper/framework.md` |
| claim-flow graphを機械生成する | 実装済み | `presence-audit/cli/presence_audit.py`, `presence-audit/reports/sample_report.md` |
| authority boundaryをモデル化する | 実装済み | `presence-audit/cli/presence_audit.py` |
| interpretation boundaryをモデル化する | 実装済み | `presence-audit/cli/presence_audit.py` |
| claim severity ladder C0-C6を定義する | 実装済み | `app/audit_specs/presence_framework.json`, `presence-audit/schema/presence.schema.json` |
| 12個の監視化転化パターンを整理する | 実装済み | `app/audit_specs/presence_framework.json`, `presence-audit/cli/presence_audit.py` |
| 機械可読な監査仕様がある | 実装済み | `presence-audit/schema/presence.schema.json`, `presence-audit/examples/*.yaml` |
| CLI監査ツールがある | 実装済み | `presence-audit/cli/presence_audit.py` |
| レポート生成器がある | 実装済み | `presence-audit/reports/sample_report.md` |
| CI統合例がある | 実装済み | `.github/workflows/presence-audit.yml`, `presence-audit/action/action.yml` |
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

- スコアリング根拠と閾値をさらに厳密化する。
- ケーススタディの議論と比較を厚くする。
- 引用付きの関連研究を完成させる。
- 雛形を投稿可能な論文本体へ仕上げる。
- Paper 1Bで実参加者データを収集し、PRESENCEの高・中・低リスク判定を妥当性検証する。
