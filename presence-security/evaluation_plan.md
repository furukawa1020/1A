# Evaluation Plan / 評価計画

## English

Paper 1A evaluates the tool, not human perception.

1. Misuse-case detection test: fixtures for P1-P12 should trigger the expected surveillance transmutation pattern.
2. Policy mutation test: changes such as `manager=false -> true`, `session -> long_term`, `C2 -> C5`, and `self -> employer` must increase risk.
3. Integration demo: Web SDK, Dart API sketch, and C ABI sketch show embeddability.
4. Security hardening test: invalid policy rejection, signature verification, negative tests, static syntax checks, dependency minimization.
5. Overhead: future measurement targets include policy load time, decision latency, memory use, and binary size.

## 日本語

Paper 1Aでは、人間の知覚ではなくツールを評価する。

1. Misuse-case detection test: P1-P12のfixtureが期待される監視化パターンを発火するか。
2. Policy mutation test: `manager=false -> true`、`session -> long_term`、`C2 -> C5`、`self -> employer` などの変更でリスクが上がるか。
3. Integration demo: Web SDK、Dart API sketch、C ABI sketchで組み込み可能性を示す。
4. Security hardening test: 不正policy拒否、署名検証、negative test、静的構文チェック、依存最小化。
5. Overhead: 今後、policy load time、decision latency、memory use、binary sizeを測る。

