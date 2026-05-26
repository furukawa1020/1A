//! No-network PRESENCE Guard core.
//!
//! This crate is intentionally small: it performs deterministic claim decisions
//! and does not contain networking, dynamic evaluation, file I/O, or policy
//! download logic.

#![forbid(unsafe_code)]

pub const PRESENCE_DECISION_ALLOW: u8 = 0;
pub const PRESENCE_DECISION_REWRITE: u8 = 1;
pub const PRESENCE_DECISION_DENY: u8 = 2;

pub const PRESENCE_REASON_ALLOWED: u8 = 0;
pub const PRESENCE_REASON_UNKNOWN_SEVERITY: u8 = 1;
pub const PRESENCE_REASON_HEALTH_TO_PRODUCTIVITY: u8 = 2;
pub const PRESENCE_REASON_AUTHORITY_BOUNDARY: u8 = 3;
pub const PRESENCE_REASON_PERSISTENT_ADMIN_RECORD: u8 = 4;
pub const PRESENCE_REASON_INTERPRETATION_AUTHORITY: u8 = 5;
pub const PRESENCE_REASON_DENY_BY_DEFAULT: u8 = 6;

pub const PRESENCE_C0_NO_CLAIM: u8 = 0;
pub const PRESENCE_C1_SENSOR_CUE: u8 = 1;
pub const PRESENCE_C2_PATTERN_CUE: u8 = 2;
pub const PRESENCE_C3_BEHAVIORAL_CLAIM: u8 = 3;
pub const PRESENCE_C4_PSYCHOLOGICAL_CLAIM: u8 = 4;
pub const PRESENCE_C5_PRODUCTIVITY_CLAIM: u8 = 5;
pub const PRESENCE_C6_ADMINISTRATIVE_CLAIM: u8 = 6;

pub const PRESENCE_AUDIENCE_SELF: u8 = 0;

pub const PRESENCE_RETENTION_NONE: u8 = 0;
pub const PRESENCE_RETENTION_SESSION: u8 = 1;
pub const PRESENCE_RETENTION_LONG_TERM: u8 = 2;

pub const PRESENCE_CLAIM_PATTERN: u8 = 0;
pub const PRESENCE_CLAIM_BEHAVIORAL: u8 = 1;
pub const PRESENCE_CLAIM_PSYCHOLOGICAL: u8 = 2;
pub const PRESENCE_CLAIM_PRODUCTIVITY: u8 = 3;
pub const PRESENCE_CLAIM_ADMINISTRATIVE: u8 = 4;

pub const PRESENCE_ACTIONABILITY_NONE: u8 = 0;
pub const PRESENCE_ACTIONABILITY_SELF_REFLECTION: u8 = 1;

#[repr(C)]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct PresenceClaimRequest {
    pub severity: u8,
    pub audience: u8,
    pub retention: u8,
    pub claim_type: u8,
    pub uses_health_signal: u8,
    pub actionability: u8,
}

#[repr(C)]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct PresenceDecision {
    pub decision: u8,
    pub allowed: u8,
    pub reason_code: u8,
    pub suggested_severity: u8,
}

fn is_known_severity(severity: u8) -> bool {
    severity <= PRESENCE_C6_ADMINISTRATIVE_CLAIM
}

fn is_allowed_actionability(actionability: u8) -> bool {
    matches!(
        actionability,
        PRESENCE_ACTIONABILITY_NONE | PRESENCE_ACTIONABILITY_SELF_REFLECTION
    )
}

fn make_decision(decision: u8, reason_code: u8) -> PresenceDecision {
    PresenceDecision {
        decision,
        allowed: u8::from(decision == PRESENCE_DECISION_ALLOW),
        reason_code,
        suggested_severity: PRESENCE_C2_PATTERN_CUE,
    }
}

