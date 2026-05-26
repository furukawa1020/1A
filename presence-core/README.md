# presence-core

## English

`presence-core` defines the runtime decision model for PRESENCE Guard.

PRESENCE Guard is a claim reference monitor. Applications should not render state claims directly. They should submit a claim request to the guard and follow the decision:

- `allow`
- `rewrite`
- `deny`
- `require_consent`

The default policy is deny-by-default and caps self-observation output at C2 pattern-level non-assertive cues.

## 日本語

`presence-core` は PRESENCE Guard の実行時判定モデルを定義する。

PRESENCE Guard は claim reference monitor である。アプリケーションは状態claimを直接表示せず、claim request をGuardに渡し、次の判定に従う。

- `allow`
- `rewrite`
- `deny`
- `require_consent`

標準ポリシーはdeny-by-defaultであり、自己観察出力をC2のパターンレベル非断定手がかりに制限する。

