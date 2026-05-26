(function initQuestionnaireItems(global) {
  const PSTT = global.PSTT || (global.PSTT = {});

  PSTT.questionGroups = [
    {
      key: "mfs",
      title: "MFS: Monitoring Feeling Score",
      items: [
        { name: "mfs_1", text: "このシステムには見張られている感じがした。" },
        { name: "mfs_2", text: "このシステムには管理されている感じがした。" },
        { name: "mfs_3", text: "このシステムは本人支援よりも評価・管理に近いと感じた。" },
        { name: "mfs_4", text: "このシステムの結果が自分に不利に使われそうだと感じた。" },
        { name: "mfs_5", text: "このシステムを使うと、不調を隠しにくくなると感じた。" }
      ]
    },
    {
      key: "lis",
      title: "LIS: Label Imposition Score",
      items: [
        { name: "lis_1", text: "システムに自分の状態を決めつけられた感じがした。" },
        { name: "lis_2", text: "自分の感じ方よりも、システムの判断が優先されるように感じた。" },
        { name: "lis_3", text: "納得していない意味づけを与えられたように感じた。" },
        { name: "lis_4", text: "表示を見ることで、自分の状態の解釈が狭められた。" },
        { name: "lis_5", text: "自分の状態を自分で考える余地が減った。" }
      ]
    },
    {
      key: "sous",
      title: "SOUS: Self-Observation Utility Score",
      items: [
        { name: "sous_1", text: "自分の状態を一度見直すきっかけになった。" },
        { name: "sous_2", text: "無理して続けているかもしれないと考える余地があった。" },
        { name: "sous_3", text: "休む・続ける・相談する判断を急がされずに考えられた。" },
        { name: "sous_4", text: "自分の文脈で解釈する余地があった。" },
        { name: "sous_5", text: "不安を過度に増やさずに振り返れそうだと感じた。" }
      ]
    },
    {
      key: "wu",
      title: "WU: Willingness to Use",
      items: [
        { name: "wu_1", text: "このシステムを自分の日常で使ってもよいと思った。" },
        { name: "wu_2", text: "このシステムなら、不調を抱えたまま作業しているときにも使えそうだと思った。" },
        { name: "wu_3", text: "このシステムは自分のための支援として受け入れられると感じた。" }
      ]
    },
    {
      key: "wd",
      title: "WD: Willingness to Disclose",
      items: [
        { name: "wd_1", text: "このシステムになら、自分の状態に関する情報を扱わせてもよいと思った。" },
        { name: "wd_2", text: "このシステムの仕組みなら、安心して自己観察に使えそうだと思った。" },
        { name: "wd_3", text: "このシステムが扱う情報の範囲は許容できると感じた。" }
      ]
    }
  ];

  PSTT.scaleItemNames = PSTT.questionGroups.flatMap((group) => group.items.map((item) => item.name));
})(window);

