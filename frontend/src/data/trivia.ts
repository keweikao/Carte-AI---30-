// Trivia 類別定義
export const TRIVIA_CATEGORIES = {
    etiquette: "餐桌禮儀",
    seasonality: "旬之味",
    myth: "迷思破解"
} as const;

export type TriviaCategory = keyof typeof TRIVIA_CATEGORIES;

export interface TriviaQuestion {
    category: TriviaCategory;
    question: string;
    answer: string;
}

export const TRIVIA_QUESTIONS: TriviaQuestion[] = [
    // ===== 餐桌禮儀與文化 (20題) =====
    { category: "etiquette", question: "吃握壽司可以把山葵(Wasabi)攪進醬油嗎？", answer: "不建議。高階壽司師傅通常已將適量山葵放在魚料與飯之間。攪拌會破壞醬油風味，也抹殺了師傅的調味平衡。" },
    { category: "etiquette", question: "喝西式濃湯時，湯匙應該往哪個方向舀？", answer: "由內向外。這源自於宮廷禮儀，目的是避免湯汁濺到自己身上。" },
    { category: "etiquette", question: "暫時離開座位時，餐巾應該放在哪裡？", answer: "放在椅子上。這暗示服務生你還會回來。若放在桌上，通常代表用餐完畢。" },
    { category: "etiquette", question: "吃義大利麵可以用湯匙輔助嗎？", answer: "在義大利，成年人通常只用叉子利用盤緣捲麵。用湯匙輔助通常是給小孩或遊客的習慣，但並非絕對禁止。" },
    { category: "etiquette", question: "吃中式合菜，筷子可以插在碗裡嗎？", answer: "絕對禁止。這像祭拜亡者的腳尾飯。另外也不可用筷子敲碗，那是乞丐乞討的動作。" },
    { category: "etiquette", question: "在日本吃拉麵發出聲音是禮貌嗎？", answer: "是的。吸麵（Slurping）能讓麵條與空氣一同入口，散發香氣並降溫，是對廚師表示「好吃」的聲音。" },
    { category: "etiquette", question: "拿紅酒杯應該握哪裡？", answer: "握杯腳（Stem）。握杯肚會透過手溫影響酒的溫度，特別是白酒與香檳。" },
    { category: "etiquette", question: "吃整條煎魚時，可以翻面嗎？", answer: "中式傳統忌諱翻魚（象徵翻船），建議將魚骨剔除後繼續吃下面。西餐則無此忌諱，但通常會先去骨。" },
    { category: "etiquette", question: "高級壽司店（Omakase）可以擦香水嗎？", answer: "強烈不建議。香水會干擾精細的魚生氣味，也會影響鄰座客人的體驗，這是嚴重的不禮貌。" },
    { category: "etiquette", question: "麵包盤上的麵包該怎麼吃？", answer: "撕成一口大小，再塗奶油。不要整顆拿起來啃，也不要一次把整顆切開塗滿奶油。" },
    { category: "etiquette", question: "別人幫你倒茶時，手指敲桌子是什麼意思？", answer: "這是「扣謝禮」。源自乾隆下江南的故事，用手指模擬下跪磕頭，表示感謝。" },
    { category: "etiquette", question: "西餐刀叉擺成「八」字型代表什麼？", answer: "代表「暫停用餐」。若刀叉平行斜放（通常是四點鐘方向），則代表「用餐完畢」。" },
    { category: "etiquette", question: "可以直接用手拿壽司吃嗎？", answer: "可以，甚至有些師傅更推薦用手，因為這能避免筷子夾散空氣感極佳的舍利（醋飯）。" },
    { category: "etiquette", question: "與人乾杯時，杯緣要比對方低嗎？", answer: "在東亞文化（如日韓台），晚輩或下屬的杯緣應低於長輩或上司，以示尊敬。" },
    { category: "etiquette", question: "可以用筷子互相傳遞食物嗎？", answer: "在日本絕對禁止。這動作類似火葬後撿骨的儀式（箸渡），極度不吉利。" },
    { category: "etiquette", question: "法式料理中，鹽罐與胡椒罐可以分開傳遞嗎？", answer: "通常建議一起傳遞。它們被視為「夫妻」，即便對方只要鹽，也要一起遞過去。" },
    { category: "etiquette", question: "牛排應該一次切完還是邊吃邊切？", answer: "邊吃邊切。一次切完會讓肉汁流失過快，且容易讓肉變涼。" },
    { category: "etiquette", question: "在韓國喝酒可以自己倒酒嗎？", answer: "通常不建議。韓國文化重視互動，互相倒酒（對酌）是禮貌，獨酌則顯得孤單或無禮。" },
    { category: "etiquette", question: "可以用自己的筷子夾公用盤的菜嗎？", answer: "若無公筷，在親近親友間尚可，但在正式場合或日本，應使用公筷或將筷子倒過來使用。" },
    { category: "etiquette", question: "小費（Tipping）是必須的嗎？", answer: "視國家而定。美國必須（約15-20%），日本則不需要（甚至可能被視為無禮），歐洲多數已含服務費，只需留零頭。" },

    // ===== 旬之味 (20題) =====
    { category: "seasonality", question: "為什麼說「R月份」才吃生蠔？", answer: "傳統認為含R的月份（Sep-Apr）適合吃。5-8月是生蠔繁殖期，肉質軟爛且易滋生細菌（但在現代養殖技術下已非絕對）。" },
    { category: "seasonality", question: "吃螃蟹有「九雌十雄」的說法？", answer: "是的。農曆九月母蟹卵滿（蟹黃），十月公蟹性腺發育成熟（蟹膏/白膠），是風味最佳的時刻。" },
    { category: "seasonality", question: "白蘆筍為什麼比綠蘆筍貴且產季短？", answer: "白蘆筍需全程避光種植（培土），採收費工。產季通常僅在春末夏初（4-6月），被稱為「盤中的白金」。" },
    { category: "seasonality", question: "黑松露與白松露的季節一樣嗎？", answer: "不同。白松露產季極短（約10-12月），黑松露則在冬季（12-3月）。白松露通常生食聞香，黑松露可烹調。" },
    { category: "seasonality", question: "日本「初鰹」為什麼受歡迎？", answer: "春季北上的鰹魚油脂較少，肉質清爽赤紅，被江戶人視為「吉利」的象徵，代表夏天的來臨。" },
    { category: "seasonality", question: "海膽（Uni）最好吃的季節是？", answer: "通常是夏季（6-8月）。這是海膽產卵前的時期，生殖腺（即我們吃的部分）最為飽滿鮮甜。" },
    { category: "seasonality", question: "為什麼冬天的蘿蔔比較好吃？", answer: "為了抵抗寒冷不結冰，蘿蔔會將澱粉轉化為糖分，因此冬天的蘿蔔特別甘甜且水分足。" },
    { category: "seasonality", question: "烏魚子是台灣冬天的特產？", answer: "是的。冬至前後十天是烏魚群洄游至台灣海峽產卵的季節，此時的烏魚子（卵巢）最為肥美。" },
    { category: "seasonality", question: "法國薄酒萊新酒（Beaujolais Nouveau）何時上市？", answer: "每年11月的第三個星期四。這是當年採收葡萄釀製的第一批酒，象徵慶祝豐收，需趁新鮮飲用。" },
    { category: "seasonality", question: "秋刀魚為什麼叫秋刀魚？", answer: "因為其身形如刀，且在秋季最為肥美（脂肪含量可達20%），是日本秋之味覺的代表。" },
    { category: "seasonality", question: "綠竹筍為什麼要在天亮前採收？", answer: "竹筍一見光就會進行光合作用產生「紫杉氰醣苷」，導致變苦（出青）。天亮前採收最鮮甜。" },
    { category: "seasonality", question: "夏天吃鰻魚是日本傳統？", answer: "是的，源自「土用丑日」吃鰻魚補元氣的習俗。雖然鰻魚其實在秋冬更肥美，但夏天吃是為了對抗酷暑。" },
    { category: "seasonality", question: "草莓其實是冬天的水果？", answer: "在台灣，草莓季從12月延續到4月。低溫有利於草莓累積糖分與香氣。" },
    { category: "seasonality", question: "什麼是「春羊」（Spring Lamb）？", answer: "指出生3-5個月尚未斷奶的羔羊，通常在春季上市。肉質呈現粉紅色，羶味極低且口感細嫩。" },
    { category: "seasonality", question: "屏東黑鮪魚季通常在何時？", answer: "約在4-6月。此時黑鮪魚隨著黑潮北上準備產卵，油脂豐厚，尤其是腹肉（Otoro）部位。" },
    { category: "seasonality", question: "日本的新茶（Shincha）何時喝？", answer: "「八十八夜」（立春後第88天，約5月初）。此時採摘的一番茶兒茶素較少，氨基酸較多，口感最甘甜。" },
    { category: "seasonality", question: "栗子是秋天的味道？", answer: "是的。秋季栗子熟成，法式甜點蒙布朗（Mont Blanc）也是以此時的栗子泥製作，象徵秋季到來。" },
    { category: "seasonality", question: "河豚為什麼要在冬天吃？", answer: "「秋彼岸到春彼岸」是河豚產季。冬季河豚為了禦寒堆積脂肪，且此時毒性相對較弱（仍需專業處理）。" },
    { category: "seasonality", question: "麻豆文旦是中秋節限定？", answer: "文旦通常在「白露」節氣前後採收，經過「辭水」（消水）後剛好在中秋節享用，果肉會更軟米更甜。" },
    { category: "seasonality", question: "為什麼冬天適合吃野味（Gibier）？", answer: "歐洲狩獵季通常在秋冬。此時野生動物（如鹿、野豬）為了過冬儲存了豐富脂肪，且食用橡實與野果，肉質風味最佳。" },

    // ===== 迷思破解 (20題) =====
    { category: "myth", question: "大火煎牛排是為了「鎖住肉汁」？", answer: "這是迷思。實驗證明煎過的表皮無法防水。梅納反應是為了產生香氣。肉汁流失主要取決於內部溫度與靜置時間。" },
    { category: "myth", question: "三分熟牛排流出的紅色液體是血？", answer: "不是。那是肌紅蛋白（Myoglobin）與水的混合物。屠宰放血後，肉中基本已無血液。不需因此害怕點三分熟。" },
    { category: "myth", question: "味精（MSG）對人體有害？", answer: "科學上無證據。味精只是麩胺酸鈉，天然存在於番茄、起司中。所謂「中國餐館症候群」已被證實是安慰劑效應或對其他成分過敏。" },
    { category: "myth", question: "用酒精入菜，酒精會完全揮發嗎？", answer: "很難。即便燉煮2.5小時，仍可能殘留5%酒精；短暫燃燒（Flambé）更只能去除約25%酒精。孕婦或駕駛需注意。" },
    { category: "myth", question: "「辣」是一種味覺嗎？", answer: "不是。辣是一種「痛覺」（熱覺）。辣椒素刺激三叉神經，大腦誤以為被火燒，因此會釋放腦內啡止痛，產生快感。" },
    { category: "myth", question: "微波爐加熱會破壞食物營養？", answer: "大部分情況下不會。微波加熱時間短、用水少，反而比水煮更能保留水溶性維生素（如維生素C）。" },
    { category: "myth", question: "木頭砧板比塑膠砧板容易滋生細菌？", answer: "不一定。木頭有天然抗菌特性，且刀痕會癒合。塑膠砧板的刀痕深處反而容易藏污納垢且難以清洗。" },
    { category: "myth", question: "現宰的牛肉一定比冷藏的好吃？", answer: "未必。死後肌肉會僵直。牛肉通常需要經過「濕式」或「乾式」熟成，讓酵素軟化結締組織並濃縮風味，才最好吃。" },
    { category: "myth", question: "豬肉一定要煮到全熟？", answer: "現代豬肉（特別是高階豬種）已大幅減少寄生蟲風險。美國農業部建議豬肉中心溫度達63°C（約粉紅色）即可安全食用且口感最佳。" },
    { category: "myth", question: "喝咖啡會導致脫水？", answer: "對習慣喝咖啡的人來說，利尿效果輕微，其水分補充的效果大於利尿。咖啡仍可計入每日飲水量。" },
    { category: "myth", question: "吃糖會讓小孩過動（Sugar Rush）？", answer: "這是廣泛的迷思。多項雙盲測試顯示，糖攝取與兒童行為改變無直接關聯。興奮通常來自派對環境本身。" },
    { category: "myth", question: "喝排毒果汁可以「排毒」？", answer: "不需要。肝臟和腎臟是最高效的排毒器官。果汁只有糖分高與纖維少的缺點，無法強化排毒功能。" },
    { category: "myth", question: "有機農業完全不使用農藥？", answer: "錯誤。有機農業可以使用「天然來源」的農藥（如除蟲菊精）。天然農藥不代表對環境或人體完全無毒。" },
    { category: "myth", question: "鑄鐵鍋絕對不能用洗碗精洗？", answer: "現代洗碗精很溫和，不會洗掉聚合的油膜（Seasoning）。只要不長時間浸泡或用強酸，偶爾用洗碗精清潔是可以的。" },
    { category: "myth", question: "煮義大利麵要在水裡加油防沾黏？", answer: "沒用。油會浮在水面，碰到麵體的機會很少。且油包覆麵體會導致醬汁掛不上去。防沾黏的關鍵是水滾、足量且適時攪拌。" },
    { category: "myth", question: "醃肉越久越入味？", answer: "大部分醃料（除了鹽）的分子太大，只能滲透表層幾毫米。長時間醃漬反而可能讓酸性物質破壞肉質，使其軟爛。" },
    { category: "myth", question: "煮水加鹽會讓水更快滾？", answer: "理論上會（沸點升高比熱降低），但以烹飪的鹽量來說，時間差距微乎其微（不到一秒），加鹽主要是為了調味。" },
    { category: "myth", question: "煮完義大利麵要沖冷水？", answer: "除非做冷麵沙拉，否則不要。沖水會洗掉表面的澱粉，讓醬汁無法吸附在麵條上。" },
    { category: "myth", question: "牛排全熟比較安全？", answer: "牛肉內層通常是無菌的（細菌在表面）。只要將表面煎熟，內部生食風險極低。絞肉（漢堡排）才需要全熟，因為表面細菌已被絞進內部。" },
    { category: "myth", question: "吃辣喝牛奶比喝水有效？", answer: "是的。辣椒素是脂溶性的。水無法溶解它，只能暫時冷卻。牛奶中的酪蛋白（Casein）能有效結合併洗去辣椒素。" },
];

// 根據類別篩選問題
export function getQuestionsByCategory(category: TriviaCategory): TriviaQuestion[] {
    return TRIVIA_QUESTIONS.filter(q => q.category === category);
}

// 隨機取得一題
export function getRandomQuestion(): TriviaQuestion {
    return TRIVIA_QUESTIONS[Math.floor(Math.random() * TRIVIA_QUESTIONS.length)];
}

// 隨機取得指定類別的一題
export function getRandomQuestionByCategory(category: TriviaCategory): TriviaQuestion | null {
    const filtered = getQuestionsByCategory(category);
    if (filtered.length === 0) return null;
    return filtered[Math.floor(Math.random() * filtered.length)];
}
