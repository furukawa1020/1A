(function initApp(global) {
  const PSTT = global.PSTT || (global.PSTT = {});
  const app = document.querySelector("#app");
  const studyVersionLabel = document.querySelector("#studyVersion");
  const progressLabel = document.querySelector("#progressLabel");
  let conditionFile = null;

  function byId(id) {
    return document.getElementById(id);
  }

  function setProgress(text) {
    progressLabel.textContent = text;
  }

  function cloneTemplate(id) {
    const template = byId(id);
    return template.content.cloneNode(true);
  }

  function clearApp() {
    app.innerHTML = "";
    app.focus();
  }

  function hashText(text) {
    let hash = 2166136261;
    for (let index = 0; index < text.length; index += 1) {
      hash ^= text.charCodeAt(index);
      hash = Math.imul(hash, 16777619);
    }
    return hash >>> 0;
  }

  function balancedLatinSequence(conditionIds, participantId) {
    const n = conditionIds.length;
    const rowIndex = hashText(participantId) % n;
    const base = [];
    for (let index = 0; index < n; index += 1) {
      if (index % 2 === 0) {
        base.push(index / 2);
      } else {
        base.push(n - 1 - Math.floor(index / 2));
      }
    }
    const rotated = base.map((value) => (value + rowIndex) % n);
    const orderedIndexes = rowIndex % 2 === 0 ? rotated : rotated.slice().reverse();
    return orderedIndexes.map((index) => conditionIds[index]);
  }

  function conditionsById() {
    const map = new Map();
    conditionFile.conditions.forEach((condition) => {
      map.set(condition.condition_id, condition);
    });
    return map;
  }

  function makeSession(participantId) {
    const conditionIds = conditionFile.conditions
      .map((condition) => condition.condition_id)
      .sort((a, b) => Number(a.slice(1)) - Number(b.slice(1)));
    return {
      participant_id: participantId,
      study_version: conditionFile.study_version,
      audit_schema: conditionFile.audit_schema,
      order_strategy: "balanced_latin_square_by_participant_id",
      condition_sequence: balancedLatinSequence(conditionIds, participantId),
      responses: [],
      drafts: {},
      started_at: new Date().toISOString(),
      completed_at: null
    };
  }

  function currentCondition(session) {
    const conditionId = session.condition_sequence[session.responses.length];
    return conditionsById().get(conditionId);
  }

  function renderStart() {
    clearApp();
    setProgress("開始前");
    const fragment = cloneTemplate("startTemplate");
    const participantInput = fragment.querySelector("#participantIdInput");
    const orderPreviewInput = fragment.querySelector("#orderPreviewInput");
    const consentInput = fragment.querySelector("#consentInput");
    const startButton = fragment.querySelector("#startButton");
    const resumeButton = fragment.querySelector("#resumeButton");
    const existing = PSTT.Storage.readSession();

    participantInput.value = existing ? existing.participant_id : PSTT.Storage.newParticipantId();

    function updatePreview() {
      const preview = makeSession(participantInput.value.trim() || PSTT.Storage.newParticipantId());
      orderPreviewInput.value = preview.condition_sequence.join(" ");
    }

    participantInput.addEventListener("input", updatePreview);
    updatePreview();

    startButton.addEventListener("click", () => {
      if (!consentInput.checked) {
        consentInput.focus();
        return;
      }
      const participantId = participantInput.value.trim() || PSTT.Storage.newParticipantId();
      const session = makeSession(participantId);
      PSTT.Storage.writeSession(session);
      renderCurrentCondition();
    });

    resumeButton.addEventListener("click", () => {
      const session = PSTT.Storage.readSession();
      if (session && session.responses.length >= session.condition_sequence.length) {
        renderComplete(session);
      } else if (session) {
        renderCurrentCondition();
      } else {
        renderReview(null);
      }
    });

    app.appendChild(fragment);
  }

  function buildResponse(session, condition, values) {
    return {
      condition_id: condition.condition_id,
      processing: condition.processing,
      visibility: condition.visibility,
      output: condition.output,
      condition_order: session.responses.length + 1,
      ...PSTT.Audit.flattenAudit(condition, conditionFile.audit_schema),
      ...values,
      answered_at: new Date().toISOString()
    };
  }

  function saveDraft(form, session, condition) {
    const collected = PSTT.Renderer.collectFormValues(form, true);
    session.drafts[condition.condition_id] = collected.values;
    PSTT.Storage.writeSession(session);
  }

  function renderCurrentCondition() {
    const session = PSTT.Storage.readSession();
    if (!session) {
      renderStart();
      return;
    }
    if (session.responses.length >= session.condition_sequence.length) {
      renderComplete(session);
      return;
    }

    const condition = currentCondition(session);
    clearApp();
    setProgress(`条件 ${session.responses.length + 1} / ${session.condition_sequence.length}: ${condition.condition_id}`);

    const fragment = cloneTemplate("conditionTemplate");
    PSTT.Renderer.renderConditionText(fragment, condition);
    const guardDecisionNode = fragment.querySelector("#guardDecision");
    if (guardDecisionNode && global.PresenceGuard) {
      global.PresenceGuard.load("policies/presence.guard.policy.json").then((guard) => {
        const request = PSTT.Renderer.conditionToClaimRequest(condition);
        guardDecisionNode.textContent = JSON.stringify(guard.requestClaim(request), null, 2);
      }).catch((error) => {
        guardDecisionNode.textContent = `PRESENCE Guard policy load failed: ${error.message}`;
      });
    }
    const questionGroups = fragment.querySelector("#questionGroups");
    const savedValues = session.drafts[condition.condition_id] || {};
    PSTT.Renderer.renderQuestionnaire(questionGroups, savedValues);
    const form = fragment.querySelector("#responseForm");
    PSTT.Renderer.fillSavedValues(form, savedValues);
    const error = fragment.querySelector("#formError");

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const collected = PSTT.Renderer.collectFormValues(form, false);
      if (collected.missing.length > 0) {
        error.textContent = "未回答の項目があります。すべての尺度項目と自由記述に回答してください。";
        return;
      }
      const updated = PSTT.Storage.readSession();
      const response = buildResponse(updated, condition, collected.values);
      updated.responses.push(response);
      delete updated.drafts[condition.condition_id];
      if (updated.responses.length >= updated.condition_sequence.length) {
        updated.completed_at = new Date().toISOString();
      }
      PSTT.Storage.writeSession(updated);
      renderCurrentCondition();
    });

    fragment.querySelector("#saveDraftButton").addEventListener("click", () => {
      const updated = PSTT.Storage.readSession();
      saveDraft(form, updated, condition);
      error.textContent = "一時保存しました。";
    });

    app.appendChild(fragment);
  }

  function mean(values) {
    const numeric = values.filter((value) => Number.isFinite(value));
    if (!numeric.length) return "";
    return (numeric.reduce((sum, value) => sum + value, 0) / numeric.length).toFixed(2);
  }

  function scaleMean(response, prefix) {
    const values = Object.entries(response)
      .filter(([key]) => key.startsWith(`${prefix}_`))
      .map(([, value]) => Number(value));
    return mean(values);
  }

  function renderComplete(session) {
    clearApp();
    setProgress("完了");
    const fragment = cloneTemplate("completeTemplate");
    const summary = fragment.querySelector("#completionSummary");
    [
      ["参加者ID", session.participant_id],
      ["回答条件数", `${session.responses.length} / ${session.condition_sequence.length}`],
      ["条件順序", session.condition_sequence.join(" ")],
      ["保存場所", "このブラウザのlocalStorage"]
    ].forEach(([label, value]) => {
      const item = document.createElement("div");
      item.className = "summary-item";
      item.innerHTML = `<strong>${value}</strong><span>${label}</span>`;
      summary.appendChild(item);
    });

    fragment.querySelector("#downloadCsvButton").addEventListener("click", () => {
      PSTT.Exporter.downloadCsv(PSTT.Storage.readSession());
    });
    fragment.querySelector("#downloadJsonButton").addEventListener("click", () => {
      PSTT.Exporter.downloadJson(PSTT.Storage.readSession());
    });
    fragment.querySelector("#reviewButton").addEventListener("click", () => {
      renderReview(PSTT.Storage.readSession());
    });
    fragment.querySelector("#newSessionButton").addEventListener("click", () => {
      PSTT.Storage.clearSession();
      renderStart();
    });

    app.appendChild(fragment);
  }

  function renderReview(session) {
    clearApp();
    setProgress("回答確認");
    const section = document.createElement("section");
    section.className = "instrument";
    const band = document.createElement("div");
    band.className = "section-band";
    band.innerHTML = "<h2>保存済み回答</h2>";
    if (!session || !session.responses.length) {
      band.appendChild(document.createTextNode("保存済み回答はありません。"));
      section.appendChild(band);
    } else {
      const table = document.createElement("table");
      table.className = "review-table";
      table.innerHTML = "<thead><tr><th>順序</th><th>条件</th><th>MFS</th><th>LIS</th><th>SOUS</th><th>WU</th><th>WD</th></tr></thead>";
      const body = document.createElement("tbody");
      session.responses.forEach((response) => {
        const row = document.createElement("tr");
        row.innerHTML = `<td>${response.condition_order}</td><td>${response.condition_id}</td><td>${scaleMean(response, "mfs")}</td><td>${scaleMean(response, "lis")}</td><td>${scaleMean(response, "sous")}</td><td>${scaleMean(response, "wu")}</td><td>${scaleMean(response, "wd")}</td>`;
        body.appendChild(row);
      });
      table.appendChild(body);
      band.appendChild(table);
      section.appendChild(band);
    }

    const actions = document.createElement("div");
    actions.className = "actions";
    const backButton = document.createElement("button");
    backButton.type = "button";
    backButton.className = "primary";
    backButton.textContent = "戻る";
    backButton.addEventListener("click", () => {
      const saved = PSTT.Storage.readSession();
      if (saved && saved.responses.length >= saved.condition_sequence.length) {
        renderComplete(saved);
      } else if (saved) {
        renderCurrentCondition();
      } else {
        renderStart();
      }
    });
    actions.appendChild(backButton);
    section.appendChild(actions);
    app.appendChild(section);
  }

  async function loadConditions() {
    const response = await fetch("conditions/conditions_2x2x2.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Could not load conditions: ${response.status}`);
    }
    conditionFile = await response.json();
    studyVersionLabel.textContent = conditionFile.study_version;
  }

  async function main() {
    try {
      await loadConditions();
      renderStart();
    } catch (error) {
      console.error(error);
      studyVersionLabel.textContent = "load failed";
      setProgress("条件ファイル未読込");
      clearApp();
      const section = document.createElement("section");
      section.className = "section-band";
      section.innerHTML = "<h2>条件ファイルを読み込めませんでした</h2><p>このアプリは条件定義JSONを読み込むため、ローカルHTTPサーバーから開いてください。</p><pre>python -m http.server 8000 --bind 127.0.0.1 --directory app</pre>";
      app.appendChild(section);
    }
  }

  main();
})(window);
