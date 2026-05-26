# Third-Party Adoption Guide

## English

PRESENCE Guard is intended to be copied into other presenteeism support, well-being support, and self-observation projects. A third-party project should integrate three layers:

1. Runtime Guard: call `requestClaim()` before rendering a state claim.
2. Static Claim Scanner: run `presence-audit scan src --fail-on HIGH` in local development and CI.
3. Build Gate: run the GitHub Action with both `config` and `scan-paths`.

Minimal GitHub Action:

```yaml
name: PRESENCE Guard

on:
  pull_request:
    paths:
      - "presence.yaml"
      - "src/**"

jobs:
  presence:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./presence-audit/action
        with:
          config: presence.yaml
          fail-on: HIGH
          scan-paths: "src"
          scan-fail-on: HIGH
```

Recommended migration path:

- Replace assertive C3-C6 labels with `requestClaim()`.
- Cap default user-facing output at C2.
- Remove manager/teacher/employer visibility from self-observation claims.
- Limit retention to `none` or `session`.
- Log only policy-level metadata, not claim text or user state.

## 日本語

PRESENCE Guardは、他のプレゼンティーズム支援、well-being支援、自己観察projectへ組み込めることを目標にしている。第三者projectでは、次の3層を導入する。

1. Runtime Guard: 状態claimを表示する前に `requestClaim()` を呼ぶ。
2. Static Claim Scanner: local developmentとCIで `presence-audit scan src --fail-on HIGH` を実行する。
3. Build Gate: GitHub Actionで `config` と `scan-paths` の両方を指定する。

最小GitHub Action:

```yaml
name: PRESENCE Guard

on:
  pull_request:
    paths:
      - "presence.yaml"
      - "src/**"

jobs:
  presence:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./presence-audit/action
        with:
          config: presence.yaml
          fail-on: HIGH
          scan-paths: "src"
          scan-fail-on: HIGH
```

推奨migration path:

- 断定的なC3-C6 labelを `requestClaim()` に置き換える。
- 利用者向けの標準出力をC2までに制限する。
- 自己観察claimからmanager/teacher/employer visibilityを外す。
- retentionを `none` または `session` に限定する。
- claim textやuser stateではなく、policy-level metadataだけをlogする。
