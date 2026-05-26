(function initManipulationChecks(global) {
  const PSTT = global.PSTT || (global.PSTT = {});

  PSTT.manipulationChecks = [
    {
      name: "manip_cloud",
      text: "この条件では、データがクラウドに送信されると感じた。",
      text_en: "In this condition, I felt that data was sent to the cloud."
    },
    {
      name: "manip_visibility",
      text: "この条件では、結果が管理者・教員・雇用者に見られる可能性があると感じた。",
      text_en: "In this condition, I felt that managers, teachers, or employers could see the result."
    },
    {
      name: "manip_assertive",
      text: "この条件では、システムが自分の状態を断定していたと感じた。",
      text_en: "In this condition, I felt that the system made an assertive claim about my state."
    },
    {
      name: "manip_self_only",
      text: "この条件では、結果は本人だけに留まると感じた。",
      text_en: "In this condition, I felt that the result stayed only with me."
    }
  ];

  PSTT.manipulationItemNames = PSTT.manipulationChecks.map((item) => item.name);
})(window);
