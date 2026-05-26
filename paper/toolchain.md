# Toolchain / ツールチェーン

## English

The implementation artifact is the PRESENCE Guard toolchain, not only `presence-audit`.

It includes:

- `presence-core`: Rust no-network decision core with C ABI and WASM build.
- `presence-sdk-js` and `presence-sdk-ts`: Web/Node SDKs.
- `presence-sdk-dart`: Flutter/Dart API sketch.
- `presence-ffi-c`: embedded C ABI and compiled embedded-style demo.
- `presence-audit`: YAML audit, runtime guard command, static claim scanner, policy signing, report generation, and CI gate.
- `presence-bench`: public-information reference profiles and expected benchmark results.
- `templates`: third-party quickstart and migration templates.
- `demos`: touchable benchmark playground and Guarded reproduction UIs.
- `presence-security`: tool threat model, logging design, policy signing design, SBOM, and security requirements.

The tool can be used as:

```text
python presence-audit/cli/presence_audit.py audit presence-audit/examples/cloud_wellbeing_dashboard.yaml
python presence-audit/cli/presence_audit.py scan app/src presence-sdk-js/src presence-sdk-ts/src --fail-on HIGH
python presence-bench/run_benchmark.py --output presence-bench/reports/benchmark_report.md
```

The WASM core can be built with:

```text
cargo build --manifest-path presence-core/Cargo.toml --release --target wasm32-unknown-unknown
```

The TypeScript SDK can be checked with:

```text
npm --prefix presence-sdk-ts run typecheck
```

## 日本語

実装成果物は `presence-audit` だけではなく、PRESENCE Guard toolchainである。

含まれるものは次である。

- `presence-core`: Rust no-network decision core、C ABI、WASM build。
- `presence-sdk-js` と `presence-sdk-ts`: Web/Node SDK。
- `presence-sdk-dart`: Flutter/Dart API sketch。
- `presence-ffi-c`: embedded C ABIとcompiled embedded-style demo。
- `presence-audit`: YAML audit、runtime guard command、static claim scanner、policy signing、report generation、CI gate。
- `presence-bench`: public-information reference profileとexpected benchmark result。
- `templates`: third-party quickstartとmigration template。
- `demos`: 触れるbenchmark playgroundとGuarded reproduction UI。
- `presence-security`: tool threat model、logging design、policy signing design、SBOM、security requirements。

利用例:

```text
python presence-audit/cli/presence_audit.py audit presence-audit/examples/cloud_wellbeing_dashboard.yaml
python presence-audit/cli/presence_audit.py scan app/src presence-sdk-js/src presence-sdk-ts/src --fail-on HIGH
python presence-bench/run_benchmark.py --output presence-bench/reports/benchmark_report.md
```

WASM coreは次でbuildする。

```text
cargo build --manifest-path presence-core/Cargo.toml --release --target wasm32-unknown-unknown
```

TypeScript SDKは次で確認する。

```text
npm --prefix presence-sdk-ts run typecheck
```

## 日本語

実装成果物は `presence-audit` である。

含まれるものは次である。

- PRESENCE YAML仕様のJSON Schema。
- CLI監査コマンド。
- MarkdownおよびJSONレポート生成。
- システム仕様例。
- GitHub Actionsワークフロー例。

ツールは次のように使える。

```text
python presence-audit/cli/presence_audit.py audit presence-audit/examples/cloud_wellbeing_dashboard.yaml
```
