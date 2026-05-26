(async function initEmployeeDemo() {
  const guard = await PresenceGuard.load("../../presence-policy/presence.guard.policy.json");
  const request = {
    sourceSignals: ["heart_rate", "keyboard_rhythm"],
    proposedText: "High stress detected",
    proposedSeverity: "C4",
    claimType: "psychological",
    audience: "self",
    retention: "session",
    actionability: "self_reflection"
  };

  const decision = guard.requestClaim(request);
  const output = document.querySelector("#renderedOutput");
  if (decision.decision === "allow") {
    output.textContent = decision.text;
  } else if (decision.decision === "rewrite") {
    output.textContent = decision.suggestedTextJa || decision.suggestedText;
  } else {
    output.textContent = "この状態claimは表示されません。";
  }
  document.querySelector("#decisionLog").textContent = JSON.stringify(decision, null, 2);
})();
