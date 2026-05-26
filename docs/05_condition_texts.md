# Condition Texts / 条件文面

## English

The condition file is:

```text
app/conditions/conditions_2x2x2.json
```

Conditions are not hard-coded into the renderer. The app loads the JSON file and changes only:

- `processing_text`
- `visibility_text`
- `output_text`

The same UI template, layout, colors, typography, and response items are used across all eight conditions.

Each condition also includes an `audit` manifest. This manifest is not an additional participant-facing manipulation. It records the researcher-side data-flow interpretation used by ESS and policy audits:

- data asset,
- trust boundaries,
- observers,
- secondary-use channels,
- identifiability,
- output claim strength.

### Common Scenario

The common scenario avoids saying that the participant is low-performing, stressed, lazy, or definitely experiencing concentration decline. It describes only a presenteeism context:

- not fully well,
- not absent or withdrawn,
- still participating,
- feeling some strain internally.

### Output Text Control

Assertive outputs use labels and recommendations. Non-assertive outputs use cues and interpretive space. Both are rendered in the same output block with the same number of output lines.

## 日本語

条件定義ファイルは次である。

```text
app/conditions/conditions_2x2x2.json
```

条件はレンダラー内に直書きしない。アプリはJSONファイルを読み込み、次の3つだけを変更する。

- `processing_text`
- `visibility_text`
- `output_text`

8条件すべてで、同じUIテンプレート、レイアウト、色、タイポグラフィ、回答項目を使用する。

各条件には `audit` マニフェストも含める。このマニフェストは参加者向けの追加操作ではない。ESSとポリシー監査に用いる研究者側のデータフロー解釈として、次を記録する。

- データ資産。
- 信頼境界。
- 可視主体。
- 二次利用チャネル。
- 識別可能性。
- 出力主張の強さ。

### 共通シナリオ

共通シナリオでは、参加者の成績が低い、ストレス状態である、怠けている、集中力が確実に低下している、といった決めつけを避ける。記述するのは、次のプレゼンティーズム文脈のみである。

- 万全ではない。
- 欠席・離脱していない。
- 参加し続けている。
- 内側では少し無理をしている感覚がある。

### 出力文面の統制

断定的出力ではラベルと推奨を用いる。非断定的出力では手がかりと解釈余地を用いる。どちらも同じ出力ブロックに、同じ行数で表示する。
