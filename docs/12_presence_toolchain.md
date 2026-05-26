# PRESENCE Toolchain / PRESENCEツールチェーン

## English

Paper 1A is defined as claim-capability enforcement middleware and a supporting security/privacy audit toolchain.

The main artifact is:

> `PRESENCE Guard`: a claim reference monitor for presenteeism support and well-being support systems.

The toolchain includes:

- `presence-core/`
- `presence-policy/`
- `presence-sdk-js/`
- `presence-sdk-dart/`
- `presence-ffi-c/`
- `presence-audit/schema/presence.schema.json`
- `presence-audit/cli/presence_audit.py`
- `presence-audit/examples/*.yaml`
- `presence-audit/reports/sample_report.md`
- `.github/workflows/presence-audit.yml`

## What It Audits

PRESENCE Guard treats claims as security/privacy control objects. It enforces:

- claim-flow,
- data boundary,
- authority boundary,
- interpretation boundary,
- claim severity,
- surveillance transmutation patterns,
- allow/rewrite/deny/require-consent decisions.

## 1A / 1B Split

Paper 1A:

- Defines PRESENCE Guard.
- Implements runtime claim enforcement and `presence-audit`.
- Applies it to representative case studies.
- Produces static risk and mitigation reports without human participants.

Paper 1B:

- Takes high-, medium-, and low-risk configurations from PRESENCE.
- Implements controlled participant-facing interfaces.
- Tests whether MFS, LIS, SOUS, WU, and WD align with PRESENCE risk levels.

## 日本語

Paper 1Aは、claim-capability enforcement middlewareと、それを支えるセキュリティ/プライバシー監査ツールチェーンとして定義する。

主成果物は次である。

> `PRESENCE Guard`: プレゼンティーズム支援・ウェルビーイング支援システムのためのclaim reference monitor。

ツールチェーンには次を含める。

- `presence-core/`
- `presence-policy/`
- `presence-sdk-js/`
- `presence-sdk-dart/`
- `presence-ffi-c/`
- `presence-audit/schema/presence.schema.json`
- `presence-audit/cli/presence_audit.py`
- `presence-audit/examples/*.yaml`
- `presence-audit/reports/sample_report.md`
- `.github/workflows/presence-audit.yml`

## 何を監査するか

PRESENCE Guard はclaimをセキュリティ/プライバシー上の制御対象として扱う。強制対象は次である。

- claim-flow。
- data boundary。
- authority boundary。
- interpretation boundary。
- claim severity。
- surveillance transmutation patterns。
- allow/rewrite/deny/require-consent判定。

## 1A / 1B の分割

Paper 1A:

- PRESENCE Guardを定義する。
- runtime claim enforcementと`presence-audit`を実装する。
- 代表的ケーススタディに適用する。
- 人を使わず、静的なリスクと緩和策レポートを生成する。

Paper 1B:

- PRESENCEが高・中・低リスクと判定した構成を用いる。
- 統制された参加者向けインターフェースを実装する。
- MFS、LIS、SOUS、WU、WDがPRESENCEリスクレベルと対応するかを検証する。
