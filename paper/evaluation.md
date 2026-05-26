# Evaluation / 評価

## English

Paper 1A evaluates PRESENCE Guard as a claim-flow reference monitor, not only as a reporting tool.

Implemented non-human evaluation:

- Misuse-case detection for P1-P12 with safe and dangerous fixtures.
- Policy mutation testing from the low-risk Noticer Local configuration.
- Runtime guard decisions for allow, rewrite, and deny fixtures.
- Static claim scanning for direct dangerous claim literals, including a positive bypass fixture and a negative scan over the Guard-integrated app.
- Public-information reference benchmark over workplace health management and presenteeism-visualization feature profiles.
- Security hardening checks for invalid policy rejection, signed policy tamper rejection, unknown severity denial, bypass detection, fuzz negative tests, no-network core scanning, dependency-surface checking, and SBOM documentation.
- Integration artifacts for Web/JavaScript, TypeScript, Dart/Flutter, C FFI, CLI, CI/action, browser reference-monitor demo, and third-party templates.
- Overhead measurement for the Python reference engine and release artifact size measurement for the Rust no-network core.

The reproducible evaluation command is:

```powershell
python presence-tests\run_presence_evaluation.py --output analysis\outputs\presence_evaluation.json
```

A separate micro-benchmark can be run with:

```powershell
python presence-tests\benchmark_guard.py --output analysis\outputs\presence_overhead.json
```

The evaluation passes only if every dangerous misuse-case fixture is detected, every paired safe fixture avoids the target pattern, dangerous mutations increase the PRESENCE score, high-risk runtime claims are denied or rewritten, policy tampering is rejected, direct condition-output rendering is absent from the demo app, the static scanner detects the bypass fixture while passing the Guard-integrated app, minimized audit logs exclude claim text and source signals, fuzzed high-risk requests are never allowed, and the no-network core contains no network API calls.

The public-information benchmark is run with:

```powershell
python presence-bench\run_benchmark.py --output presence-bench\reports\benchmark_report.md
```

The benchmark profiles are derived from public feature descriptions and do not claim that any named service is unsafe, non-compliant, or surveillance-oriented.

Paper 1B will evaluate whether high-, medium-, and low-risk configurations identified by PRESENCE correspond to participant-rated monitoring feeling, label imposition, and self-observation utility.

## 日本語

Paper 1Aでは、PRESENCE Guardを単なるレポート生成ツールではなく、claim-flow reference monitorとして評価する。

実装済みの人なし評価は次の通りである。

- P1からP12までの監視化misuse-caseについて、危険fixtureでは検出し、安全fixtureでは対象パターンを検出しないことを確認する。
- 低リスクなNoticer Local構成に対して、manager-visible化、long-term retention化、C5化、employer可視化、productivity label化、cloud processing化のmutationを入れ、PRESENCE scoreが上昇することを確認する。
- runtime guardについて、`allow`、`rewrite`、`deny` の各fixtureを確認する。
- dangerous claim literalを検出するstatic claim scannerを確認する。positive bypass fixtureは検出し、Guard統合済みappは通過する。
- 健康経営・プレゼンティーズム可視化系の公開機能profileから作ったpublic-information reference benchmarkを確認する。
- invalid policy rejection、署名付きpolicyの改ざん拒否、未知severityの拒否、bypass検出、fuzz negative test、no-network core scan、依存面の確認、SBOM文書化を行う。
- Web/JavaScript、TypeScript、Dart/Flutter、C FFI、CLI、CI/action、browser reference-monitor demo、third-party templateの組み込み形態を示す。
- Python reference engineのdecision latencyと、Rust no-network coreのrelease artifact sizeを測定する。

再現用コマンドは次である。

```powershell
python presence-tests\run_presence_evaluation.py --output analysis\outputs\presence_evaluation.json
```

個別のmicro-benchmarkは次で実行できる。

```powershell
python presence-tests\benchmark_guard.py --output analysis\outputs\presence_overhead.json
```

この評価は、危険fixtureの検出、安全fixtureでの非検出、危険mutationによるscore上昇、高リスクruntime claimのdeny/rewrite、policy改ざん拒否、demo appにおける直接claim描画の不在、static scannerがbypass fixtureを検出しGuard統合済みappを通過させること、minimized audit logにclaim textとsource signalが含まれないこと、fuzzされた高リスクrequestの非allow、no-network coreにnetwork API呼び出しがないことをすべて満たす場合にのみpassする。

public-information benchmarkは次で実行する。

```powershell
python presence-bench\run_benchmark.py --output presence-bench\reports\benchmark_report.md
```

benchmark profileは公開機能説明から抽象化したものであり、名前の挙がった実在サービスが危険、非準拠、監視的であるとは主張しない。

## 日本語

Paper 1Aでは、PRESENCE Guardをツールチェーンとして評価する。

評価計画は次である。

- P1-P12のパターン検出。
- policy mutation testing。
- Web/Dart/C統合デモ。
- security hardening checks。
- overhead measurement。

Paper 1Bでは、PRESENCEが高・中・低リスクと判定した構成が、参加者評価の監視感、ラベル押し付け感、自己観察支援効果と対応するかを検証する。
