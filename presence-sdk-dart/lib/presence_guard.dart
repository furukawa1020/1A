class PresenceDecision {
  final String decision;
  final bool allowed;
  final List<String> reason;
  final String? suggestedText;
  final String? suggestedTextJa;
  final String? suggestedSeverity;

  PresenceDecision({
    required this.decision,
    required this.allowed,
    required this.reason,
    this.suggestedText,
    this.suggestedTextJa,
    this.suggestedSeverity,
  });
}

class PresenceGuard {
  final Map<String, dynamic> policy;

  PresenceGuard(this.policy);

  PresenceDecision requestClaim({
    required List<String> sourceSignals,
    required String proposedClaim,
    required String severity,
    required String claimType,
    required String audience,
    String retention = "session",
    String actionability = "self_reflection",
  }) {
    final scores = {"C0": 0, "C1": 1, "C2": 2, "C3": 3, "C4": 4, "C5": 5, "C6": 6};
    final maxSeverity = policy["max_allowed_severity"] ?? "C2";
    final maxScore = scores[maxSeverity] ?? 2;
    final claimScore = scores[severity];
    final reasons = <String>[];
    final allowedAudiences = List<String>.from(policy["allowed_audiences"] ?? ["self"]);
    final allowedRetention = List<String>.from(policy["allowed_retention"] ?? ["none", "session"]);
    final authorityAudiences = {"manager", "teacher", "employer", "evaluator", "admin", "organization"};

    if (claimScore == null) {
      return PresenceDecision(decision: "deny", allowed: false, reason: ["unknown claim severity"]);
    }
    if (!allowedAudiences.contains(audience)) {
      reasons.add("audience is not allowed by policy");
    }
    if (!allowedRetention.contains(retention)) {
      reasons.add("retention is not allowed by policy");
    }
    if (claimScore > maxScore) {
      reasons.add("claim severity exceeds policy cap $maxSeverity");
    }
    if (claimType == "productivity" && sourceSignals.any((s) => ["heart_rate", "sleep", "fatigue", "mood", "self_report"].contains(s))) {
      reasons.add("health signal must not become productivity claim");
      return _deny(reasons);
    }
    if (authorityAudiences.contains(audience)) {
      reasons.add("self-observation claim crosses authority boundary");
      return _deny(reasons);
    }
    if (claimType == "psychological") {
      reasons.add("psychological claim requires explicit capability");
    }
    if (claimScore > 2) {
      reasons.add("user must retain interpretation authority");
    }
    if (reasons.isEmpty) {
      return PresenceDecision(decision: "allow", allowed: true, reason: const []);
    }
    return PresenceDecision(
      decision: "rewrite",
      allowed: false,
      reason: reasons,
      suggestedText: policy["claim_minimization"]?["default_suggested_text"],
      suggestedTextJa: policy["claim_minimization"]?["default_suggested_text_ja"],
      suggestedSeverity: policy["claim_minimization"]?["default_rewrite_severity"] ?? "C2",
    );
  }

  PresenceDecision _deny(List<String> reasons) {
    return PresenceDecision(
      decision: "deny",
      allowed: false,
      reason: reasons,
      suggestedText: policy["claim_minimization"]?["default_suggested_text"],
      suggestedTextJa: policy["claim_minimization"]?["default_suggested_text_ja"],
      suggestedSeverity: policy["claim_minimization"]?["default_rewrite_severity"] ?? "C2",
    );
  }
}

