# ESS: Exposure Surface Score / 曝露面スコア

## English

ESS is not a participant attitude score. It is a researcher-side design audit score for exposure surface.

### Items

| Item | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Data transmission | None | Features only | Raw data |
| Processing location | On device | Edge / limited server | Cloud |
| Storage | None / short-term | Local storage | Cloud long-term |
| Third-party visibility | Self only | Researcher / supporter | Manager / teacher / employer |
| Identifiability | Anonymous | Pseudonymous ID | Real name / organizational ID |
| Secondary use | Difficult by design | Export possible | Report / API / admin dashboard |
| Output claim | Non-assertive cue | Score | Psychological or productivity label |

### Weights

| Item | Weight |
| --- | --- |
| Third-party visibility | 2.0 |
| Secondary use | 2.0 |
| Output claim | 1.5 |
| Other items | 1.0 |

### Intended Use

ESS supports the security/privacy contribution by separating design exposure from subjective discomfort. Participant-rated outcomes may vary by individual, but ESS records what the scenario design exposes by construction.

The score should be reported alongside MFS, LIS, SOUS, WU, and WD. ESS should not be interpreted as a psychological scale.

The repository includes `analysis/scripts/08_compute_ess.py` to compute condition-level ESS from the condition JSON. The script records a bilingual audit note in the output so that ESS is not confused with participant-rated outcomes.

The app also includes `app/audit.html`, a researcher-only audit view. This view computes ESS and policy findings from the condition manifest without participant responses. It should not be shown as part of the participant flow because it can prime responses.

## 日本語

ESSは参加者の態度スコアではない。研究者側が設計上の曝露面を監査するためのスコアである。

### 項目

| 項目 | 0 | 1 | 2 |
| --- | --- | --- | --- |
| データ送信 | なし | 特徴量のみ | 生データ |
| 処理場所 | 端末内 | エッジ / 限定サーバ | クラウド |
| 保存 | なし / 短時間 | ローカル保存 | クラウド長期保存 |
| 第三者可視性 | 本人のみ | 研究者 / 支援者 | 管理者 / 教員 / 雇用者 |
| 識別可能性 | 匿名 | 仮名ID | 実名 / 組織ID |
| 二次利用 | 設計上困難 | エクスポート可能 | レポート / API / 管理画面 |
| 出力主張 | 非断定的手がかり | スコア | 心理 / 生産性ラベル |

### 重み

| 項目 | 重み |
| --- | --- |
| 第三者可視性 | 2.0 |
| 二次利用 | 2.0 |
| 出力主張 | 1.5 |
| その他の項目 | 1.0 |

### 利用目的

ESSは、設計上の曝露と主観的不快感を分けることで、セキュリティ/プライバシー上の貢献を支える。参加者評価は個人差を含むが、ESSはシナリオ設計が構造的に何を曝露するかを記録する。

ESSはMFS、LIS、SOUS、WU、WDと並べて報告する。ただし、心理尺度として解釈してはいけない。

このリポジトリには、条件JSONから条件ごとのESSを計算する `analysis/scripts/08_compute_ess.py` を含める。このスクリプトは出力に英日併記の監査メモを含め、ESSが参加者評価アウトカムと混同されないようにする。

アプリには研究者専用の監査ビュー `app/audit.html` も含める。このビューは参加者回答なしで、条件マニフェストからESSとポリシー所見を計算する。参加者の回答を誘導しうるため、参加者フローの一部としては表示しない。
