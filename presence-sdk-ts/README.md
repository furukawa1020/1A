# @presence/guard TypeScript SDK

## English

This package provides the TypeScript shape of the PRESENCE Guard runtime API.

Applications call `requestClaim()` before rendering state claims. The SDK returns `allow`, `rewrite`, or `deny` according to claim severity, audience, retention, actionability, capabilities, and presenteeism-specific invariants.

The TypeScript SDK intentionally keeps network loading outside the core class. A host application may load a pinned policy by its own trusted mechanism, then pass the policy object to `PresenceGuard.fromPolicy(policy)`.

```ts
import { PresenceGuard } from "@presence/guard";

const guard = PresenceGuard.fromPolicy(policy);
const decision = guard.requestClaim({
  sourceSignals: ["keyboard_rhythm"],
  proposedText: "Concentration has decreased",
  proposedSeverity: "C3",
  claimType: "behavioral",
  audience: "self",
  retention: "session",
  actionability: "self_reflection"
});
```

## 日本語

このpackageは、PRESENCE Guard runtime APIのTypeScript形状を提供する。

アプリケーションは状態claimを表示する前に `requestClaim()` を呼ぶ。SDKはclaim severity、audience、retention、actionability、capability、プレゼンティーズム特有の不変条件に基づいて、`allow`、`rewrite`、`deny` を返す。

TypeScript SDKでは、network loadingをcore classの外側に置く。host applicationは自分の信頼できる仕組みで固定済みpolicyを読み込み、そのpolicy objectを `PresenceGuard.fromPolicy(policy)` に渡す。
