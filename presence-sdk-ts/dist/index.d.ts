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
declare const CLAIM_SCORES: Record<ClaimSeverity, number>;
export declare class PresenceGuard {
    private readonly policy;
    constructor(policy?: PresencePolicy);
    static fromPolicy(policy: PresencePolicy): PresenceGuard;
    requestClaim(request: ClaimRequest): ClaimDecision;
}
export { CLAIM_SCORES };
