#include "../include/presence_guard.h"

presence_decision_t presence_request_claim(const presence_claim_request_t *request) {
  presence_decision_t decision = {0, 0, "deny by default"};

  if (!request) {
    decision.reason = "missing request";
    return decision;
  }

  if (request->uses_health_signal && request->is_productivity_claim) {
    decision.reason = "health signal must not become productivity claim";
    return decision;
  }

  if (request->audience != PRESENCE_AUDIENCE_SELF) {
    decision.reason = "self-observation claim crosses authority boundary";
    return decision;
  }

  if (request->retention == PRESENCE_RETENTION_LONG_TERM &&
      (request->is_productivity_claim || request->is_psychological_claim)) {
    decision.reason = "temporary state must not become persistent administrative record";
    return decision;
  }

  if (request->severity <= PRESENCE_C2_PATTERN_CUE &&
      request->audience == PRESENCE_AUDIENCE_SELF &&
      request->retention != PRESENCE_RETENTION_LONG_TERM) {
    decision.allowed = 1;
    decision.rewrite = 0;
    decision.reason = "allowed";
    return decision;
  }

  decision.allowed = 0;
  decision.rewrite = 1;
  decision.reason = "rewrite to C2 non-assertive cue";
  return decision;
}

