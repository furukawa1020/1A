(async function runDemo() {
  const guard = await PresenceGuard.load("../../presence-policy/presence.guard.policy.json");
  const decision = guard.requestClaim({
    sourceSignals: ["heart_rate", "keyboard_activity"],
    proposedText: "集中力が低下しています",
    proposedSeverity: "C3",
    claimType: "behavioral",
    audience: "self",
    retention: "session",
    actionability: "self_reflection"
  });
  document.querySelector("#output").textContent = JSON.stringify(decision, null, 2);
})();

