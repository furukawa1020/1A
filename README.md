# Presenteeism Support Surveillance Transmutation Testbed

## English

This repository contains a research-grade experimental testbed for studying when presenteeism support becomes surveillance.

The project does not aim to detect presenteeism, diagnose stress, or evaluate productivity. Instead, it decomposes how processing location, third-party visibility, and output claims shape monitoring feeling, label imposition, and self-observation utility in presenteeism support contexts.

The central security and privacy question is not "How accurately can we infer a user's state?" but "Under what design conditions does support for people working or studying while unwell become surveillance, evaluation, or imposed labeling?"

### Repository Layout

- `docs/`: positioning, threat model, factorial design, measures, ESS audit, ethics, and analysis plan.
- `app/`: browser-based PSTT experiment interface and 2x2x2 condition file.
- `analysis/`: preregistration draft and analysis scripts.
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

### Study Design

The core study is a 2 x 2 x 2 within-subject factorial scenario experiment:

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

本リポジトリは、プレゼンティーズム支援がどのような条件で監視へ転化するのかを検証するための、研究用実験基盤である。

本プロジェクトは、プレゼンティーズムの検出、ストレス診断、生産性評価を目的としない。その代わりに、処理場所、第三者可視性、出力の断定性が、プレゼンティーズム支援文脈における監視感、ラベル押し付け感、自己観察支援効果にどのような影響を与えるかを因子分解する。

中心となるセキュリティ/プライバシー上の問いは、「ユーザー状態をどれだけ正確に推定できるか」ではなく、「不調を抱えながら働く・学ぶ人への支援が、どの設計条件で監視・評価・ラベリングへ転化するのか」である。

### リポジトリ構成

- `docs/`: 位置づけ、脅威モデル、因子設計、尺度、ESS監査、倫理、分析計画。
- `app/`: ブラウザで動作するPSTT実験UIと2x2x2条件定義ファイル。
- `analysis/`: 事前登録草案と分析スクリプト。
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

### 研究デザイン

中核となる研究は、2 x 2 x 2 の被験者内シナリオベース因子実験である。

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

