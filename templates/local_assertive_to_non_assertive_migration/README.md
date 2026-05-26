# Local Assertive to Non-Assertive Migration

## English

This migration template shows a concrete before/after change. The unsafe version emits a C4 psychological claim. The safe version keeps the system local and self-only, but rewrites the output as a C2 pattern-level cue.

Run:

```powershell
python presence-audit\cli\presence_audit.py audit templates\local_assertive_to_non_assertive_migration\before.presence.yaml
python presence-audit\cli\presence_audit.py audit templates\local_assertive_to_non_assertive_migration\after.presence.yaml --fail-on HIGH
```

## 日本語

このmigration templateは、危険な設計から安全側へ移す具体例である。beforeはC4 psychological claimを出す。afterはlocal/self-onlyを維持しつつ、出力をC2 pattern-level cueへ書き換える。
