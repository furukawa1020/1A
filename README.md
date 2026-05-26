# PRESENCE Guard

## English

PRESENCE Guard is claim-capability enforcement middleware for presenteeism support systems.

The project does not detect presenteeism, diagnose stress or mental health, evaluate productivity, or judge whether any real service is unsafe. Instead, it treats system-generated claims as security/privacy control objects and controls when a support system may render, export, retain, or expose those claims.

The central question is:

> When do claims generated for self-observation cross authority and interpretation boundaries and become monitoring, labeling, or assessment?

## 日本語

PRESENCE Guardは、プレゼンティーズム支援システムのためのclaim-capability enforcement middlewareである。

本プロジェクトは、プレゼンティーズムの検出、ストレスやメンタルヘルスの診断、生産性評価、実在サービスの安全性判定を目的としない。代わりに、システムが生成する状態claimをセキュリティ/プライバシー上の制御対象として扱い、支援システムがそれらのclaimをいつ表示・出力・保存・権限者へ可視化してよいかを制御する。

中心的な問いは次である。

> 自己観察のために生成されたclaimは、いつauthority boundaryとinterpretation boundaryを越えて、監視・ラベリング・査定へ転化するのか。

## Repository Layout / 構成

- `presence-core/`: Rust no-network decision core, C ABI, and WASM package.
- `presence-sdk-js/`: Web/JavaScript runtime Guard SDK.
- `presence-sdk-ts/`: TypeScript SDK with generated `dist/` output.
- `presence-sdk-dart/`: Dart/Flutter API sketch.
- `presence-ffi-c/`: embedded-style C ABI and demo.
- `presence-policy/`: default deny-by-default policy and policy bundles.
- `presence-audit/`: YAML audit, runtime guard command, static claim scanner, policy signing, reports, and GitHub Action.
- `presence-bench/`: public-information reference profiles and benchmark reports.
- `presence-security/`: threat model, logging design, policy signing design, SBOM, and security requirements.
- `presence-tests/`: evaluation, quickstart, benchmark, demo, fuzz, and security checks.
- `templates/`: third-party quickstart and migration templates.
- `demos/`: touchable demos and benchmark playground.
- `paper/`: paper sections and result templates.
- `docs/`: design notes, architecture, evaluation, adoption, and public reference profile documentation.
- `app/`: Paper 1B scenario-testbed prototype retained for later human validation.

## Five-Minute Quickstart / 5分クイックスタート

Run a low-risk template audit:

```powershell
python presence-audit\cli\presence_audit.py audit templates\self_observation_local_only\presence.yaml --fail-on HIGH
```

Scan the template for direct dangerous claim literals:

```powershell
python presence-audit\cli\presence_audit.py scan templates\self_observation_local_only --fail-on HIGH
```

Compare unsafe and mitigated migration profiles:

```powershell
python presence-audit\cli\presence_audit.py audit templates\local_assertive_to_non_assertive_migration\before.presence.yaml
python presence-audit\cli\presence_audit.py audit templates\local_assertive_to_non_assertive_migration\after.presence.yaml --fail-on HIGH
```

日本語: 低リスクtemplateの監査、危険claim文字列のscan、危険設計から安全設計へのmigration例を上の3手順で確認できる。

## Touch The Demos / デモを触る

Serve the repository root:

```powershell
python -m http.server 8020 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:8020/demos/bench_playground/
http://127.0.0.1:8020/demos/risk_dashboard_demo/
http://127.0.0.1:8020/demos/employee_app_demo/
http://127.0.0.1:8020/demos/noticer_local_guarded_demo/
```

The demos are abstract reproductions of public feature patterns, not copies or assessments of real services.

日本語: demoは実在サービスのcopyや評価ではなく、公開機能パターンを抽象化した再現UIである。`bench_playground` ではprofile選択、Guard判定、mitigation適用を触れる。

## Benchmark / ベンチマーク

Run the public-information reference benchmark:

```powershell
python presence-bench\run_benchmark.py --output presence-bench\reports\benchmark_report.md --json-output presence-bench\reports\benchmark_report.json
```

Profiles:

