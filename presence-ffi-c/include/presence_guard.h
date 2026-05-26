#ifndef PRESENCE_GUARD_H
#define PRESENCE_GUARD_H

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
  PRESENCE_C0_NO_CLAIM = 0,
  PRESENCE_C1_SENSOR_CUE = 1,
  PRESENCE_C2_PATTERN_CUE = 2,
  PRESENCE_C3_BEHAVIORAL_CLAIM = 3,
  PRESENCE_C4_PSYCHOLOGICAL_CLAIM = 4,
  PRESENCE_C5_PRODUCTIVITY_CLAIM = 5,
  PRESENCE_C6_ADMINISTRATIVE_CLAIM = 6
} presence_claim_severity_t;

typedef enum {
  PRESENCE_AUDIENCE_SELF = 0,
  PRESENCE_AUDIENCE_MANAGER = 1,
  PRESENCE_AUDIENCE_TEACHER = 2,
  PRESENCE_AUDIENCE_EMPLOYER = 3,
  PRESENCE_AUDIENCE_EVALUATOR = 4
} presence_audience_t;

typedef enum {
  PRESENCE_RETENTION_NONE = 0,
  PRESENCE_RETENTION_SESSION = 1,
  PRESENCE_RETENTION_LONG_TERM = 2
} presence_retention_t;

typedef struct {
  presence_claim_severity_t severity;
  presence_audience_t audience;
  presence_retention_t retention;
  int is_productivity_claim;
  int is_psychological_claim;
  int uses_health_signal;
} presence_claim_request_t;

typedef struct {
  int allowed;
  int rewrite;
  const char *reason;
} presence_decision_t;

presence_decision_t presence_request_claim(const presence_claim_request_t *request);

#ifdef __cplusplus
}
#endif

#endif

