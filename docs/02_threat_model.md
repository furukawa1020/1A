# Threat Model / 脅威モデル

## English

The threat model is not limited to malicious external attackers. Surveillance transmutation can occur under benevolent or organizationally legitimate language such as support, health management, learning support, workplace improvement, early noticing, or well-being.

### Information Assets

- Work or study state data.
- State-related features derived from behavior or interaction.
- System outputs about the user's current state.
- Free-text responses collected during the experiment.
- Condition-level response records.

### Threat Actors

- Managers, teachers, employers, or evaluators.
- Service providers operating cloud or analytics infrastructure.
- Researchers with access to experimental records.
- The system itself when it makes assertive claims about internal state.
- Organizational processes that reuse reports beyond the user's self-support context.

### Trust Boundaries

- User device vs. cloud server.
- Self-only display vs. third-party report.
- Non-assertive cue vs. assertive label.
- Research data collection environment vs. the scenario system being evaluated.

### Transmutation Path

Support intention can transform into surveillance through:

```text
Support Intention
  -> Sensing / Logging
  -> State Inference
  -> Output Claim
  -> Visibility / Sharing
  -> Managerial or Self-surveillance Effect
```

The core security/privacy issue is not only whether data is encrypted or access-controlled. It is also what the system is allowed to claim, where the data is processed, and who can see the result.

## 日本語

この脅威モデルは、悪意ある外部攻撃者だけを対象にしない。監視化への転化は、本人支援、健康管理、学習支援、職場環境改善、早期気づき、ウェルビーイングといった善意または組織的に正当化されやすい言葉のもとでも起こりうる。

### 情報資産

- 仕事・学業に関する状態データ。
- 行動やインタラクションから導出された状態関連特徴量。
- ユーザーの現在状態に関するシステム出力。
- 実験中に収集される自由記述回答。
- 条件ごとの回答記録。

### 脅威主体

- 管理者、教員、雇用者、評価者。
- クラウド基盤や分析基盤を運用するサービス提供者。
- 実験記録にアクセスできる研究者。
- 内部状態について断定的主張を行うシステム自身。
- 本人支援の文脈を超えてレポートを再利用する組織プロセス。

### 信頼境界

- ユーザー端末 vs. クラウドサーバ。
- 本人のみ表示 vs. 第三者向けレポート。
- 非断定的手がかり vs. 断定的ラベル。
- 研究データ収集環境 vs. 評価対象となるシナリオ上のシステム。

### 転化経路

支援意図は、次の経路を通じて監視へ転化しうる。

```text
Support Intention
  -> Sensing / Logging
  -> State Inference
  -> Output Claim
  -> Visibility / Sharing
  -> Managerial or Self-surveillance Effect
```

中核的なセキュリティ/プライバシー問題は、データが暗号化されているか、アクセス制御されているかだけではない。システムが何を主張してよいのか、データがどこで処理されるのか、その結果を誰が見られるのかも問題である。

