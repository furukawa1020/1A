# presence-audit

## English

`presence-audit` is a PRESENCE command-line tool for auditing surveillance transmutation risk in presenteeism support and well-being support systems.

It treats system-generated claims as security/privacy assets. A design YAML file is analyzed for:

- claim-flow,
- data boundary,
- authority boundary,
- interpretation boundary,
- claim severity,
- surveillance transmutation patterns,
- PRESENCE score,
- recommended mitigations.

### Usage

```powershell
python presence-audit\cli\presence_audit.py audit presence-audit\examples\cloud_wellbeing_dashboard.yaml
```

Generate Markdown:

```powershell
python presence-audit\cli\presence_audit.py audit presence-audit\examples\cloud_wellbeing_dashboard.yaml --format markdown --output presence-audit\reports\sample_report.md
```

Fail CI on high risk:

```powershell
python presence-audit\cli\presence_audit.py audit presence.yaml --fail-on HIGH
```

### Risk Levels

- `LOW`: lower exposure; typically local, self-only, non-assertive cues.
- `MEDIUM`: meaningful claim or interpretation risk.
- `HIGH`: authority visibility, long retention, or high-severity claims.
- `CRITICAL`: multiple authority, retention, productivity, and administrative risks co-occur.

## 日本語

`presence-audit` は、プレゼンティーズム支援・ウェルビーイング支援システムにおける監視化転化リスクを監査するPRESENCEコマンドラインツールである。

このツールは、システムが生成するclaimをセキュリティ/プライバシー資産として扱う。設計YAMLを解析し、次を出力する。

- claim-flow。
- data boundary。
- authority boundary。
- interpretation boundary。
- claim severity。
- surveillance transmutation patterns。
- PRESENCE score。
- 推奨緩和策。

### 使い方

```powershell
python presence-audit\cli\presence_audit.py audit presence-audit\examples\cloud_wellbeing_dashboard.yaml
```

Markdownを生成する。

```powershell
python presence-audit\cli\presence_audit.py audit presence-audit\examples\cloud_wellbeing_dashboard.yaml --format markdown --output presence-audit\reports\sample_report.md
```

高リスク以上でCIを失敗させる。

```powershell
python presence-audit\cli\presence_audit.py audit presence.yaml --fail-on HIGH
```

### リスクレベル

- `LOW`: 曝露が低い。典型的にはローカル、本人のみ、非断定手がかり。
- `MEDIUM`: claimまたは解釈上のリスクがある。
- `HIGH`: authority可視性、長期保存、高severity claimがある。
- `CRITICAL`: authority、保存、生産性claim、管理claimが複合する。

