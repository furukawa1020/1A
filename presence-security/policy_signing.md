# PRESENCE Policy Signing

## English

PRESENCE supports two policy signing modes:

1. HMAC prototype for local experiments.
2. Asymmetric RSA prototype for deployment-like evaluation.

The asymmetric mode separates the signing key from the verification key. Private keys must not be committed to the repository.

Generate keys:

```powershell
python presence-audit\cli\presence_audit.py generate-keypair --private-key analysis\outputs\policy.private.json --public-key presence-policy\presence.policy.public.json
```

Sign:

```powershell
python presence-audit\cli\presence_audit.py sign-policy-asym presence-policy\presence.guard.policy.json --private-key analysis\outputs\policy.private.json --output presence-policy\presence.guard.asym.bundle.json
```

Verify:

```powershell
python presence-audit\cli\presence_audit.py verify-policy-asym presence-policy\presence.guard.asym.bundle.json --public-key presence-policy\presence.policy.public.json
```

This is still a research prototype. Production deployments should use audited cryptographic libraries, managed keys, key rotation, provenance, and a secure update framework such as TUF.

## 日本語

PRESENCEは2種類のpolicy signing modeを持つ。

1. local experiment用のHMAC prototype。
2. deployment-like evaluation用のasymmetric RSA prototype。

asymmetric modeでは、署名鍵と検証鍵を分離する。private keyはrepositoryへcommitしてはいけない。

鍵生成:

```powershell
python presence-audit\cli\presence_audit.py generate-keypair --private-key analysis\outputs\policy.private.json --public-key presence-policy\presence.policy.public.json
```

署名:

```powershell
python presence-audit\cli\presence_audit.py sign-policy-asym presence-policy\presence.guard.policy.json --private-key analysis\outputs\policy.private.json --output presence-policy\presence.guard.asym.bundle.json
```

検証:

```powershell
python presence-audit\cli\presence_audit.py verify-policy-asym presence-policy\presence.guard.asym.bundle.json --public-key presence-policy\presence.policy.public.json
```

これは研究prototypeである。本番運用では、監査済み暗号library、managed key、key rotation、provenance、TUFのようなsecure update frameworkを用いるべきである。
