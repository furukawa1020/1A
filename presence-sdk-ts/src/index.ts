// presence-scan: ignore-file

export type ClaimSeverity = "C0" | "C1" | "C2" | "C3" | "C4" | "C5" | "C6";
export type Audience = "self" | "manager" | "teacher" | "employer" | "evaluator" | "admin" | "organization";
export type Retention = "none" | "session" | "short_term" | "long_term";
export type ClaimType = "pattern" | "behavioral" | "psychological" | "productivity" | "administrative" | "unknown";
export type GuardDecisionKind = "allow" | "rewrite" | "deny" | "require_consent";

export interface PresencePolicy {
  mode?: "deny_by_default" | string;
  max_allowed_severity?: ClaimSeverity;
  allowed_audiences?: Audience[];
  allowed_retention?: Retention[];
  allowed_actionability?: string[];
  capabilities?: Record<string, boolean>;
  invariants?: Record<string, boolean>;
  claim_minimization?: {
    default_rewrite_severity?: ClaimSeverity;
    default_suggested_text?: string;
    default_suggested_text_ja?: string;
  };
}

export interface ClaimRequest {
  sourceSignals?: string[];
  proposedText?: string;
  proposedSeverity: ClaimSeverity;
  claimType?: ClaimType;
  type?: ClaimType;
  audience: Audience;
  retention: Retention;
  actionability: string;
}

export interface ClaimDecision {
  decision: GuardDecisionKind;
  allowed: boolean;
  reason: string[];
  suggestedText?: string;
  suggestedTextJa?: string;
  suggestedSeverity?: ClaimSeverity;
  text?: string;
  severity?: ClaimSeverity;
}

const CLAIM_SCORES: Record<ClaimSeverity, number> = {
  C0: 0,
  C1: 1,
  C2: 2,
  C3: 3,
  C4: 4,
  C5: 5,
  C6: 6
};

const AUTHORITY_AUDIENCES = new Set<Audience>(["manager", "teacher", "employer", "evaluator", "admin", "organization"]);
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

const DEFAULT_POLICY: Required<PresencePolicy> = {
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
  }
};

function normalizePolicy(policy: PresencePolicy): Required<PresencePolicy> {
  return {
    ...DEFAULT_POLICY,
    ...policy,
    capabilities: {
      ...DEFAULT_POLICY.capabilities,
      ...policy.capabilities
    },
    invariants: {
      ...DEFAULT_POLICY.invariants,
      ...policy.invariants
    },
    claim_minimization: {
      ...DEFAULT_POLICY.claim_minimization,
      ...policy.claim_minimization
    }
  };
}

function hasHealthSignal(request: ClaimRequest): boolean {
  return (request.sourceSignals ?? []).some((signal) => HEALTH_SIGNALS.has(signal));
}

function containsDiagnosticTerm(text: string | undefined): boolean {
  const normalized = String(text ?? "").toLowerCase();
  return DIAGNOSTIC_TERMS.some((term) => normalized.includes(term.toLowerCase()));
}

function makeDecision(
  decision: GuardDecisionKind,
  reasons: string[],
  policy: Required<PresencePolicy>,
  extras: Partial<ClaimDecision> = {}
): ClaimDecision {
  return {
    decision,
    allowed: decision === "allow",
    reason: reasons,
    suggestedText: policy.claim_minimization.default_suggested_text,
    suggestedTextJa: policy.claim_minimization.default_suggested_text_ja,
    suggestedSeverity: policy.claim_minimization.default_rewrite_severity,
    ...extras
  };
}

export class PresenceGuard {
  private readonly policy: Required<PresencePolicy>;

  constructor(policy: PresencePolicy = {}) {
    this.policy = normalizePolicy(policy);
  }

  static fromPolicy(policy: PresencePolicy): PresenceGuard {
    return new PresenceGuard(policy);
  }

  requestClaim(request: ClaimRequest): ClaimDecision {
    const reasons: string[] = [];
    const severityScore = CLAIM_SCORES[request.proposedSeverity];
    const maxScore = CLAIM_SCORES[this.policy.max_allowed_severity];
    const claimType = request.claimType ?? request.type ?? "unknown";
    const capabilities = this.policy.capabilities;
    const invariants = this.policy.invariants;

    if (severityScore === undefined) {
      return makeDecision("deny", ["unknown claim severity"], this.policy);
    }

    if (!this.policy.allowed_audiences.includes(request.audience)) {
      reasons.push("audience is not allowed by policy");
    }
    if (!this.policy.allowed_retention.includes(request.retention)) {
      reasons.push("retention is not allowed by policy");
    }
    if (!this.policy.allowed_actionability.includes(request.actionability)) {
      reasons.push("actionability is not allowed by policy");
    }
    if (severityScore > maxScore) {
      reasons.push(`claim severity exceeds policy cap ${this.policy.max_allowed_severity}`);
    }

    if (invariants.health_signal_must_not_become_productivity_claim !== false && hasHealthSignal(request) && claimType === "productivity") {
      reasons.push("health signal must not become productivity claim");
      return makeDecision("deny", reasons, this.policy);
    }
    if (invariants.self_observation_claim_must_not_cross_authority_boundary !== false && AUTHORITY_AUDIENCES.has(request.audience)) {
      reasons.push("self-observation claim crosses authority boundary");
      return makeDecision("deny", reasons, this.policy);
    }
    if (
      invariants.temporary_state_must_not_become_persistent_administrative_record !== false &&
      request.retention === "long_term" &&
      ["administrative", "productivity", "psychological"].includes(claimType)
    ) {
      reasons.push("temporary state must not become persistent administrative record");
      return makeDecision("deny", reasons, this.policy);
    }
    if (invariants.psychological_claim_requires_explicit_capability !== false && claimType === "psychological" && !capabilities.psychological_claims) {
      reasons.push("psychological claim requires explicit capability");
    }
    if (claimType === "productivity" && !capabilities.productivity_claims) {
      reasons.push("productivity claims are disabled");
    }
    if (claimType === "administrative" && !capabilities.administrative_claims) {
      reasons.push("administrative claims are disabled");
    }
    if (invariants.non_diagnostic_system_must_not_produce_quasi_diagnostic_labels !== false && containsDiagnosticTerm(request.proposedText) && !capabilities.diagnostic_labels) {
      reasons.push("non-diagnostic system must not produce quasi-diagnostic labels");
    }
    if (invariants.user_must_retain_interpretation_authority !== false && severityScore > 2) {
      reasons.push("user must retain interpretation authority");
    }

    if (reasons.length === 0) {
      return makeDecision("allow", [], this.policy, {
        text: request.proposedText,
        severity: request.proposedSeverity
      });
    }
    if (request.audience === "self" && request.retention !== "long_term") {
      return makeDecision("rewrite", reasons, this.policy);
    }
    return makeDecision("deny", reasons, this.policy);
  }
}

export { CLAIM_SCORES };
