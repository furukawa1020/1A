import { PresenceGuard } from "../../presence-sdk-ts/src/index";
import policy from "../../presence-policy/presence.guard.policy.json";

const guard = PresenceGuard.fromPolicy(policy);

export function renderSelfObservation(render) {
  const decision = guard.requestClaim({
    sourceSignals: ["keyboard_rhythm"],
    proposedText: "The work flow may have changed slightly",
    proposedSeverity: "C2",
    claimType: "pattern",
    audience: "self",
    retention: "session",
    actionability: "self_reflection"
  });

  if (decision.decision === "allow") {
    render(decision.text);
  } else if (decision.decision === "rewrite") {
    render(decision.suggestedText);
  } else {
    render("No state claim is shown.");
  }
}
