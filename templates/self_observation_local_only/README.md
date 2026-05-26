# Self-Observation Local-Only Template

## English

Use this template for a low-risk self-observation tool. The default design keeps processing local, keeps output self-only, uses session retention, and caps output at C2 non-assertive cues.

Run:

```powershell
python presence-audit\cli\presence_audit.py audit templates\self_observation_local_only\presence.yaml --fail-on HIGH
python presence-audit\cli\presence_audit.py scan templates\self_observation_local_only --fail-on HIGH
```

## 日本語

このtemplateは、低リスクな自己観察ツールの出発点である。標準設計では、処理をローカルに保ち、出力を本人のみに限定し、保存をsessionに限定し、出力をC2の非断定cueまでに抑える。

実行:

```powershell
python presence-audit\cli\presence_audit.py audit templates\self_observation_local_only\presence.yaml --fail-on HIGH
python presence-audit\cli\presence_audit.py scan templates\self_observation_local_only --fail-on HIGH
```
