(function initManipulationChecks(global) {
  const PSTT = global.PSTT || (global.PSTT = {});

  PSTT.manipulationChecks = [
    {
      name: "manip_cloud",
      text: "この条件では、データがクラウドに送信されると感じた。"
    },
    {
      name: "manip_visibility",
      text: "この条件では、結果が管理者・教員・雇用者に見られる可能性があると感じた。"
    },
    {
      name: "manip_assertive",
      text: "この条件では、システムが自分の状態を断定していたと感じた。"
    },
    {
      name: "manip_self_only",
      text: "この条件では、結果は本人だけに留まると感じた。"
    }
  ];

  PSTT.manipulationItemNames = PSTT.manipulationChecks.map((item) => item.name);
})(window);

