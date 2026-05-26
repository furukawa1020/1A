# Presenteeism Support Surveillance Transmutation Testbed

This repository contains a research-grade experimental testbed for studying when presenteeism support becomes surveillance.

The project does not aim to detect presenteeism, diagnose stress, or evaluate productivity. Instead, it decomposes how processing location, third-party visibility, and output claims shape monitoring feeling, label imposition, and self-observation utility in presenteeism support contexts.

The central security and privacy question is not "How accurately can we infer a user's state?" but "Under what design conditions does support for people working or studying while unwell become surveillance, evaluation, or imposed labeling?"

## 日本語版

本リポジトリは、プレゼンティーズム支援がどのような設計条件で監視へ転化するのかを検証する研究用実験基盤である。

本研究は、プレゼンティーズムの検出、ストレス診断、生産性評価を目的としない。処理場所、第三者可視性、出力の断定性が、監視感、ラベル押し付け感、自己観察支援効果にどのような影響を与えるかを因子分解して検証する。

中心問いは「ユーザー状態をどれだけ正確に推定できるか」ではなく、「不調を抱えながら働く・学ぶ人への支援が、どの条件で監視・評価・ラベリングへ転化するのか」である。

## Repository Layout

- `docs/`: positioning, threat model, factorial design, measures, ESS audit, ethics, and analysis plan.
- `app/`: browser-based PSTT experiment interface and 2x2x2 condition file.
- `analysis/`: preregistration draft and analysis scripts.
- `paper/`: paper title, abstract, introduction, method, and discussion templates.

## Run The Testbed

The app loads `app/conditions/conditions_2x2x2.json`, so serve it over local HTTP:

```powershell
python -m http.server 8000 --bind 127.0.0.1 --directory app
```

Then open:

```text
http://127.0.0.1:8000/
```

Responses are stored in the browser's local storage and can be exported as CSV or JSON. No server upload is performed by the app.

## Study Design

The core study is a 2 x 2 x 2 within-subject factorial scenario experiment:

| Factor | Level 1 | Level 2 |
| --- | --- | --- |
| Processing Location | Cloud | Local |
| Third-party Visibility | Manager-visible | Self-only |
| Output Claim | Assertive Label | Non-assertive Cue |

The proposed lower-risk configuration is `C8 = Local + Self-only + Non-assertive Cue`.

## Non-Goals

This project must not claim that it can:

- detect presenteeism,
- diagnose stress or mental health,
- evaluate productivity,
- improve health outcomes,
- prove that cloud processing or manager visibility is always harmful.

