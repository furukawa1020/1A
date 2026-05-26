# PRESENCE Core WASM Package

## English

This folder contains the generated WASM artifact and a tiny JavaScript loader for the no-network PRESENCE decision core.

Build from source:

```powershell
cargo build --manifest-path presence-core\Cargo.toml --release --target wasm32-unknown-unknown
Copy-Item presence-core\target\wasm32-unknown-unknown\release\presence_core.wasm presence-core\pkg\presence_core.wasm
```

Use:

```javascript
import { loadPresenceCoreWasm, decodeDecision } from "./presence_core_wasm_loader.js";

const core = await loadPresenceCoreWasm("./presence_core.wasm");
const code = core.presence_request_claim_code(2, 0, 1, 0, 0, 1);
console.log(decodeDecision(code));
```

## 日本語

このfolderには、no-network PRESENCE decision coreの生成済みWASM artifactと小さなJavaScript loaderを置く。

sourceからbuildする:

```powershell
cargo build --manifest-path presence-core\Cargo.toml --release --target wasm32-unknown-unknown
Copy-Item presence-core\target\wasm32-unknown-unknown\release\presence_core.wasm presence-core\pkg\presence_core.wasm
```

利用例:

```javascript
import { loadPresenceCoreWasm, decodeDecision } from "./presence_core_wasm_loader.js";

const core = await loadPresenceCoreWasm("./presence_core.wasm");
const code = core.presence_request_claim_code(2, 0, 1, 0, 0, 1);
console.log(decodeDecision(code));
```
