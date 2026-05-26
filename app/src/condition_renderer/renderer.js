(function initRenderer(global) {
  const PSTT = global.PSTT || (global.PSTT = {});

  function createElement(tagName, className, text) {
    const element = document.createElement(tagName);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  }

  function renderScenario(container) {
    container.innerHTML = "";
    PSTT.scenario.paragraphs.forEach((paragraph) => {
      container.appendChild(createElement("p", "", paragraph));
    });
  }

  function renderOutput(container, outputText) {
    container.innerHTML = "";
    const list = createElement("ul", "output-lines");
    outputText.split("\n").forEach((line) => {
      list.appendChild(createElement("li", "", line));
    });
    container.appendChild(list);
  }

  function renderConditionText(fragment, condition) {
    fragment.querySelector("#processingText").textContent = condition.processing_text;
    fragment.querySelector("#visibilityText").textContent = condition.visibility_text;
    renderOutput(fragment.querySelector("#outputText"), condition.output_text);
    renderScenario(fragment.querySelector("#scenarioText"));
  }

  function conditionToClaimRequest(condition) {
    const assertive = condition.output === "assertive";
    const managerVisible = condition.visibility === "manager_visible";
    return {
      sourceSignals: condition.processing === "cloud" ? ["keyboard_activity", "self_report"] : ["keyboard_rhythm"],
      proposedText: condition.output_text.split("\n")[0],
      proposedSeverity: assertive ? "C4" : "C2",
      claimType: assertive ? "psychological" : "pattern",
      audience: managerVisible ? "manager" : "self",
      retention: managerVisible ? "long_term" : "session",
      actionability: managerVisible ? "manager_report" : "self_reflection",
      evidenceStrength: "limited"
    };
  }

  function makeRating(name, savedValue) {
    const wrapper = createElement("div", "rating");
    for (let value = 1; value <= 7; value += 1) {
      const label = document.createElement("label");
      const input = document.createElement("input");
      input.type = "radio";
      input.name = name;
      input.value = String(value);
      input.required = true;
      if (String(savedValue || "") === String(value)) {
        input.checked = true;
      }
      const visible = createElement("span", "", String(value));
      label.append(input, visible);
      wrapper.appendChild(label);
    }
    return wrapper;
  }

  function makeQuestionGroup(group, savedValues) {
    const section = createElement("section", "question-group");
    section.appendChild(createElement("h3", "", group.title));
    const labels = createElement("div", "scale-labels");
    labels.append(createElement("span", "", "1: まったくそう思わない"));
    labels.append(createElement("span", "", "7: 非常にそう思う"));
    section.appendChild(labels);

    const table = createElement("div", "question-table");
    group.items.forEach((item) => {
      const row = createElement("div", "question-row");
      row.appendChild(createElement("p", "question-text", item.text));
      row.appendChild(makeRating(item.name, savedValues[item.name]));
      table.appendChild(row);
    });
    section.appendChild(table);
    return section;
  }

  function renderQuestionnaire(container, savedValues) {
    container.innerHTML = "";
    PSTT.questionGroups.forEach((group) => {
      container.appendChild(makeQuestionGroup(group, savedValues));
    });
    container.appendChild(
      makeQuestionGroup(
        {
          title: "操作チェック",
          items: PSTT.manipulationChecks
        },
        savedValues
      )
    );
  }

  function getCheckedValue(form, name) {
    const checked = form.querySelector(`input[name="${name}"]:checked`);
    return checked ? Number(checked.value) : null;
  }

  function collectFormValues(form, allowMissing) {
    const names = PSTT.scaleItemNames.concat(PSTT.manipulationItemNames);
    const values = {};
    const missing = [];
    names.forEach((name) => {
      const value = getCheckedValue(form, name);
      if (value === null) {
        missing.push(name);
      } else {
        values[name] = value;
      }
    });

    const freeText = form.querySelector("#freeText").value.trim();
    if (!freeText && !allowMissing) {
      missing.push("free_text");
    }
    values.free_text = freeText;

    return { values, missing };
  }

  function fillSavedValues(form, savedValues) {
    if (!savedValues) return;
    Object.entries(savedValues).forEach(([name, value]) => {
      const input = form.querySelector(`input[name="${name}"][value="${value}"]`);
      if (input) input.checked = true;
    });
    const textarea = form.querySelector("#freeText");
    if (textarea && savedValues.free_text) {
      textarea.value = savedValues.free_text;
    }
  }

  PSTT.Renderer = {
    renderConditionText,
    conditionToClaimRequest,
    renderQuestionnaire,
    collectFormValues,
    fillSavedValues
  };
})(window);
