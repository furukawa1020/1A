# PRESENCE Toolchain / PRESENCEツールチェーン

## English

Paper 1A is defined as a static security/privacy audit framework and toolchain.

The main artifact is:

> `presence-audit`: a privacy/security linter for presenteeism support and well-being support systems.

The toolchain includes:

- `presence-audit/schema/presence.schema.json`
- `presence-audit/cli/presence_audit.py`
- `presence-audit/examples/*.yaml`
- `presence-audit/reports/sample_report.md`
- `.github/workflows/presence-audit.yml`

## What It Audits

`presence-audit` treats claims as security/privacy assets. It audits:

- claim-flow,
- data boundary,
- authority boundary,
- interpretation boundary,
- claim severity,
- surveillance transmutation patterns,
- recommended mitigations.

## 1A / 1B Split

Paper 1A:

- Defines PRESENCE.
- Implements `presence-audit`.
- Applies it to representative case studies.
- Produces static risk and mitigation reports without human participants.

Paper 1B:

- Takes high-, medium-, and low-risk configurations from PRESENCE.
- Implements controlled participant-facing interfaces.
- Tests whether MFS, LIS, SOUS, WU, and WD align with PRESENCE risk levels.

## 日本語

Paper 1Aは、静的なセキュリティ/プライバシー監査フレームワークとツールチェーンとして定義する。

主成果物は次である。

> `presence-audit`: プレゼンティーズム支援・ウェルビーイング支援システムのための privacy/security linter。

ツールチェーンには次を含める。

- `presence-audit/schema/presence.schema.json`
- `presence-audit/cli/presence_audit.py`
- `presence-audit/examples/*.yaml`
- `presence-audit/reports/sample_report.md`
- `.github/workflows/presence-audit.yml`

## 何を監査するか

`presence-audit` はclaimをセキュリティ/プライバシー資産として扱う。監査対象は次である。

- claim-flow。
- data boundary。
- authority boundary。
- interpretation boundary。
- claim severity。
- surveillance transmutation patterns。
- 推奨緩和策。

## 1A / 1B の分割

Paper 1A:

- PRESENCEを定義する。
- `presence-audit` を実装する。
- 代表的ケーススタディに適用する。
- 人を使わず、静的なリスクと緩和策レポートを生成する。

Paper 1B:

- PRESENCEが高・中・低リスクと判定した構成を用いる。
- 統制された参加者向けインターフェースを実装する。
- MFS、LIS、SOUS、WU、WDがPRESENCEリスクレベルと対応するかを検証する。

