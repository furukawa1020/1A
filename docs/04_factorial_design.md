# Factorial Design / 因子設計

## English

Study 1A uses a 2 x 2 x 2 within-subject factorial scenario experiment.

| Factor | Level 1 | Level 2 |
| --- | --- | --- |
| Processing Location | Cloud | Local |
| Third-party Visibility | Manager-visible | Self-only |
| Output Claim | Assertive Label | Non-assertive Cue |

### Conditions

| ID | Processing | Visibility | Output |
| --- | --- | --- | --- |
| C1 | Cloud | Manager-visible | Assertive |
| C2 | Cloud | Manager-visible | Non-assertive |
| C3 | Cloud | Self-only | Assertive |
| C4 | Cloud | Self-only | Non-assertive |
| C5 | Local | Manager-visible | Assertive |
| C6 | Local | Manager-visible | Non-assertive |
| C7 | Local | Self-only | Assertive |
| C8 | Local | Self-only | Non-assertive |

The proposed lower-risk configuration is C8. The high-risk reference configuration is C1.

### Order

The app assigns a balanced Latin-square-like sequence based on the participant ID. The participant ID is generated randomly by default, so participants are distributed across order rows while preserving logged reproducibility.

The exported response includes:

- `condition_order`
- `condition_sequence`
- `order_strategy`

## 日本語

Study 1A は、2 x 2 x 2 の被験者内シナリオベース因子実験である。

| 因子 | 水準1 | 水準2 |
| --- | --- | --- |
| 処理場所 | Cloud | Local |
| 第三者可視性 | Manager-visible | Self-only |
| 出力主張 | Assertive Label | Non-assertive Cue |

### 条件

| ID | 処理場所 | 可視性 | 出力 |
| --- | --- | --- | --- |
| C1 | Cloud | Manager-visible | Assertive |
| C2 | Cloud | Manager-visible | Non-assertive |
| C3 | Cloud | Self-only | Assertive |
| C4 | Cloud | Self-only | Non-assertive |
| C5 | Local | Manager-visible | Assertive |
| C6 | Local | Manager-visible | Non-assertive |
| C7 | Local | Self-only | Assertive |
| C8 | Local | Self-only | Non-assertive |

監視化リスクを抑える設計候補は C8 である。高リスク参照条件は C1 である。

### 条件順序

アプリは参加者IDに基づき、バランスド・ラテン方格に近い順序を割り当てる。参加者IDは標準でランダム生成されるため、参加者は順序行に分散される。同時に、ログとして再現可能な順序も保存される。

エクスポートされる回答には次が含まれる。

- `condition_order`
- `condition_sequence`
- `order_strategy`