- `presenteeism_survey_dashboard`
- `employee_app_manager_dashboard`
- `health_data_labor_risk_dashboard`
- `stress_check_high_risk_extraction`
- `productivity_loss_visualization`
- `noticer_local_low_risk`

日本語: `presence-bench` は公開機能説明から抽象化したreference profileを用いる。実在サービスを攻撃・診断・順位付けするものではない。

## Full Evaluation / 全評価

Run the Paper 1A non-human evaluation:

```powershell
python presence-tests\run_presence_evaluation.py --output analysis\outputs\presence_evaluation.json
python presence-tests\benchmark_guard.py --output analysis\outputs\presence_overhead.json
```

Run third-party quickstart verification:

```powershell
python presence-tests\third_party_quickstart.py
```

Run demo HTTP and screenshot smoke tests:

```powershell
python presence-tests\demo_smoke_test.py --screenshots
```

日本語: Paper 1Aは人なし評価として、misuse-case detection、policy mutation、runtime decision、static scan、public benchmark、quickstart、demo smoke test、minimal logging、WASM/TS/Rust/C確認を行う。

## SDK/Core Verification / SDK・core確認

TypeScript:

```powershell
npm.cmd --prefix presence-sdk-ts install --no-audit --no-fund
npm.cmd --prefix presence-sdk-ts run typecheck
npm.cmd --prefix presence-sdk-ts run build
```

Rust and WASM:

```powershell
cargo test --manifest-path presence-core\Cargo.toml
cargo build --manifest-path presence-core\Cargo.toml --release --target wasm32-unknown-unknown
Copy-Item presence-core\target\wasm32-unknown-unknown\release\presence_core.wasm presence-core\pkg\presence_core.wasm -Force
```

WASM loader check:

```powershell
node --input-type=module -e "import fs from 'node:fs/promises'; import { decodeDecision } from './presence-core/pkg/presence_core_wasm_loader.js'; const bytes=await fs.readFile('presence-core/pkg/presence_core.wasm'); const wasm=await WebAssembly.instantiate(bytes,{}); console.log(decodeDecision(wasm.instance.exports.presence_request_claim_code(2,0,1,0,0,1)));"
```

C embedded demo:

```powershell
gcc presence-ffi-c\src\presence_guard.c presence-ffi-c\examples\embedded_gateway.c -o presence-ffi-c\examples\embedded_gateway_build.exe
presence-ffi-c\examples\embedded_gateway_build.exe
```

## Policy Signing / Policy署名

Generate keys, sign, and verify:

```powershell
python presence-audit\cli\presence_audit.py generate-keypair --private-key analysis\outputs\policy.private.json --public-key analysis\outputs\policy.public.json
python presence-audit\cli\presence_audit.py sign-policy-asym presence-policy\presence.guard.policy.json --private-key analysis\outputs\policy.private.json --output analysis\outputs\presence.guard.asym.bundle.json
python presence-audit\cli\presence_audit.py verify-policy-asym analysis\outputs\presence.guard.asym.bundle.json --public-key analysis\outputs\policy.public.json
```

日本語: 非対称署名は研究prototypeである。本番運用では監査済み暗号library、managed keys、key rotation、provenance、secure update frameworkを使うべきである。

## CI Gate / CIゲート

```yaml
- uses: ./presence-audit/action
  with:
    config: presence.yaml
    fail-on: HIGH
    scan-paths: "src app"
    scan-fail-on: HIGH
```

This combines design audit, static dangerous-claim scanning, and CI failure on high-risk claim-flow.

日本語: 設計監査、危険claim文字列のstatic scan、高リスクclaim-flowでのCI失敗を組み合わせる。

## Non-Goals / 非目的

This project must not claim that it can:

- detect actual presenteeism,
- diagnose stress or mental health,
- evaluate productivity,
- improve health outcomes,
- prove that cloud processing or manager visibility is always harmful,
- assess or rank real services.

日本語: 本プロジェクトは、実際のプレゼンティーズム検出、ストレス/メンタルヘルス診断、生産性評価、健康アウトカム改善、クラウド処理や管理者可視性の一律有害性、実在サービスの評価や順位付けを主張してはならない。
