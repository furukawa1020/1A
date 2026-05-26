# presence-core

## English

`presence-core` defines the runtime decision model for PRESENCE Guard.

PRESENCE Guard is a claim reference monitor. Applications should not render state claims directly. They should submit a claim request to the guard and follow the decision:

- `allow`
- `rewrite`
- `deny`
- `require_consent`

The default policy is deny-by-default and caps self-observation output at C2 pattern-level non-assertive cues.

The Rust crate is the no-network decision core. It contains no policy download, remote update, dynamic evaluation, or telemetry path. Networked loading belongs outside the core and must feed an already selected policy/request into the reference monitor.

Run:

```powershell
cargo test --manifest-path presence-core\Cargo.toml
cargo build --manifest-path presence-core\Cargo.toml --release
```

## 日本語

`presence-core` はPRESENCE Guardの実行時判定モデルを定義する。

PRESENCE Guardはclaim reference monitorである。アプリケーションは状態claimを直接表示せず、claim requestをGuardへ渡し、次の判定に従う。

- `allow`
- `rewrite`
- `deny`
- `require_consent`

標準policyはdeny-by-defaultであり、本人向け自己観察出力をC2のpattern-level non-assertive cueまでに制限する。

Rust crateはno-network decision coreである。policy download、remote update、dynamic evaluation、telemetry pathを含まない。ネットワークを使う読み込み処理はcoreの外側に置き、選択済みのpolicy/requestだけをreference monitorへ渡す。

実行コマンドは次である。

```powershell
cargo test --manifest-path presence-core\Cargo.toml
cargo build --manifest-path presence-core\Cargo.toml --release
```

## 日本語

`presence-core` は PRESENCE Guard の実行時判定モデルを定義する。

PRESENCE Guard は claim reference monitor である。アプリケーションは状態claimを直接表示せず、claim request をGuardに渡し、次の判定に従う。

- `allow`
- `rewrite`
- `deny`
- `require_consent`

標準ポリシーはdeny-by-defaultであり、自己観察出力をC2のパターンレベル非断定手がかりに制限する。
