(function initPresenceGuard(globalScope) {
  // presence-scan: ignore-file
  const CLAIM_SCORES = {
    C0: 0,
    C1: 1,
    C2: 2,
    C3: 3,
    C4: 4,
    C5: 5,
    C6: 6
  };

  const AUTHORITY_AUDIENCES = new Set(["manager", "teacher", "employer", "evaluator", "admin", "organization"]);
  const HEALTH_SIGNALS = new Set(["heart_rate", "sleep", "fatigue", "mood", "self_report", "health_status"]);
  const DIAGNOSTIC_TERMS = [
    "stress",
    "depression",
    "anxiety",
    "burnout",
    "fatigue",
    "高ストレス",
    "うつ",
    "不安",
    "燃え尽き",
    "疲労",
    "危険状態",
    "要対応"
  ];

  function score(severity) {
    return CLAIM_SCORES[severity] ?? null;
  }

  function normalizePolicy(policy) {
    return {
      mode: "deny_by_default",
      max_allowed_severity: "C2",
      allowed_audiences: ["self"],
      allowed_retention: ["none", "session"],
      allowed_actionability: ["self_reflection", "none"],
      capabilities: {},
      invariants: {},
      claim_minimization: {
        default_rewrite_severity: "C2",
        default_suggested_text: "The work flow may have changed slightly. It may be worth briefly checking how you feel.",
        default_suggested_text_ja: "作業の流れに少し変化があるかもしれません。一度、自分の感じを見てもよさそうです。"
      },
      ...policy
    };
  }

  function hasHealthSignal(request) {
    return (request.sourceSignals || []).some((signal) => HEALTH_SIGNALS.has(signal));
  }

  function containsDiagnosticTerm(text) {
    const normalized = String(text || "").toLowerCase();
    return DIAGNOSTIC_TERMS.some((term) => normalized.includes(term.toLowerCase()));
  }

  function authorityAudience(audience) {
    if (Array.isArray(audience)) {
      return audience.some((item) => AUTHORITY_AUDIENCES.has(item));
    }
    return AUTHORITY_AUDIENCES.has(audience);
  }

  function makeDecision(decision, reasons, policy, extras) {
    const min = policy.claim_minimization || {};
    return {
      decision,
      allowed: decision === "allow",
      reason: reasons,
      suggestedText: min.default_suggested_text,
      suggestedTextJa: min.default_suggested_text_ja,
      suggestedSeverity: min.default_rewrite_severity || "C2",
      ...extras
    };
  }

  class PresenceGuard {
    constructor(policy) {
      this.policy = normalizePolicy(policy || {});
    }

    static async load(urlOrPolicy) {
      if (typeof urlOrPolicy === "string") {
        const response = await fetch(urlOrPolicy, { cache: "no-store" });
        if (!response.ok) {
          throw new Error(`Could not load PRESENCE policy: ${response.status}`);
        }
        return new PresenceGuard(await response.json());
      }
      return new PresenceGuard(urlOrPolicy);
    }

    requestClaim(request) {
      const policy = this.policy;
      const reasons = [];
      const severityScore = score(request.proposedSeverity);
      const maxScore = score(policy.max_allowed_severity || "C2");
      const claimType = request.claimType || request.type || "unknown";
      const audience = request.audience || "unknown";
      const retention = request.retention || "unknown";
      const actionability = request.actionability || "unknown";
      const capabilities = policy.capabilities || {};
      const invariants = policy.invariants || {};

      if (severityScore === null) {
        return makeDecision("deny", ["unknown claim severity"], policy);
      }

      if (!(policy.allowed_audiences || []).includes(audience)) {
        reasons.push("audience is not allowed by policy");
      }

      if (!(policy.allowed_retention || []).includes(retention)) {
        reasons.push("retention is not allowed by policy");
      }

      if (!(policy.allowed_actionability || []).includes(actionability)) {
        reasons.push("actionability is not allowed by policy");
      }

      if (severityScore > maxScore) {
        reasons.push(`claim severity exceeds policy cap ${policy.max_allowed_severity}`);
      }

      if (invariants.health_signal_must_not_become_productivity_claim && hasHealthSignal(request) && claimType === "productivity") {
        reasons.push("health signal must not become productivity claim");
        return makeDecision("deny", reasons, policy);
      }

      if (invariants.self_observation_claim_must_not_cross_authority_boundary && authorityAudience(audience)) {
        reasons.push("self-observation claim crosses authority boundary");
        return makeDecision("deny", reasons, policy);
      }

      if (
        invariants.temporary_state_must_not_become_persistent_administrative_record &&
        retention === "long_term" &&
        ["administrative", "productivity", "psychological"].includes(claimType)
      ) {
        reasons.push("temporary state must not become persistent administrative record");
        return makeDecision("deny", reasons, policy);
      }

      if (
        invariants.psychological_claim_requires_explicit_capability &&
        claimType === "psychological" &&
        !capabilities.psychological_claims
      ) {
        reasons.push("psychological claim requires explicit capability");
      }

      if (claimType === "productivity" && !capabilities.productivity_claims) {
        reasons.push("productivity claims are disabled");
      }

      if (claimType === "administrative" && !capabilities.administrative_claims) {
        reasons.push("administrative claims are disabled");
      }

      if (
        invariants.non_diagnostic_system_must_not_produce_quasi_diagnostic_labels &&
        containsDiagnosticTerm(request.proposedText) &&
        !capabilities.diagnostic_labels
      ) {
        reasons.push("non-diagnostic system must not produce quasi-diagnostic labels");
      }

      if (invariants.user_must_retain_interpretation_authority && severityScore > 2) {
        reasons.push("user must retain interpretation authority");
      }

      if (reasons.length === 0) {
        return makeDecision("allow", [], policy, {
          text: request.proposedText,
          severity: request.proposedSeverity
        });
      }

      if (audience === "self" && retention !== "long_term") {
        return makeDecision("rewrite", reasons, policy);
      }

      return makeDecision("deny", reasons, policy);
    }
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { PresenceGuard, CLAIM_SCORES };
  } else {
    globalScope.PresenceGuard = PresenceGuard;
  }
})(typeof window !== "undefined" ? window : globalThis);
