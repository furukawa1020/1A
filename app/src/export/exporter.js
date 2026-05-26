(function initExporter(global) {
  const PSTT = global.PSTT || (global.PSTT = {});

  const exportColumns = [
    "participant_id",
    "study_version",
    "condition_id",
    "processing",
    "visibility",
    "output",
    "condition_order",
    "mfs_1",
    "mfs_2",
    "mfs_3",
    "mfs_4",
    "mfs_5",
    "lis_1",
    "lis_2",
    "lis_3",
    "lis_4",
    "lis_5",
    "sous_1",
    "sous_2",
    "sous_3",
    "sous_4",
    "sous_5",
    "wu_1",
    "wu_2",
    "wu_3",
    "wd_1",
    "wd_2",
    "wd_3",
    "manip_cloud",
    "manip_visibility",
    "manip_assertive",
    "free_text",
    "manip_self_only",
    "condition_sequence",
    "order_strategy",
    "answered_at"
  ];

  function escapeCsv(value) {
    if (value === null || value === undefined) return "";
    const text = String(value);
    if (/[",\n\r]/.test(text)) {
      return `"${text.replace(/"/g, '""')}"`;
    }
    return text;
  }

  function toRows(session) {
    return session.responses.map((response) => {
      const row = {
        participant_id: session.participant_id,
        study_version: session.study_version,
        condition_sequence: session.condition_sequence.join(" "),
        order_strategy: session.order_strategy,
        ...response
      };
      return row;
    });
  }

  function toCsv(session) {
    const rows = toRows(session);
    const lines = [exportColumns.join(",")];
    rows.forEach((row) => {
      lines.push(exportColumns.map((column) => escapeCsv(row[column])).join(","));
    });
    return lines.join("\n");
  }

  function download(filename, mimeType, content) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  }

  function downloadCsv(session) {
    const filename = `${session.participant_id}_pstt_1a.csv`;
    download(filename, "text/csv;charset=utf-8", toCsv(session));
  }

  function downloadJson(session) {
    const filename = `${session.participant_id}_pstt_1a.json`;
    download(filename, "application/json;charset=utf-8", JSON.stringify(session, null, 2));
  }

  PSTT.Exporter = {
    exportColumns,
    toRows,
    toCsv,
    downloadCsv,
    downloadJson
  };
})(window);

