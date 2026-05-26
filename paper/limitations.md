# Limitations / 限界

## English

- The public reference benchmark is derived from public feature descriptions, not from logged-in product screens, private documentation, API probing, or vulnerability testing.
- The benchmark profiles are abstractions. They must not be read as claims that named vendors are unsafe, non-compliant, or surveillance-oriented.
- PRESENCE Guard controls claim output and claim-flow policy. It does not detect actual presenteeism, diagnose stress or mental health, or evaluate productivity.
- The current asymmetric signature implementation is a research prototype. Production deployments should use audited cryptographic libraries, managed keys, key rotation, provenance, and a secure update framework.
- The WASM package exposes a low-level scalar API. Higher-level language bindings should be audited before production use.
- Static scanning can miss dynamically generated claims and can flag intentional dangerous strings in benchmark demos. CI should scope scan paths to application/SDK code and keep benchmark corpora separate.
- Paper 1A is a tool and benchmark evaluation. Human perception and usability validation belongs to Paper 1B.

## 日本語

- Public reference benchmarkは、公開機能説明から作ったものであり、ログイン後画面、private document、API probing、vulnerability testingに基づくものではない。
- Benchmark profileは抽象化である。名前の挙がったvendorが危険、非準拠、監視的であるという主張として読んではいけない。
- PRESENCE Guardはclaim outputとclaim-flow policyを制御する。実際のpresenteeism検出、stress/mental health診断、生産性評価は行わない。
- 現在のasymmetric signature実装は研究prototypeである。本番運用では、監査済みcryptographic library、managed key、key rotation、provenance、secure update frameworkを使うべきである。
- WASM packageはlow-level scalar APIを公開する。高水準language bindingは本番利用前に監査が必要である。
- Static scanningは動的生成claimを見逃す可能性があり、benchmark demo内の意図的な危険文字列を検出する。CIではapplication/SDK codeをscan対象にし、benchmark corpusは分けるべきである。
- Paper 1Aはtoolとbenchmarkの評価である。人間の知覚・usability validationはPaper 1Bで扱う。
