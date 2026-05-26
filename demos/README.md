# PRESENCE Guard Demos

## English

These demos are abstract reproductions of feature patterns, not copies of real products.

- `risk_dashboard_demo/`: manager dashboard pattern with blocked C5/C6 claim flows.
- `employee_app_demo/`: employee self-observation app pattern with runtime rewrite.
- `noticer_local_guarded_demo/`: low-risk C2 local/self-only reference.

Serve the repository root over local HTTP:

```powershell
python -m http.server 8020 --bind 127.0.0.1
```

Then open:

```text
http://127.0.0.1:8020/demos/risk_dashboard_demo/
http://127.0.0.1:8020/demos/employee_app_demo/
http://127.0.0.1:8020/demos/noticer_local_guarded_demo/
```

## 日本語

これらのdemoは、実在製品のcopyではなく、公開機能パターンを抽象化した再現UIである。

- `risk_dashboard_demo/`: C5/C6 claim-flowをblockするmanager dashboard pattern。
- `employee_app_demo/`: runtime rewriteを示す従業員向けself-observation app pattern。
- `noticer_local_guarded_demo/`: 低リスクなC2 local/self-only reference。
