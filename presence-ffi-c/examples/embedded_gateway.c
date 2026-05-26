#include "../include/presence_guard.h"
#include <stdio.h>

int main(void) {
  presence_claim_request_t request = {
    .severity = PRESENCE_C2_PATTERN_CUE,
    .audience = PRESENCE_AUDIENCE_SELF,
    .retention = PRESENCE_RETENTION_NONE,
    .is_productivity_claim = 0,
    .is_psychological_claim = 0,
    .uses_health_signal = 0
  };

  presence_decision_t decision = presence_request_claim(&request);
  printf("allowed=%d rewrite=%d reason=%s\n", decision.allowed, decision.rewrite, decision.reason);
  return decision.allowed ? 0 : 1;
}
