# PRESENCE Guard Architecture / PRESENCE Guardアーキテクチャ

## English

PRESENCE Guard is a claim-capability enforcement middleware.

Applications should not render state claims directly. They should call:

```javascript
guard.requestClaim({
  sourceSignals: ["heart_rate", "keyboard_activity"],
  proposedText: "High stress detected",
  proposedSeverity: "C4",
  claimType: "psychological",
  audience: "self",
  retention: "session",
  actionability: "self_reflection"
});
```

The guard returns:

- `allow`
- `rewrite`
- `deny`
- `require_consent`

## Reference Monitor Flow

```text
Application / Interface
  -> requestClaim()
PRESENCE Runtime Guard
  -> Policy Bundle
  -> Claim Severity Engine
  -> Authority Boundary Checker
  -> Retention / Export Checker
Decision: allow / rewrite / deny / require consent
```

## Presenteeism-Specific Invariants

- Health signal must not become productivity claim.
- Self-observation claim must not cross authority boundary.
- Temporary state must not become persistent administrative record.
- Psychological claim requires explicit capability.
- Non-diagnostic systems must not produce quasi-diagnostic labels.
- User must retain interpretation authority.

## 日本語

PRESENCE Guard は claim-capability enforcement middleware である。

アプリケーションは状態claimを直接表示してはいけない。次のようにGuardを呼ぶ。

```javascript
guard.requestClaim({
  sourceSignals: ["heart_rate", "keyboard_activity"],
  proposedText: "High stress detected",
  proposedSeverity: "C4",
  claimType: "psychological",
  audience: "self",
  retention: "session",
  actionability: "self_reflection"
});
```

Guardは次を返す。

- `allow`
- `rewrite`
- `deny`
- `require_consent`

## Reference Monitor Flow

```text
Application / Interface
  -> requestClaim()
PRESENCE Runtime Guard
  -> Policy Bundle
  -> Claim Severity Engine
  -> Authority Boundary Checker
  -> Retention / Export Checker
Decision: allow / rewrite / deny / require consent
```

## プレゼンティーズム特有の不変条件

- 健康信号から生産性claimを生成してはいけない。
- 自己観察claimはauthority boundaryを越えてはいけない。
- 一時状態を永続的な管理記録にしてはいけない。
- 心理claimには明示capabilityが必要である。
- 非診断システムは疑似診断ラベルを生成してはいけない。
- ユーザーは解釈権を保持しなければならない。

