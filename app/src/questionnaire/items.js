(function initQuestionnaireItems(global) {
  // presence-scan: ignore-file
  const PSTT = global.PSTT || (global.PSTT = {});

  PSTT.questionGroups = [
    {
      key: "mfs",
      title: "MFS: Monitoring Feeling Score",
      title_en: "MFS: Monitoring Feeling Score",
      items: [
        { name: "mfs_1", text: "このシステムには見張られている感じがした。", text_en: "I felt watched by this system." },
        { name: "mfs_2", text: "このシステムには管理されている感じがした。", text_en: "I felt managed by this system." },
        { name: "mfs_3", text: "このシステムは本人支援よりも評価・管理に近いと感じた。", text_en: "I felt this system was closer to evaluation or management than self-support." },
        { name: "mfs_4", text: "このシステムの結果が自分に不利に使われそうだと感じた。", text_en: "I felt the system's result could be used against me." },
        { name: "mfs_5", text: "このシステムを使うと、不調を隠しにくくなると感じた。", text_en: "I felt that using this system would make it harder to hide being unwell." }
      ]
    },
    {
      key: "lis",
      title: "LIS: Label Imposition Score",
      title_en: "LIS: Label Imposition Score",
      items: [
        { name: "lis_1", text: "システムに自分の状態を決めつけられた感じがした。", text_en: "I felt that the system determined my state." },
        { name: "lis_2", text: "自分の感じ方よりも、システムの判断が優先されるように感じた。", text_en: "I felt that the system's judgment was prioritized over my own feeling." },
        { name: "lis_3", text: "納得していない意味づけを与えられたように感じた。", text_en: "I felt assigned an interpretation that I did not accept." },
        { name: "lis_4", text: "表示を見ることで、自分の状態の解釈が狭められた。", text_en: "Seeing the display narrowed how I could interpret my state." },
        { name: "lis_5", text: "自分の状態を自分で考える余地が減った。", text_en: "I had less room to think about my state myself." }
      ]
    },
    {
      key: "sous",
      title: "SOUS: Self-Observation Utility Score",
      title_en: "SOUS: Self-Observation Utility Score",
      items: [
        { name: "sous_1", text: "自分の状態を一度見直すきっかけになった。", text_en: "It gave me a chance to review my state." },
        { name: "sous_2", text: "無理して続けているかもしれないと考える余地があった。", text_en: "It left room to consider whether I might be pushing myself." },
        { name: "sous_3", text: "休む・続ける・相談する判断を急がされずに考えられた。", text_en: "I could think about whether to rest, continue, or consult someone without being rushed." },
        { name: "sous_4", text: "自分の文脈で解釈する余地があった。", text_en: "It left room to interpret the result in my own context." },
        { name: "sous_5", text: "不安を過度に増やさずに振り返れそうだと感じた。", text_en: "I felt I could reflect without excessive anxiety." }
      ]
    },
    {
      key: "wu",
      title: "WU: Willingness to Use",
      title_en: "WU: Willingness to Use",
      items: [
        { name: "wu_1", text: "このシステムを自分の日常で使ってもよいと思った。", text_en: "I would be willing to use this system in my daily life." },
        { name: "wu_2", text: "このシステムなら、不調を抱えたまま作業しているときにも使えそうだと思った。", text_en: "I felt this system could be used when working while unwell." },
        { name: "wu_3", text: "このシステムは自分のための支援として受け入れられると感じた。", text_en: "I felt this system was acceptable as support for myself." }
      ]
    },
    {
      key: "wd",
      title: "WD: Willingness to Disclose",
      title_en: "WD: Willingness to Disclose",
      items: [
        { name: "wd_1", text: "このシステムになら、自分の状態に関する情報を扱わせてもよいと思った。", text_en: "I would allow this system to handle information about my state." },
        { name: "wd_2", text: "このシステムの仕組みなら、安心して自己観察に使えそうだと思った。", text_en: "With this system design, I felt I could use it for self-observation with peace of mind." },
        { name: "wd_3", text: "このシステムが扱う情報の範囲は許容できると感じた。", text_en: "I felt the scope of information handled by this system was acceptable." }
      ]
    }
  ];

  PSTT.scaleItemNames = PSTT.questionGroups.flatMap((group) => group.items.map((item) => item.name));
})(window);
