(async function initNoticerDemo() {
  const guard = await PresenceGuard.load("../../presence-policy/presence.guard.policy.json");
  const request = {
    sourceSignals: ["task_rhythm"],
    proposedText: "The work flow may have changed slightly",
    proposedSeverity: "C2",
    claimType: "pattern",
    audience: "self",
    retention: "session",
    actionability: "self_reflection"
  };

  const decision = guard.requestClaim(request);
  document.querySelector("#renderedOutput").textContent = decision.text || decision.suggestedTextJa || decision.suggestedText;
  document.querySelector("#decisionLog").textContent = JSON.stringify(decision, null, 2);
})();
