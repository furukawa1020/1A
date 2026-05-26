# PRESENCE Guard Minimal Logging

## English

PRESENCE logs must not become a new surveillance record. A denied claim can itself reveal sensitive state or organizational intent. Therefore, PRESENCE audit events store only policy-level metadata:

- decision
- reason rule ids or reason labels
- proposed severity
- claim type
- audience class
- retention class

PRESENCE audit events must not store:

- claim text
- raw signals
- source signal names when they reveal health state
- user identifiers
- timestamps precise enough to reconstruct work rhythm unless operationally required
- manager-facing report content

The CLI supports minimized log output:

```powershell
python presence-audit\cli\presence_audit.py guard presence-policy\presence.guard.policy.json presence-tests\fixtures\request_productivity_manager.json --log-output analysis\outputs\guard_event.min.json
```

## 日本語

PRESENCEのlogは、新しい監視記録になってはいけない。denyされたclaim自体が、機微な状態や組織側の意図を示しうる。そのため、PRESENCE audit eventはpolicy-level metadataだけを保存する。

- decision
- reason rule idまたはreason label
- proposed severity
- claim type
- audience class
- retention class

PRESENCE audit eventが保存してはいけないもの:

- claim text
- raw signal
- health stateを示しうるsource signal name
- user identifier
- 業務リズムを復元できるほど精密なtimestamp。ただし運用上必須の場合を除く
- manager-facing report content

CLIはminimized log outputをサポートする。

```powershell
python presence-audit\cli\presence_audit.py guard presence-policy\presence.guard.policy.json presence-tests\fixtures\request_productivity_manager.json --log-output analysis\outputs\guard_event.min.json
```
