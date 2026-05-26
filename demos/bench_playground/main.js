(async function initBenchPlayground() {
  const guard = await PresenceGuard.load("../../presence-policy/presence.guard.policy.json");
  const profiles = window.PRESENCE_BENCH_PROFILES;
  const state = {
    profile: structuredClone(profiles[0]),
    original: structuredClone(profiles[0])
  };

  const profileSelect = document.querySelector("#profileSelect");
  const profileSummary = document.querySelector("#profileSummary");
  const decisionCards = document.querySelector("#decisionCards");
  const claimFlow = document.querySelector("#claimFlow");
  const report = document.querySelector("#report");

  profiles.forEach((profile) => {
    const option = document.createElement("option");
    option.value = profile.id;
    option.textContent = profile.title;
    profileSelect.appendChild(option);
  });

  function cloneProfile(id) {
    return structuredClone(profiles.find((profile) => profile.id === id));
  }

  function requestForClaim(profile, claim) {
    const authorityVisible = profile.visibility.some((item) => ["manager", "teacher", "employer", "evaluator"].includes(item));
    return {
      sourceSignals: claim.sourceSignals,
      proposedText: claim.text,
      proposedSeverity: claim.severity,
      claimType: claim.claimType,
      audience: authorityVisible ? "manager" : "self",
      retention: profile.retention,
      actionability: authorityVisible ? "manager_report" : "self_reflection"
    };
  }

  function scoreProfile(profile, decisions) {
    let score = 0;
    if (profile.processing === "cloud") score += 3;
    if (profile.retention === "long_term") score += 3;
    if (profile.visibility.some((item) => ["manager", "teacher", "employer", "evaluator"].includes(item))) score += 4;
    score += profile.claims.reduce((max, claim) => Math.max(max, Number(claim.severity.slice(1))), 0);
    score += decisions.filter((item) => item.decision.decision === "deny").length * 3;
    return score;
  }

  function riskLevel(score) {
    if (score >= 18) return "CRITICAL";
    if (score >= 12) return "HIGH";
    if (score >= 6) return "MEDIUM";
    return "LOW";
  }

  function render() {
    const decisions = state.profile.claims.map((claim) => ({
      claim,
      request: requestForClaim(state.profile, claim),
      decision: guard.requestClaim(requestForClaim(state.profile, claim))
    }));
    const score = scoreProfile(state.profile, decisions);

    profileSummary.innerHTML = "";
    [
      ["processing", state.profile.processing],
      ["retention", state.profile.retention],
      ["visibility", state.profile.visibility.join(", ")],
      ["actions", state.profile.actions.join(", ")],
      ["risk", riskLevel(score)],
      ["score", String(score)]
    ].forEach(([key, value]) => {
      const dt = document.createElement("dt");
      const dd = document.createElement("dd");
      dt.textContent = key;
      dd.textContent = value;
      profileSummary.append(dt, dd);
    });

    decisionCards.innerHTML = "";
    decisions.forEach(({ claim, decision }) => {
      const card = document.createElement("div");
      card.className = `decision-card ${decision.decision}`;
      card.innerHTML = `<strong>${claim.text}</strong><span>${decision.decision.toUpperCase()}</span><p>${decision.reason.join("; ") || "allowed by policy"}</p>`;
      decisionCards.appendChild(card);
    });

    claimFlow.innerHTML = "";
    state.profile.claims.forEach((claim) => {
      const item = document.createElement("div");
      item.className = "flow-item";
      item.textContent = `${claim.sourceSignals.join(", ")} -> ${claim.claimType} -> ${claim.severity} -> ${state.profile.visibility.join(", ")} -> ${state.profile.actions.join(", ")}`;
      claimFlow.appendChild(item);
    });

    report.textContent = JSON.stringify(
      {
        profile: state.profile.id,
        risk: riskLevel(score),
        decisions: decisions.map(({ claim, decision }) => ({
          claim: claim.text,
          severity: claim.severity,
          type: claim.claimType,
          decision: decision.decision,
          reason: decision.reason,
          suggested: decision.suggestedTextJa || decision.suggestedText
        }))
      },
      null,
      2
    );
  }

  profileSelect.addEventListener("change", () => {
    state.profile = cloneProfile(profileSelect.value);
    state.original = cloneProfile(profileSelect.value);
    render();
  });

  document.querySelector("#mitigateButton").addEventListener("click", () => {
    state.profile.processing = "local";
    state.profile.retention = "session";
    state.profile.visibility = ["user"];
    state.profile.actions = ["user_notification"];
    state.profile.claims = state.profile.claims.map((claim) => ({
      ...claim,
      text: "The work flow may have changed slightly",
      severity: "C2",
      claimType: "pattern",
      sourceSignals: claim.sourceSignals.filter((signal) => !["health_status", "heart_rate", "stress_check"].includes(signal)).slice(0, 1)
    }));
    render();
  });

  document.querySelector("#resetButton").addEventListener("click", () => {
    state.profile = structuredClone(state.original);
    render();
  });

  render();
})();
