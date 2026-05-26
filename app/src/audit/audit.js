(function initAudit(global) {
  const PSTT = global.PSTT || (global.PSTT = {});

  const DEFAULT_WEIGHTS = {
    data_transmission: 1.0,
    processing_location: 1.0,
    storage: 1.0,
    third_party_visibility: 2.0,
    identifiability: 1.0,
    secondary_use: 2.0,
    output_claim: 1.5
  };

  const SCORE_KEYS = Object.keys(DEFAULT_WEIGHTS);

  function weightsFromSchema(schema) {
    return (schema && schema.weights) || DEFAULT_WEIGHTS;
  }

  function scoreCondition(condition, auditSchema) {
    const weights = weightsFromSchema(auditSchema);
    const audit = condition.audit || {};
    const raw = {};
    const weighted = {};
    SCORE_KEYS.forEach((key) => {
      raw[key] = Number(audit[key] || 0);
      weighted[`${key}_weighted`] = raw[key] * Number(weights[key] || 1);
    });
    const ess = Object.values(weighted).reduce((sum, value) => sum + value, 0);
    return { raw, weighted, ess };
  }

  function policyFindings(condition, auditSchema) {
    const audit = condition.audit || {};
    const findings = [];
    const scored = scoreCondition(condition, auditSchema);

    if (audit.third_party_visibility >= 2 && audit.output_claim >= 2) {
      findings.push({
        severity: "high",
        code: "manager_visible_assertive_label",
        message_en: "Manager-visible output and assertive labeling co-occur.",
        message_ja: "管理者可視性と断定ラベルが同時に存在する。"
      });
    }

    if (audit.secondary_use >= 2) {
      findings.push({
        severity: "high",
        code: "secondary_use_enabled",
        message_en: "The scenario includes a report or channel that enables secondary use.",
        message_ja: "レポート等により二次利用可能性がある。"
      });
    }

    if (audit.processing_location >= 2 && audit.data_transmission >= 2) {
      findings.push({
        severity: "medium",
        code: "cloud_processing_boundary",
        message_en: "The data crosses the device-to-cloud trust boundary.",
        message_ja: "データが端末からクラウドへの信頼境界を越える。"
      });
    }

    if (audit.output_claim >= 2) {
      findings.push({
        severity: "medium",
        code: "assertive_internal_state_claim",
        message_en: "The output makes an assertive claim about the user's internal state.",
        message_ja: "出力がユーザーの内部状態について断定的に主張する。"
      });
    }

    if (scored.ess === 0) {
      findings.push({
        severity: "info",
        code: "low_exposure_candidate",
        message_en: "No audited exposure item is above zero in this scenario.",
        message_ja: "このシナリオでは監査項目上の曝露が0である。"
      });
    }

    return findings;
  }

  function flattenAudit(condition, auditSchema) {
    const audit = condition.audit || {};
    const scored = scoreCondition(condition, auditSchema);
    const findings = policyFindings(condition, auditSchema);
    return {
      audit_data_asset: audit.data_asset || "",
      audit_data_asset_ja: audit.data_asset_ja || "",
      audit_trust_boundaries: (audit.trust_boundaries || []).join(" "),
      audit_observers: (audit.observers || []).join(" "),
      audit_secondary_use_channels: (audit.secondary_use_channels || []).join(" "),
      audit_policy_profile: audit.policy_profile || "",
      ess: scored.ess.toFixed(2),
      audit_data_transmission: scored.raw.data_transmission,
      audit_processing_location: scored.raw.processing_location,
      audit_storage: scored.raw.storage,
      audit_third_party_visibility: scored.raw.third_party_visibility,
      audit_identifiability: scored.raw.identifiability,
      audit_secondary_use: scored.raw.secondary_use,
      audit_output_claim: scored.raw.output_claim,
      audit_findings: findings.map((finding) => finding.code).join(" ")
    };
  }

  PSTT.Audit = {
    SCORE_KEYS,
    scoreCondition,
    policyFindings,
    flattenAudit
  };
})(window);

