(async function initAuditView(global) {
  const PSTT = global.PSTT || (global.PSTT = {});
  const version = document.querySelector("#auditVersion");
  const summary = document.querySelector("#auditSummary");
  const tableHost = document.querySelector("#auditTable");

  function makeSummary(label, value) {
    const item = document.createElement("div");
    item.className = "summary-item";
    const strong = document.createElement("strong");
    strong.textContent = value;
    const span = document.createElement("span");
    span.textContent = label;
    item.append(strong, span);
    return item;
  }

  function renderTable(data) {
    const table = document.createElement("table");
    table.className = "review-table audit-table";
    table.innerHTML = "<thead><tr><th>条件</th><th>ESS</th><th>信頼境界</th><th>可視主体</th><th>二次利用</th><th>所見</th></tr></thead>";
    const body = document.createElement("tbody");
    data.conditions.forEach((condition) => {
      const scored = PSTT.Audit.scoreCondition(condition, data.audit_schema);
      const findings = PSTT.Audit.policyFindings(condition, data.audit_schema);
      const row = document.createElement("tr");
      row.innerHTML = `
        <td><strong>${condition.condition_id}</strong><br>${condition.processing} / ${condition.visibility} / ${condition.output}</td>
        <td>${scored.ess.toFixed(2)}</td>
        <td>${(condition.audit.trust_boundaries || []).join("<br>") || "none"}</td>
        <td>${(condition.audit.observers || []).join("<br>") || "none"}</td>
        <td>${(condition.audit.secondary_use_channels || []).join("<br>") || "none"}</td>
        <td>${findings.map((finding) => `${finding.severity}: ${finding.message_ja}`).join("<br>")}</td>
      `;
      body.appendChild(row);
    });
    table.appendChild(body);
    tableHost.innerHTML = "";
    tableHost.appendChild(table);
  }

  try {
    const response = await fetch("conditions/conditions_2x2x2.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`Could not load conditions: ${response.status}`);
    const data = await response.json();
    version.textContent = data.study_version;
    const scored = data.conditions.map((condition) => PSTT.Audit.scoreCondition(condition, data.audit_schema).ess);
    summary.appendChild(makeSummary("条件数", String(data.conditions.length)));
    summary.appendChild(makeSummary("最大ESS", Math.max(...scored).toFixed(2)));
    summary.appendChild(makeSummary("最小ESS", Math.min(...scored).toFixed(2)));
    summary.appendChild(makeSummary("監査スキーマ", data.condition_schema));
    renderTable(data);
  } catch (error) {
    version.textContent = "load failed";
    tableHost.textContent = error.message;
  }
})(window);

