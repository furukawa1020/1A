export const PresenceDecision = {
  allow: 0,
  rewrite: 1,
  deny: 2
};

export const PresenceReason = {
  0: "allowed",
  1: "unknown severity",
  2: "health signal must not become productivity claim",
  3: "self-observation claim crosses authority boundary",
  4: "temporary state must not become persistent administrative record",
  5: "user must retain interpretation authority",
  6: "deny by default"
};

export async function loadPresenceCoreWasm(urlOrBytes) {
  let bytes;
  if (urlOrBytes instanceof ArrayBuffer || ArrayBuffer.isView(urlOrBytes)) {
    bytes = urlOrBytes;
  } else {
    const response = await fetch(urlOrBytes);
    if (!response.ok) {
      throw new Error(`Could not load PRESENCE core WASM: ${response.status}`);
    }
    bytes = await response.arrayBuffer();
  }
  const result = await WebAssembly.instantiate(bytes, {});
  return result.instance.exports;
}

export function decodeDecision(code) {
  const decisionCode = code & 0xff;
  const allowed = ((code >> 8) & 0xff) === 1;
  const reasonCode = (code >> 16) & 0xff;
  const suggestedSeverityCode = (code >> 24) & 0xff;
  const decision =
    decisionCode === PresenceDecision.allow
      ? "allow"
      : decisionCode === PresenceDecision.rewrite
        ? "rewrite"
        : "deny";
  return {
    decision,
    allowed,
    reasonCode,
    reason: PresenceReason[reasonCode] || "unknown reason",
    suggestedSeverity: `C${suggestedSeverityCode}`
  };
}
