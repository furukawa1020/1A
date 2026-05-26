# Presenteeism Support Surveillance Transmutation Testbed

## English

This repository contains PRESENCE, a claim-flow security/privacy audit framework for studying when presenteeism support becomes surveillance.

The project does not aim to detect presenteeism, diagnose stress, or evaluate productivity. Instead, it treats system-generated claims as security/privacy assets and audits how processing, retention, authority visibility, secondary use, evidence strength, normative actionability, claim severity, and exit possibility shape surveillance transmutation risk.

The central security and privacy question is not "How accurately can we infer a user's state?" but "When do claims generated for self-observation cross authority and interpretation boundaries and become monitoring, labeling, or assessment?"

### Repository Layout

- `presence-audit/`: schema, CLI, examples, sample reports, and CI/action integration for PRESENCE.
- `docs/`: positioning, threat model, PRESENCE toolchain, factorial design, measures, ESS audit, ethics, and analysis plan.
- `app/`: browser-based PSTT experiment interface and 2x2x2 condition file.
- `app/audit.html`: researcher-only audit view that computes ESS and policy findings without participant ratings.
- `analysis/`: preregistration draft and analysis scripts.
- `analysis/scripts/08_compute_ess.py`: researcher-side ESS audit from the condition JSON.
- `analysis/scripts/09_policy_audit.py`: policy finding audit from the condition JSON.
- `paper/`: paper title, abstract, introduction, method, and discussion templates.

### Run The Testbed

The app loads `app/conditions/conditions_2x2x2.json`, so serve it over local HTTP:

```powershell
python -m http.server 8000 --bind 127.0.0.1 --directory app
```

Then open:

```text
http://127.0.0.1:8000/
```

Responses are stored in the browser's local storage and can be exported as CSV or JSON. No server upload is performed by the app.

For researcher-side condition auditing without participants, open:

```text
http://127.0.0.1:8000/audit.html
```

### Run presence-audit

```powershell
python presence-audit\cli\presence_audit.py audit presence-audit\examples\cloud_wellbeing_dashboard.yaml
```

Generate a Markdown report:

```powershell
python presence-audit\cli\presence_audit.py audit presence-audit\examples\cloud_wellbeing_dashboard.yaml --format markdown --output presence-audit\reports\sample_report.md
```

### Study Design

The Paper 1A artifact is a static audit framework and toolchain. The 2 x 2 x 2 scenario experiment is retained as the Paper 1B validation path:

| Factor | Level 1 | Level 2 |
| --- | --- | --- |
| Processing Location | Cloud | Local |
| Third-party Visibility | Manager-visible | Self-only |
| Output Claim | Assertive Label | Non-assertive Cue |

The proposed lower-risk configuration is `C8 = Local + Self-only + Non-assertive Cue`.

### Non-Goals

This project must not claim that it can:

- detect presenteeism,
- diagnose stress or mental health,
- evaluate productivity,
- improve health outcomes,
- prove that cloud processing or manager visibility is always harmful.

## 日本語

本リポジトリは、プレゼンティーズム支援がどのような条件で監視へ転化するのかを監査する、Claim-Flow セキュリティ/プライバシーフレームワーク PRESENCE を含む。

本プロジェクトは、プレゼンティーズムの検出、ストレス診断、生産性評価を目的としない。その代わりに、システムが生成するclaimをセキュリティ/プライバシー資産として扱い、処理、保持、authority可視性、二次利用、証拠強度、行動命令性、claim severity、離脱可能性が監視化リスクにどう関わるかを監査する。

中心となるセキュリティ/プライバシー上の問いは、「ユーザー状態をどれだけ正確に推定できるか」ではなく、「自己観察のために生成されたclaimが、いつauthority boundaryやinterpretation boundaryを越え、監視・ラベリング・査定になるのか」である。

### リポジトリ構成

- `presence-audit/`: PRESENCEのschema、CLI、examples、sample reports、CI/action統合。
- `docs/`: 位置づけ、脅威モデル、PRESENCEツールチェーン、因子設計、尺度、ESS監査、倫理、分析計画。
- `app/`: ブラウザで動作するPSTT実験UIと2x2x2条件定義ファイル。
- `app/audit.html`: 参加者評価なしでESSとポリシー所見を計算する研究者用監査ビュー。
- `analysis/`: 事前登録草案と分析スクリプト。
- `analysis/scripts/08_compute_ess.py`: 条件JSONから研究者側ESS監査を行うスクリプト。
- `analysis/scripts/09_policy_audit.py`: 条件JSONからポリシー所見を出す監査スクリプト。
- `paper/`: 論文タイトル、要旨、導入、方法、結果、議論の雛形。

### 実験基盤の起動

アプリは `app/conditions/conditions_2x2x2.json` を読み込むため、ローカルHTTPで配信する。

```powershell
python -m http.server 8000 --bind 127.0.0.1 --directory app
```

その後、次のURLを開く。

```text
http://127.0.0.1:8000/
```

回答はブラウザのローカルストレージに保存され、CSVまたはJSONとしてエクスポートできる。アプリは回答をサーバーへアップロードしない。

参加者を使わずに条件監査だけを行う場合は、次を開く。

```text
http://127.0.0.1:8000/audit.html
```

### presence-audit の実行

```powershell
python presence-audit\cli\presence_audit.py audit presence-audit\examples\cloud_wellbeing_dashboard.yaml
```

Markdownレポートを生成する。

```powershell
python presence-audit\cli\presence_audit.py audit presence-audit\examples\cloud_wellbeing_dashboard.yaml --format markdown --output presence-audit\reports\sample_report.md
```

### 研究デザイン

Paper 1Aの中核成果物は、静的監査フレームワークとツールチェーンである。2 x 2 x 2 のシナリオ実験は、Paper 1Bの妥当性検証として残す。

| 因子 | 水準1 | 水準2 |
| --- | --- | --- |
| 処理場所 | Cloud | Local |
| 第三者可視性 | Manager-visible | Self-only |
| 出力断定性 | Assertive Label | Non-assertive Cue |

監視化リスクを抑える設計候補は `C8 = Local + Self-only + Non-assertive Cue` である。

### 非目的

本プロジェクトでは、以下を主張してはいけない。

- プレゼンティーズムを検出できる。
- ストレスやメンタルヘルスを診断できる。
- 生産性を評価できる。
- 健康上のアウトカムを改善できる。
- クラウド処理や管理者可視性が常に有害である。
