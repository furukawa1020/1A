# Abstract / 要旨

## English

Presenteeism support systems aim to help people who continue working or studying while experiencing health-related difficulty. However, such systems can transform support into surveillance when claims about a person's state cross authority boundaries and become visible to managers, teachers, employers, or evaluation processes. This paper introduces PRESENCE, a claim-flow threat modeling and design audit framework for surveillance transmutation in presenteeism support systems. PRESENCE treats system-generated claims, not only raw data, as security/privacy assets. It models claim-flow from signals to features, estimates, labels, claims, recommendations, and administrative actions; introduces authority and interpretation boundaries; defines a claim severity ladder from C0 to C6; catalogs twelve surveillance transmutation patterns; and implements a machine-readable audit toolchain, `presence-audit`, with YAML specifications, CLI analysis, report generation, and CI integration examples. Our goal is not to detect presenteeism or diagnose mental states. Instead, we provide a static security/privacy audit method for identifying when self-observation support risks becoming monitoring, labeling, or assessment, and for generating mitigations before human-subject evaluation.

## 日本語

プレゼンティーズム支援システムは、健康上の困難を抱えながらも働き続ける、または学び続ける人を支援することを目指す。しかし、そのようなシステムは、本人状態に関するclaimがauthority boundaryを越え、管理者、教員、雇用者、評価プロセスに可視化されるとき、支援から監視へ転化しうる。本論文は、プレゼンティーズム支援システムにおける監視化転化のためのclaim-flow脅威モデリングおよび設計監査フレームワークPRESENCEを提案する。PRESENCEは、生データだけでなく、システムが生成するclaimをセキュリティ/プライバシー資産として扱う。信号から特徴量、推定、ラベル、claim、推奨、管理行動に至るclaim-flowをモデル化し、authority boundaryとinterpretation boundaryを導入し、C0からC6までのclaim severity ladderを定義し、12個の監視化転化パターンを整理する。さらに、YAML仕様、CLI解析、レポート生成、CI統合例を備えた機械可読監査ツールチェーン `presence-audit` を実装する。本研究の目的は、プレゼンティーズムを検出することや心理状態を診断することではない。人を対象とした評価の前に、自己観察支援が監視・ラベリング・査定へ転化するリスクを特定し、緩和策を生成する静的なセキュリティ/プライバシー監査手法を提供することである。

