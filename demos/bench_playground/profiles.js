window.PRESENCE_BENCH_PROFILES = [
  {
    id: "presenteeism_survey_dashboard",
    title: "Presenteeism Survey Dashboard",
    processing: "cloud",
    retention: "long_term",
    visibility: ["user", "manager", "employer"],
    actions: ["manager_report", "weekly_summary", "csv_export"],
    claims: [
      {
        text: "Psychological condition score",
        severity: "C4",
        claimType: "psychological",
        sourceSignals: ["stress_survey", "engagement_survey"]
      },
      {
        text: "Presenteeism productivity loss score",
        severity: "C5",
        claimType: "productivity",
        sourceSignals: ["presenteeism_survey", "self_report"]
      }
    ]
  },
  {
    id: "employee_app_manager_dashboard",
    title: "Employee App + Manager Dashboard",
    processing: "cloud",
    retention: "long_term",
    visibility: ["user", "manager", "employer"],
    actions: ["manager_report", "organizational_dashboard"],
    claims: [
      {
        text: "Health behavior and condition status",
        severity: "C4",
        claimType: "psychological",
        sourceSignals: ["sleep", "stress_survey"]
      },
      {
        text: "Organization health-management priority",
        severity: "C6",
        claimType: "administrative",
        sourceSignals: ["health_check", "labor_information"]
      }
    ]
  },
  {
    id: "health_data_labor_risk_dashboard",
    title: "Health Data + Labor Risk Dashboard",
    processing: "cloud",
    retention: "long_term",
    visibility: ["user", "manager", "employer", "evaluator"],
    actions: ["manager_report", "administrative_action", "csv_export"],
    claims: [
      {
        text: "Labor risk priority",
        severity: "C6",
        claimType: "administrative",
        sourceSignals: ["health_check", "stress_check", "overtime"]
      }
    ]
  },
  {
    id: "stress_check_high_risk_extraction",
    title: "Stress Check High-Risk Extraction",
    processing: "cloud",
    retention: "long_term",
    visibility: ["user", "manager", "employer"],
    actions: ["attention_flag", "occupational_health_follow_up"],
    claims: [
      {
        text: "High stress extraction",
        severity: "C4",
        claimType: "psychological",
        sourceSignals: ["stress_check", "self_report"]
      },
      {
        text: "Interview follow-up required",
        severity: "C6",
        claimType: "administrative",
        sourceSignals: ["stress_check"]
      }
    ]
  },
  {
    id: "productivity_loss_visualization",
    title: "Productivity Loss / Economic Effect Visualization",
    processing: "cloud",
    retention: "long_term",
    visibility: ["user", "manager", "employer"],
    actions: ["manager_report", "team_benchmark", "csv_export"],
    claims: [
      {
        text: "Productivity loss due to health condition",
        severity: "C5",
        claimType: "productivity",
        sourceSignals: ["health_status", "presenteeism_survey"]
      },
      {
        text: "Economic loss estimate",
        severity: "C5",
        claimType: "productivity",
        sourceSignals: ["self_report", "absenteeism_survey"]
      }
    ]
  },
  {
    id: "noticer_local_low_risk",
    title: "Noticer Local Low Risk",
    processing: "local",
    retention: "session",
    visibility: ["user"],
    actions: ["user_notification"],
    claims: [
      {
        text: "The work flow may have changed slightly",
        severity: "C2",
        claimType: "pattern",
        sourceSignals: ["task_rhythm"]
      }
    ]
  }
];
