#include "../../presence-ffi-c/include/presence_guard.h"

void show_soft_cue(void);
void show_neutral_idle_state(void);

void evaluate_gateway_cue(void) {
  presence_claim_request_t request = {
    .severity = PRESENCE_C2_PATTERN_CUE,
    .audience = PRESENCE_AUDIENCE_SELF,
    .retention = PRESENCE_RETENTION_NONE,
    .is_productivity_claim = 0,
    .is_psychological_claim = 0,
    .uses_health_signal = 0
  };

  presence_decision_t decision = presence_request_claim(&request);
  if (decision.allowed) {
    show_soft_cue();
  } else {
    show_neutral_idle_state();
  }
}