/// Decide whether a proposed claim may be rendered.
///
/// Default policy:
/// - deny unknown severities
/// - deny health-signal to productivity-claim conversion
/// - deny authority-visible claims
/// - deny persistent psychological/productivity/administrative records
/// - allow only C0-C2 self-only non-assertive cues
/// - rewrite higher self-only session claims to C2
#[no_mangle]
pub extern "C" fn presence_request_claim_core(request: PresenceClaimRequest) -> PresenceDecision {
    if !is_known_severity(request.severity) {
        return make_decision(
            PRESENCE_DECISION_DENY,
            PRESENCE_REASON_UNKNOWN_SEVERITY,
        );
    }

    if request.uses_health_signal != 0 && request.claim_type == PRESENCE_CLAIM_PRODUCTIVITY {
        return make_decision(
            PRESENCE_DECISION_DENY,
            PRESENCE_REASON_HEALTH_TO_PRODUCTIVITY,
        );
    }

    if request.audience != PRESENCE_AUDIENCE_SELF {
        return make_decision(
            PRESENCE_DECISION_DENY,
            PRESENCE_REASON_AUTHORITY_BOUNDARY,
        );
    }

    if request.retention == PRESENCE_RETENTION_LONG_TERM
        && matches!(
            request.claim_type,
            PRESENCE_CLAIM_PSYCHOLOGICAL
                | PRESENCE_CLAIM_PRODUCTIVITY
                | PRESENCE_CLAIM_ADMINISTRATIVE
        )
    {
        return make_decision(
            PRESENCE_DECISION_DENY,
            PRESENCE_REASON_PERSISTENT_ADMIN_RECORD,
        );
    }

    if !is_allowed_actionability(request.actionability) {
        return make_decision(PRESENCE_DECISION_DENY, PRESENCE_REASON_DENY_BY_DEFAULT);
    }

    if request.severity <= PRESENCE_C2_PATTERN_CUE
        && matches!(
            request.retention,
            PRESENCE_RETENTION_NONE | PRESENCE_RETENTION_SESSION
        )
    {
        return make_decision(PRESENCE_DECISION_ALLOW, PRESENCE_REASON_ALLOWED);
    }

    if matches!(
        request.retention,
        PRESENCE_RETENTION_NONE | PRESENCE_RETENTION_SESSION
    ) {
        return make_decision(
            PRESENCE_DECISION_REWRITE,
            PRESENCE_REASON_INTERPRETATION_AUTHORITY,
        );
    }

    make_decision(PRESENCE_DECISION_DENY, PRESENCE_REASON_DENY_BY_DEFAULT)
}

#[no_mangle]
pub extern "C" fn presence_score_severity(severity: u8) -> i32 {
    if is_known_severity(severity) {
        i32::from(severity)
    } else {
        -1
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn base_request() -> PresenceClaimRequest {
        PresenceClaimRequest {
            severity: PRESENCE_C2_PATTERN_CUE,
            audience: PRESENCE_AUDIENCE_SELF,
            retention: PRESENCE_RETENTION_SESSION,
            claim_type: PRESENCE_CLAIM_PATTERN,
            uses_health_signal: 0,
            actionability: PRESENCE_ACTIONABILITY_SELF_REFLECTION,
        }
    }

    #[test]
    fn allows_c2_self_session_cue() {
        let decision = presence_request_claim_core(base_request());
        assert_eq!(decision.decision, PRESENCE_DECISION_ALLOW);
        assert_eq!(decision.allowed, 1);
    }

    #[test]
    fn rewrites_high_self_claim() {
        let mut request = base_request();
        request.severity = PRESENCE_C4_PSYCHOLOGICAL_CLAIM;
        request.claim_type = PRESENCE_CLAIM_PSYCHOLOGICAL;
        let decision = presence_request_claim_core(request);
        assert_eq!(decision.decision, PRESENCE_DECISION_REWRITE);
        assert_eq!(decision.reason_code, PRESENCE_REASON_INTERPRETATION_AUTHORITY);
    }

    #[test]
    fn denies_health_signal_to_productivity_claim() {
        let mut request = base_request();
        request.severity = PRESENCE_C5_PRODUCTIVITY_CLAIM;
        request.claim_type = PRESENCE_CLAIM_PRODUCTIVITY;
        request.uses_health_signal = 1;
        let decision = presence_request_claim_core(request);
        assert_eq!(decision.decision, PRESENCE_DECISION_DENY);
        assert_eq!(decision.reason_code, PRESENCE_REASON_HEALTH_TO_PRODUCTIVITY);
    }

    #[test]
    fn denies_authority_boundary_crossing() {
        let mut request = base_request();
        request.audience = 1;
        let decision = presence_request_claim_core(request);
        assert_eq!(decision.decision, PRESENCE_DECISION_DENY);
        assert_eq!(decision.reason_code, PRESENCE_REASON_AUTHORITY_BOUNDARY);
    }
}
