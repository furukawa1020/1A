# presence-policy

## English

This directory contains the default PRESENCE Guard policy.

The default policy is deny-by-default and enforces:

- no health-signal-to-productivity claim,
- no self-observation claim crossing authority boundary,
- no temporary state becoming persistent administrative record,
- no psychological claim without explicit capability,
- no quasi-diagnostic label in non-diagnostic systems,
- user interpretation authority retained by capping default claims at C2.

Prototype policy bundles can be HMAC-signed by the CLI for local research use. Production use should replace this with asymmetric signatures and a secure update mechanism.

## 日本語

このディレクトリには、PRESENCE Guardの標準ポリシーを置く。

標準ポリシーはdeny-by-defaultであり、次を強制する。

- 健康信号から生産性claimを生成しない。
- 自己観察claimをauthority boundary越しに出さない。
- 一時状態を永続的な管理記録にしない。
- 明示capabilityなしに心理claimを出さない。
- 非診断システムで疑似診断ラベルを出さない。
- 標準claimをC2以下に制限し、ユーザーの解釈権を保持する。

CLIは研究用プロトタイプとしてHMAC署名付きpolicy bundleを生成できる。本番利用では、非対称署名と安全な更新機構に置き換えるべきである。

