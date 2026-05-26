# PRESENCE Guard Reference Monitor Evaluation

## English

This document describes the implemented Paper 1A evaluation. PRESENCE Guard is evaluated as a claim-flow reference monitor: applications must submit proposed claims to the guard before rendering them, and the guard returns `allow`, `rewrite`, or `deny`.

The evaluation command is:

```powershell
python presence-tests\run_presence_evaluation.py --output analysis\outputs\presence_evaluation.json
```

The runner checks:

- P1-P12 misuse-case detection with paired safe and dangerous fixtures.
- Policy mutation sensitivity from a low-risk Noticer Local baseline.
- Runtime decisions for high-stress, productivity-to-manager, and soft-cue claim requests.
- Signed policy verification and tamper rejection.
- Invalid spec and unknown severity rejection.
- Static bypass detection for direct claim rendering.
- Fuzz negative tests that ensure high-risk requests are never allowed.
- No-network core scanning for the Rust and C core files.
- Runtime dependency surface checks.
- Lightweight decision latency and artifact-size measurements.

The browser demo now treats Guard output as authoritative. It initially shows a neutral pending message, then renders only the guard-approved text, the guard rewrite, or a denial message. It does not render `condition.output_text` directly as the user-visible state claim.

## 日本語

この文書は、Paper 1Aで実装済みの評価を説明する。PRESENCE Guardはclaim-flow reference monitorとして評価される。アプリケーションは状態claimを直接表示せず、表示前にclaim requestをGuardへ渡し、Guardの `allow`、`rewrite`、`deny` に従う。

評価コマンドは次である。

```powershell
python presence-tests\run_presence_evaluation.py --output analysis\outputs\presence_evaluation.json
```

評価ランナーは次を確認する。

- P1からP12までのmisuse-caseについて、安全fixtureと危険fixtureの対で検出を確認する。
- 低リスクなNoticer Local baselineからのpolicy mutationに対するscore上昇を確認する。
- high-stress、productivity-to-manager、soft-cue requestに対するruntime decisionを確認する。
- 署名付きpolicyの検証と改ざん拒否を確認する。
- invalid specとunknown severityの拒否を確認する。
- 直接claim描画に対するstatic bypass detectionを行う。
- 高リスクrequestがallowされないことをfuzz negative testで確認する。
- Rust coreとC coreにnetwork API呼び出しがないことをscanする。
- runtime dependency surfaceを確認する。
- 軽量なdecision latencyとartifact sizeを測定する。

ブラウザdemoでは、Guard出力を権威ある判定として扱う。最初は中立的な判定中メッセージのみを表示し、その後はGuardが許可した文、Guardのrewrite、またはdenyメッセージだけを表示する。`condition.output_text` を利用者に見える状態claimとして直接描画しない。
