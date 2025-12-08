// Trivia 類別定義
export const TRIVIA_CATEGORIES = {
    etiquette: { zh: "餐桌禮儀", en: "Etiquette" },
    seasonality: { zh: "旬之味", en: "Seasonality" },
    myth: { zh: "迷思破解", en: "Myth Busting" }
} as const;

export type TriviaCategory = keyof typeof TRIVIA_CATEGORIES;

export interface TriviaQuestion {
    category: TriviaCategory;
    question: { zh: string; en: string };
    answer: { zh: string; en: string };
}

export const TRIVIA_QUESTIONS: TriviaQuestion[] = [
    // ===== 餐桌禮儀與文化 (20題) =====
    {
        category: "etiquette",
        question: {
            zh: "吃握壽司可以把山葵(Wasabi)攪進醬油嗎？",
            en: "Should you mix wasabi into your soy sauce when eating sushi?"
        },
        answer: {
            zh: "不建議。高階壽司師傅通常已將適量山葵放在魚料與飯之間。攪拌會破壞醬油風味，也抹殺了師傅的調味平衡。",
            en: "Not recommended. High-end sushi chefs already place the right amount of wasabi between the fish and rice. Mixing destroys the soy sauce flavor and the chef's intended balance."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "喝西式濃湯時，湯匙應該往哪個方向舀？",
            en: "Which direction should you scoop soup with your spoon in Western dining?"
        },
        answer: {
            zh: "由內向外。這源自於宮廷禮儀，目的是避免湯汁濺到自己身上。",
            en: "Away from you (outward). This court etiquette prevents soup from splashing onto your clothes."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "暫時離開座位時，餐巾應該放在哪裡？",
            en: "Where should you place your napkin when temporarily leaving the table?"
        },
        answer: {
            zh: "放在椅子上。這暗示服務生你還會回來。若放在桌上，通常代表用餐完畢。",
            en: "On your chair. This signals to the server that you'll return. Placing it on the table means you're finished."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "吃義大利麵可以用湯匙輔助嗎？",
            en: "Is it proper to use a spoon to help twirl pasta?"
        },
        answer: {
            zh: "在義大利，成年人通常只用叉子利用盤緣捲麵。用湯匙輔助通常是給小孩或遊客的習慣，但並非絕對禁止。",
            en: "In Italy, adults typically only use a fork against the plate's edge. Using a spoon is common for children or tourists, but not strictly forbidden."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "吃中式合菜，筷子可以插在碗裡嗎？",
            en: "Can you stick chopsticks upright in your rice bowl?"
        },
        answer: {
            zh: "絕對禁止。這像祭拜亡者的腳尾飯。另外也不可用筷子敲碗，那是乞丐乞討的動作。",
            en: "Absolutely not. This resembles incense offerings for the deceased. Also avoid tapping bowls with chopsticks, which resembles begging."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "在日本吃拉麵發出聲音是禮貌嗎？",
            en: "Is slurping noodles considered polite in Japan?"
        },
        answer: {
            zh: "是的。吸麵（Slurping）能讓麵條與空氣一同入口，散發香氣並降溫，是對廚師表示「好吃」的聲音。",
            en: "Yes! Slurping brings air with the noodles, enhancing aroma and cooling them. It signals appreciation to the chef."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "拿紅酒杯應該握哪裡？",
            en: "Where should you hold a wine glass?"
        },
        answer: {
            zh: "握杯腳（Stem）。握杯肚會透過手溫影響酒的溫度，特別是白酒與香檳。",
            en: "By the stem. Holding the bowl transfers body heat, affecting the wine's temperature, especially for whites and champagne."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "吃整條煎魚時，可以翻面嗎？",
            en: "Should you flip a whole fish when eating?"
        },
        answer: {
            zh: "中式傳統忌諱翻魚（象徵翻船），建議將魚骨剔除後繼續吃下面。西餐則無此忌諱，但通常會先去骨。",
            en: "In Chinese tradition, flipping symbolizes capsizing a boat—bad luck. Remove the bones instead. Western dining has no such taboo."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "高級壽司店（Omakase）可以擦香水嗎？",
            en: "Can you wear perfume to a high-end Omakase restaurant?"
        },
        answer: {
            zh: "強烈不建議。香水會干擾精細的魚生氣味，也會影響鄰座客人的體驗，這是嚴重的不禮貌。",
            en: "Strongly discouraged. Perfume interferes with delicate fish aromas and affects other guests. It's considered very impolite."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "麵包盤上的麵包該怎麼吃？",
            en: "How should you eat bread from the bread plate?"
        },
        answer: {
            zh: "撕成一口大小，再塗奶油。不要整顆拿起來啃，也不要一次把整顆切開塗滿奶油。",
            en: "Tear off bite-sized pieces and butter each piece individually. Don't bite the whole roll or pre-butter the entire thing."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "別人幫你倒茶時，手指敲桌子是什麼意思？",
            en: "What does tapping fingers on the table mean when someone pours tea for you?"
        },
        answer: {
            zh: "這是「扣謝禮」。源自乾隆下江南的故事，用手指模擬下跪磕頭，表示感謝。",
            en: "This is a 'finger kowtow' of thanks. Legend says Emperor Qianlong's servants used this gesture to thank him incognito."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "西餐刀叉擺成「八」字型代表什麼？",
            en: "What does placing knife and fork in a 'V' shape mean?"
        },
        answer: {
            zh: "代表「暫停用餐」。若刀叉平行斜放（通常是四點鐘方向），則代表「用餐完畢」。",
            en: "'I'm still eating.' Placing them parallel at 4 o'clock position means 'I'm finished.'"
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "可以直接用手拿壽司吃嗎？",
            en: "Is it acceptable to eat sushi with your hands?"
        },
        answer: {
            zh: "可以，甚至有些師傅更推薦用手，因為這能避免筷子夾散空氣感極佳的舍利（醋飯）。",
            en: "Yes, some chefs prefer it! Hands prevent chopsticks from crushing the delicately airy shari (vinegared rice)."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "與人乾杯時，杯緣要比對方低嗎？",
            en: "Should your glass be lower than others when toasting in Asia?"
        },
        answer: {
            zh: "在東亞文化（如日韓台），晚輩或下屬的杯緣應低於長輩或上司，以示尊敬。",
            en: "In East Asian cultures (Japan, Korea, Taiwan), juniors should hold their glass lower than seniors as a sign of respect."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "可以用筷子互相傳遞食物嗎？",
            en: "Can you pass food from chopsticks to chopsticks?"
        },
        answer: {
            zh: "在日本絕對禁止。這動作類似火葬後撿骨的儀式（箸渡），極度不吉利。",
            en: "Absolutely forbidden in Japan. This mimics the bone-picking ritual after cremation and is extremely inauspicious."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "法式料理中，鹽罐與胡椒罐可以分開傳遞嗎？",
            en: "In French dining, can you pass the salt and pepper separately?"
        },
        answer: {
            zh: "通常建議一起傳遞。它們被視為「夫妻」，即便對方只要鹽，也要一起遞過去。",
            en: "Pass them together. They're considered 'married.' Even if someone only wants salt, pass both."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "牛排應該一次切完還是邊吃邊切？",
            en: "Should you cut your entire steak at once or cut as you eat?"
        },
        answer: {
            zh: "邊吃邊切。一次切完會讓肉汁流失過快，且容易讓肉變涼。",
            en: "Cut as you eat. Pre-cutting causes juices to escape faster and the meat to cool quicker."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "在韓國喝酒可以自己倒酒嗎？",
            en: "In Korea, is it okay to pour your own drink?"
        },
        answer: {
            zh: "通常不建議。韓國文化重視互動，互相倒酒（對酌）是禮貌，獨酌則顯得孤單或無禮。",
            en: "Not recommended. Korean culture values interaction—pouring for each other shows respect. Pouring for yourself seems lonely or rude."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "可以用自己的筷子夾公用盤的菜嗎？",
            en: "Can you use your personal chopsticks to take food from shared plates?"
        },
        answer: {
            zh: "若無公筷，在親近親友間尚可，但在正式場合或日本，應使用公筷或將筷子倒過來使用。",
            en: "Among close family it's tolerable, but in formal settings or Japan, use serving chopsticks or the reverse end of your own."
        }
    },
    {
        category: "etiquette",
        question: {
            zh: "小費（Tipping）是必須的嗎？",
            en: "Is tipping mandatory?"
        },
        answer: {
            zh: "視國家而定。美國必須（約15-20%），日本則不需要（甚至可能被視為無禮），歐洲多數已含服務費，只需留零頭。",
            en: "Depends on the country. Essential in the US (15-20%), unnecessary in Japan (even offensive), mostly included in Europe (just round up)."
        }
    },

    // ===== 旬之味 (20題) =====
    {
        category: "seasonality",
        question: {
            zh: "為什麼說「R月份」才吃生蠔？",
            en: "Why should you only eat oysters in months with an 'R'?"
        },
        answer: {
            zh: "傳統認為含R的月份（Sep-Apr）適合吃。5-8月是生蠔繁殖期，肉質軟爛且易滋生細菌（但在現代養殖技術下已非絕對）。",
            en: "Tradition says months with 'R' (Sep-Apr) are best. May-Aug is spawning season with softer meat and higher bacteria risk—though modern farming has largely solved this."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "吃螃蟹有「九雌十雄」的說法？",
            en: "What does 'Female in September, Male in October' mean for crabs?"
        },
        answer: {
            zh: "是的。農曆九月母蟹卵滿（蟹黃），十月公蟹性腺發育成熟（蟹膏/白膠），是風味最佳的時刻。",
            en: "In lunar September, female crabs are full of roe (crab butter). In October, male crabs have mature gonads (crab paste). Each peaks at different times."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "白蘆筍為什麼比綠蘆筍貴且產季短？",
            en: "Why is white asparagus more expensive with a shorter season?"
        },
        answer: {
            zh: "白蘆筍需全程避光種植（培土），採收費工。產季通常僅在春末夏初（4-6月），被稱為「盤中的白金」。",
            en: "White asparagus must be grown covered from light (earthed up), making harvest labor-intensive. Season is only April-June, earning it the name 'white gold.'"
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "黑松露與白松露的季節一樣嗎？",
            en: "Do black and white truffles have the same season?"
        },
        answer: {
            zh: "不同。白松露產季極短（約10-12月），黑松露則在冬季（12-3月）。白松露通常生食聞香，黑松露可烹調。",
            en: "No. White truffle season is very short (Oct-Dec), while black truffle runs Dec-Mar. White truffles are shaved raw; black can be cooked."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "日本「初鰹」為什麼受歡迎？",
            en: "Why is 'Hatsu-gatsuo' (first bonito) so prized in Japan?"
        },
        answer: {
            zh: "春季北上的鰹魚油脂較少，肉質清爽赤紅，被江戶人視為「吉利」的象徵，代表夏天的來臨。",
            en: "Spring bonito traveling north is leaner with bright red, refreshing flesh. Edo-period people saw it as lucky, heralding summer's arrival."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "海膽（Uni）最好吃的季節是？",
            en: "When is sea urchin (uni) at its best?"
        },
        answer: {
            zh: "通常是夏季（6-8月）。這是海膽產卵前的時期，生殖腺（即我們吃的部分）最為飽滿鮮甜。",
            en: "Usually summer (June-August). This is just before spawning, when the gonads (the part we eat) are fullest and sweetest."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "為什麼冬天的蘿蔔比較好吃？",
            en: "Why are winter radishes sweeter?"
        },
        answer: {
            zh: "為了抵抗寒冷不結冰，蘿蔔會將澱粉轉化為糖分，因此冬天的蘿蔔特別甘甜且水分足。",
            en: "To survive cold without freezing, radishes convert starch to sugar. Winter radishes are especially sweet and juicy."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "烏魚子是台灣冬天的特產？",
            en: "Is mullet roe a Taiwanese winter specialty?"
        },
        answer: {
            zh: "是的。冬至前後十天是烏魚群洄游至台灣海峽產卵的季節，此時的烏魚子（卵巢）最為肥美。",
            en: "Yes! Around the winter solstice, mullet migrate to Taiwan Strait to spawn. Their roe is at peak richness during this time."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "法國薄酒萊新酒（Beaujolais Nouveau）何時上市？",
            en: "When is Beaujolais Nouveau released?"
        },
        answer: {
            zh: "每年11月的第三個星期四。這是當年採收葡萄釀製的第一批酒，象徵慶祝豐收，需趁新鮮飲用。",
            en: "The third Thursday of November each year. It's the first wine from that year's harvest, celebrating the vintage—drink it fresh!"
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "秋刀魚為什麼叫秋刀魚？",
            en: "Why is Pacific saury called 'autumn knife fish' in Asia?"
        },
        answer: {
            zh: "因為其身形如刀，且在秋季最為肥美（脂肪含量可達20%），是日本秋之味覺的代表。",
            en: "Its body is knife-shaped, and it's fattest in autumn (up to 20% fat content). It's the quintessential taste of Japanese fall."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "綠竹筍為什麼要在天亮前採收？",
            en: "Why must bamboo shoots be harvested before dawn?"
        },
        answer: {
            zh: "竹筍一見光就會進行光合作用產生「紫杉氰醣苷」，導致變苦（出青）。天亮前採收最鮮甜。",
            en: "Once exposed to light, bamboo shoots photosynthesize and produce bitter compounds. Pre-dawn harvest ensures maximum sweetness."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "夏天吃鰻魚是日本傳統？",
            en: "Is eating eel in summer a Japanese tradition?"
        },
        answer: {
            zh: "是的，源自「土用丑日」吃鰻魚補元氣的習俗。雖然鰻魚其實在秋冬更肥美，但夏天吃是為了對抗酷暑。",
            en: "Yes, from the 'Doyo no Ushi no Hi' tradition. Though eel is actually fattier in fall/winter, eating it in summer was believed to combat heat fatigue."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "草莓其實是冬天的水果？",
            en: "Are strawberries actually a winter fruit?"
        },
        answer: {
            zh: "在台灣，草莓季從12月延續到4月。低溫有利於草莓累積糖分與香氣。",
            en: "In Taiwan, strawberry season runs December to April. Cold temperatures help strawberries accumulate more sugar and aroma."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "什麼是「春羊」（Spring Lamb）？",
            en: "What is 'Spring Lamb'?"
        },
        answer: {
            zh: "指出生3-5個月尚未斷奶的羔羊，通常在春季上市。肉質呈現粉紅色，羶味極低且口感細嫩。",
            en: "Lamb born 3-5 months ago, still milk-fed, typically available in spring. The meat is pink, very mild, and exceptionally tender."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "屏東黑鮪魚季通常在何時？",
            en: "When is bluefin tuna season in Pingtung, Taiwan?"
        },
        answer: {
            zh: "約在4-6月。此時黑鮪魚隨著黑潮北上準備產卵，油脂豐厚，尤其是腹肉（Otoro）部位。",
            en: "April to June. Bluefin tuna ride the Kuroshio Current north to spawn, making them fattiest—especially the belly (otoro)."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "日本的新茶（Shincha）何時喝？",
            en: "When should you drink Japanese Shincha (new tea)?"
        },
        answer: {
            zh: "「八十八夜」（立春後第88天，約5月初）。此時採摘的一番茶兒茶素較少，氨基酸較多，口感最甘甜。",
            en: "Around 'Hachiju-hachiya' (88th day after spring begins, early May). This first-flush tea has less catechin, more amino acids, and the sweetest taste."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "栗子是秋天的味道？",
            en: "Are chestnuts an autumn flavor?"
        },
        answer: {
            zh: "是的。秋季栗子熟成，法式甜點蒙布朗（Mont Blanc）也是以此時的栗子泥製作，象徵秋季到來。",
            en: "Yes! Chestnuts ripen in fall. The French dessert Mont Blanc is made with autumn chestnut purée, symbolizing the season."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "河豚為什麼要在冬天吃？",
            en: "Why is fugu (pufferfish) best in winter?"
        },
        answer: {
            zh: "「秋彼岸到春彼岸」是河豚產季。冬季河豚為了禦寒堆積脂肪，且此時毒性相對較弱（仍需專業處理）。",
            en: "Season runs 'fall equinox to spring equinox.' Winter fugu store fat against the cold, and toxicity is relatively lower (still requires licensed chefs)."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "麻豆文旦是中秋節限定？",
            en: "Is pomelo a Mid-Autumn Festival exclusive?"
        },
        answer: {
            zh: "文旦通常在「白露」節氣前後採收，經過「辭水」（消水）後剛好在中秋節享用，果肉會更軟米更甜。",
            en: "Pomelos are harvested around 'White Dew' solar term, then stored to reduce moisture. They're perfectly sweet and tender by Mid-Autumn Festival."
        }
    },
    {
        category: "seasonality",
        question: {
            zh: "為什麼冬天適合吃野味（Gibier）？",
            en: "Why is winter ideal for game meat (gibier)?"
        },
        answer: {
            zh: "歐洲狩獵季通常在秋冬。此時野生動物（如鹿、野豬）為了過冬儲存了豐富脂肪，且食用橡實與野果，肉質風味最佳。",
            en: "European hunting season is fall/winter. Wild animals (deer, boar) have stored fat for winter and eaten acorns and berries, making their meat richest."
        }
    },

    // ===== 迷思破解 (20題) =====
    {
        category: "myth",
        question: {
            zh: "大火煎牛排是為了「鎖住肉汁」？",
            en: "Does searing steak at high heat 'seal in the juices'?"
        },
        answer: {
            zh: "這是迷思。實驗證明煎過的表皮無法防水。梅納反應是為了產生香氣。肉汁流失主要取決於內部溫度與靜置時間。",
            en: "This is a myth. Experiments show seared surfaces don't seal anything. The Maillard reaction creates flavor. Juice loss depends on internal temp and resting time."
        }
    },
    {
        category: "myth",
        question: {
            zh: "三分熟牛排流出的紅色液體是血？",
            en: "Is the red liquid in rare steak blood?"
        },
        answer: {
            zh: "不是。那是肌紅蛋白（Myoglobin）與水的混合物。屠宰放血後，肉中基本已無血液。不需因此害怕點三分熟。",
            en: "No. It's myoglobin mixed with water. After slaughter and bleeding, there's virtually no blood left in meat. Don't fear ordering rare!"
        }
    },
    {
        category: "myth",
        question: {
            zh: "味精（MSG）對人體有害？",
            en: "Is MSG harmful to your health?"
        },
        answer: {
            zh: "科學上無證據。味精只是麩胺酸鈉，天然存在於番茄、起司中。所謂「中國餐館症候群」已被證實是安慰劑效應或對其他成分過敏。",
            en: "No scientific evidence. MSG is just sodium glutamate, naturally found in tomatoes and cheese. 'Chinese Restaurant Syndrome' has been debunked as placebo or other allergies."
        }
    },
    {
        category: "myth",
        question: {
            zh: "用酒精入菜，酒精會完全揮發嗎？",
            en: "Does all the alcohol cook off when you add wine to food?"
        },
        answer: {
            zh: "很難。即便燉煮2.5小時，仍可能殘留5%酒精；短暫燃燒（Flambé）更只能去除約25%酒精。孕婦或駕駛需注意。",
            en: "No. Even after 2.5 hours of simmering, 5% may remain. Flambéing only removes about 25%. Pregnant women and drivers should be aware."
        }
    },
    {
        category: "myth",
        question: {
            zh: "「辣」是一種味覺嗎？",
            en: "Is 'spicy' a taste?"
        },
        answer: {
            zh: "不是。辣是一種「痛覺」（熱覺）。辣椒素刺激三叉神經，大腦誤以為被火燒，因此會釋放腦內啡止痛，產生快感。",
            en: "No—it's actually pain (heat perception). Capsaicin triggers trigeminal nerves, making your brain think you're burning, releasing endorphins for relief and pleasure."
        }
    },
    {
        category: "myth",
        question: {
            zh: "微波爐加熱會破壞食物營養？",
            en: "Does microwaving destroy food nutrients?"
        },
        answer: {
            zh: "大部分情況下不會。微波加熱時間短、用水少，反而比水煮更能保留水溶性維生素（如維生素C）。",
            en: "Usually no. Microwaving uses less time and water, actually preserving more water-soluble vitamins (like Vitamin C) than boiling."
        }
    },
    {
        category: "myth",
        question: {
            zh: "木頭砧板比塑膠砧板容易滋生細菌？",
            en: "Do wooden cutting boards harbor more bacteria than plastic?"
        },
        answer: {
            zh: "不一定。木頭有天然抗菌特性，且刀痕會癒合。塑膠砧板的刀痕深處反而容易藏污納垢且難以清洗。",
            en: "Not necessarily. Wood has natural antimicrobial properties and its knife scars heal. Plastic cutting boards trap bacteria in deep grooves that are hard to clean."
        }
    },
    {
        category: "myth",
        question: {
            zh: "現宰的牛肉一定比冷藏的好吃？",
            en: "Is freshly slaughtered beef better than aged beef?"
        },
        answer: {
            zh: "未必。死後肌肉會僵直。牛肉通常需要經過「濕式」或「乾式」熟成，讓酵素軟化結締組織並濃縮風味，才最好吃。",
            en: "Not at all. Rigor mortis makes fresh meat tough. Beef needs wet or dry aging for enzymes to tenderize connective tissue and concentrate flavor."
        }
    },
    {
        category: "myth",
        question: {
            zh: "豬肉一定要煮到全熟？",
            en: "Must pork always be cooked well-done?"
        },
        answer: {
            zh: "現代豬肉（特別是高階豬種）已大幅減少寄生蟲風險。美國農業部建議豬肉中心溫度達63°C（約粉紅色）即可安全食用且口感最佳。",
            en: "Not anymore. Modern pork (especially premium breeds) has minimal parasite risk. USDA says 145°F (63°C) internal temp—still slightly pink—is safe and optimal."
        }
    },
    {
        category: "myth",
        question: {
            zh: "喝咖啡會導致脫水？",
            en: "Does coffee cause dehydration?"
        },
        answer: {
            zh: "對習慣喝咖啡的人來說，利尿效果輕微，其水分補充的效果大於利尿。咖啡仍可計入每日飲水量。",
            en: "For regular coffee drinkers, the diuretic effect is mild. Coffee's hydration outweighs fluid loss—it counts toward daily water intake."
        }
    },
    {
        category: "myth",
        question: {
            zh: "吃糖會讓小孩過動（Sugar Rush）？",
            en: "Does sugar make kids hyperactive?"
        },
        answer: {
            zh: "這是廣泛的迷思。多項雙盲測試顯示，糖攝取與兒童行為改變無直接關聯。興奮通常來自派對環境本身。",
            en: "A widespread myth. Multiple double-blind studies show no direct link between sugar and behavior changes. Excitement usually comes from the party environment itself."
        }
    },
    {
        category: "myth",
        question: {
            zh: "喝排毒果汁可以「排毒」？",
            en: "Can detox juices 'cleanse' your body?"
        },
        answer: {
            zh: "不需要。肝臟和腎臟是最高效的排毒器官。果汁只有糖分高與纖維少的缺點，無法強化排毒功能。",
            en: "No. Your liver and kidneys are the most efficient detox organs. Juice cleanses just add sugar, remove fiber, and can't enhance your body's natural detoxification."
        }
    },
    {
        category: "myth",
        question: {
            zh: "有機農業完全不使用農藥？",
            en: "Does organic farming use no pesticides?"
        },
        answer: {
            zh: "錯誤。有機農業可以使用「天然來源」的農藥（如除蟲菊精）。天然農藥不代表對環境或人體完全無毒。",
            en: "False. Organic farming can use 'naturally derived' pesticides (like pyrethrin). Natural doesn't mean completely safe for the environment or humans."
        }
    },
    {
        category: "myth",
        question: {
            zh: "鑄鐵鍋絕對不能用洗碗精洗？",
            en: "Should you never use soap on cast iron?"
        },
        answer: {
            zh: "現代洗碗精很溫和，不會洗掉聚合的油膜（Seasoning）。只要不長時間浸泡或用強酸，偶爾用洗碗精清潔是可以的。",
            en: "Modern dish soap is mild and won't strip polymerized seasoning. Occasional soap use is fine—just don't soak for long or use harsh acids."
        }
    },
    {
        category: "myth",
        question: {
            zh: "煮義大利麵要在水裡加油防沾黏？",
            en: "Should you add oil to pasta water to prevent sticking?"
        },
        answer: {
            zh: "沒用。油會浮在水面，碰到麵體的機會很少。且油包覆麵體會導致醬汁掛不上去。防沾黏的關鍵是水滾、足量且適時攪拌。",
            en: "No use. Oil floats and rarely touches pasta. Oily pasta also repels sauce. The real keys: boiling water, enough water, and stirring occasionally."
        }
    },
    {
        category: "myth",
        question: {
            zh: "醃肉越久越入味？",
            en: "Does marinating longer make meat more flavorful?"
        },
        answer: {
            zh: "大部分醃料（除了鹽）的分子太大，只能滲透表層幾毫米。長時間醃漬反而可能讓酸性物質破壞肉質，使其軟爛。",
            en: "Most marinade molecules (except salt) are too large to penetrate beyond a few millimeters. Over-marinating lets acids break down meat texture, making it mushy."
        }
    },
    {
        category: "myth",
        question: {
            zh: "煮水加鹽會讓水更快滾？",
            en: "Does adding salt make water boil faster?"
        },
        answer: {
            zh: "理論上會（沸點升高比熱降低），但以烹飪的鹽量來說，時間差距微乎其微（不到一秒），加鹽主要是為了調味。",
            en: "Technically yes (higher boiling point, lower heat capacity), but at cooking salt levels, the difference is under a second. Salt's real purpose is flavor."
        }
    },
    {
        category: "myth",
        question: {
            zh: "煮完義大利麵要沖冷水？",
            en: "Should you rinse pasta after cooking?"
        },
        answer: {
            zh: "除非做冷麵沙拉，否則不要。沖水會洗掉表面的澱粉，讓醬汁無法吸附在麵條上。",
            en: "Only for cold pasta salads. Rinsing washes off surface starch that helps sauce cling to the noodles."
        }
    },
    {
        category: "myth",
        question: {
            zh: "牛排全熟比較安全？",
            en: "Is well-done steak safer than rare?"
        },
        answer: {
            zh: "牛肉內層通常是無菌的（細菌在表面）。只要將表面煎熟，內部生食風險極低。絞肉（漢堡排）才需要全熟，因為表面細菌已被絞進內部。",
            en: "Steak interior is usually sterile (bacteria stay on the surface). Searing the outside is enough. Ground beef (burgers) needs thorough cooking since surface bacteria get mixed throughout."
        }
    },
    {
        category: "myth",
        question: {
            zh: "吃辣喝牛奶比喝水有效？",
            en: "Is milk better than water for cooling spicy heat?"
        },
        answer: {
            zh: "是的。辣椒素是脂溶性的。水無法溶解它，只能暫時冷卻。牛奶中的酪蛋白（Casein）能有效結合併洗去辣椒素。",
            en: "Yes. Capsaicin is fat-soluble. Water can't dissolve it, only temporarily cool your mouth. Milk's casein protein effectively binds to and washes away capsaicin."
        }
    },
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

// 取得類別顯示名稱
export function getCategoryName(category: TriviaCategory, locale: 'zh' | 'en' = 'zh'): string {
    return TRIVIA_CATEGORIES[category][locale];
}
