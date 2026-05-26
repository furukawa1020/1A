(function initStorage(global) {
  const PSTT = global.PSTT || (global.PSTT = {});
  const STORAGE_KEY = "pstt.study1a.current_session";
  const ID_KEY = "pstt.study1a.last_participant_id";

  function readSession() {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch (error) {
      console.error("Could not parse saved PSTT session", error);
      return null;
    }
  }

  function writeSession(session) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
    localStorage.setItem(ID_KEY, session.participant_id);
  }

  function clearSession() {
    localStorage.removeItem(STORAGE_KEY);
  }

  function newParticipantId() {
    const now = new Date();
    const stamp = now.toISOString().replace(/[-:.TZ]/g, "").slice(0, 14);
    const random = Math.random().toString(36).slice(2, 7).toUpperCase();
    return `PSTT-${stamp}-${random}`;
  }

  function getLastParticipantId() {
    return localStorage.getItem(ID_KEY) || newParticipantId();
  }

  PSTT.Storage = {
    readSession,
    writeSession,
    clearSession,
    newParticipantId,
    getLastParticipantId
  };
})(window);

