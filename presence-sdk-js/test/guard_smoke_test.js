const { PresenceGuard } = require("../src/presence-guard.js");
const policy = require("../../presence-policy/presence.guard.policy.json");

const guard = new PresenceGuard(policy);

const highStress = guard.requestClaim({
  sourceSignals: ["heart_rate", "keyboard_activity"],
  proposedText: "High stress detected",
  proposedSeverity: "C4",
  claimType: "psychological",
  audience: "self",
  retention: "session",
  actionability: "self_reflection"
});

const productivityToManager = guard.requestClaim({
  sourceSignals: ["heart_rate"],
  proposedText: "Reduced work efficiency",
  proposedSeverity: "C5",
  claimType: "productivity",
  audience: "manager",
  retention: "long_term",
  actionability: "manager_report"
});

const softCue = guard.requestClaim({
  sourceSignals: ["keyboard_rhythm"],
  proposedText: "The work flow may have changed slightly",
  proposedSeverity: "C2",
  claimType: "pattern",
  audience: "self",
  retention: "session",
  actionability: "self_reflection"
});

if (highStress.decision !== "rewrite") {
  throw new Error(`Expected high stress claim to rewrite, got ${highStress.decision}`);
}
if (productivityToManager.decision !== "deny") {
  throw new Error(`Expected manager productivity claim to deny, got ${productivityToManager.decision}`);
}
if (softCue.decision !== "allow") {
  throw new Error(`Expected soft cue to allow, got ${softCue.decision}`);
}

console.log("PRESENCE Guard smoke tests passed");

