(async function initRiskDashboardDemo() {
  const guard = await PresenceGuard.load("../../presence-policy/presence.guard.policy.json");
  const requests = [
    {
      label: "Productivity loss by health condition",
      sourceSignals: ["health_status", "presenteeism_survey"],
      proposedText: "Productivity loss due to health condition",
      proposedSeverity: "C5",
      claimType: "productivity",
      audience: "manager",
      retention: "long_term",
      actionability: "manager_report"
    },
    {
      label: "Administrative high-risk priority",
      sourceSignals: ["stress_check", "overtime"],
      proposedText: "Manager action required",
      proposedSeverity: "C6",
      claimType: "administrative",
      audience: "manager",
      retention: "long_term",
      actionability: "manager_report"
    },
    {
      label: "Export claim-level records",
      sourceSignals: ["stress_survey", "self_report"],
      proposedText: "High stress extraction",
      proposedSeverity: "C4",
      claimType: "psychological",
      audience: "employer",
      retention: "long_term",
      actionability: "manager_report"
    }
  ];

  const blockedClaims = document.querySelector("#blockedClaims");
  const decisionLog = document.querySelector("#decisionLog");
  const decisions = requests.map((request) => ({ request: request.label, decision: guard.requestClaim(request) }));

  decisions.forEach(({ request, decision }) => {
    const card = document.createElement("div");
    card.className = "decision-card blocked";
    card.innerHTML = `<strong>${request}</strong><span>${decision.decision.toUpperCase()}</span><p>${decision.reason.join("; ")}</p>`;
    blockedClaims.appendChild(card);
  });
  decisionLog.textContent = JSON.stringify(decisions, null, 2);
})();
