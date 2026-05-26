# Threat Model

The threat model is not limited to malicious external attackers. Surveillance transmutation can occur under benevolent or organizationally legitimate language such as support, health management, learning support, workplace improvement, early noticing, or well-being.

## Information Assets

- Work or study state data.
- State-related features derived from behavior or interaction.
- System outputs about the user's current state.
- Free-text responses collected during the experiment.
- Condition-level response records.

## Threat Actors

- Managers, teachers, employers, or evaluators.
- Service providers operating cloud or analytics infrastructure.
- Researchers with access to experimental records.
- The system itself when it makes assertive claims about internal state.
- Organizational processes that reuse reports beyond the user's self-support context.

## Trust Boundaries

- User device vs. cloud server.
- Self-only display vs. third-party report.
- Non-assertive cue vs. assertive label.
- Research data collection environment vs. the scenario system being evaluated.

## Transmutation Path

Support intention can transform into surveillance through:

```text
Support Intention
  -> Sensing / Logging
  -> State Inference
  -> Output Claim
  -> Visibility / Sharing
  -> Managerial or Self-surveillance Effect
```

The core security/privacy issue is not only whether data is encrypted or access-controlled. It is also what the system is allowed to claim, where the data is processed, and who can see the result.

