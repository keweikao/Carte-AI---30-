/**
 * 類別順序定義
 * 依照用餐順序排列（前菜 → 主菜 → 主食 → 湯品 → 甜點）
 */
export const CATEGORY_ORDER: Record<string, string[]> = {
  "中式餐館": ["冷菜", "熱菜", "主食", "點心", "湯品"],
  "日本料理": ["刺身", "壽司", "燒烤", "麵類", "湯物"],
  "美式餐廳": ["前菜", "主餐", "配菜", "甜點", "飲料"],
  "義式料理": ["前菜", "義大利麵", "披薩", "主菜", "甜點"],
  "泰式料理": ["開胃菜", "咖哩", "炒飯麵", "湯類", "甜品"],
};

/**
 * 類別圖示對應
 */
export const CATEGORY_ICONS: Record<string, Record<string, string>> = {
  "中式餐館": {
    "冷菜": "🥶",
    "熱菜": "🔥",
    "主食": "🍚",
    "點心": "🥟",
    "湯品": "🍲",
  },
  "日本料理": {
    "刺身": "🐟",
    "壽司": "🍣",
    "燒烤": "🔥",
    "麵類": "🍜",
    "湯物": "🍵",
  },
  "美式餐廳": {
    "前菜": "🥗",
    "主餐": "🍔",
    "配菜": "🍟",
    "甜點": "🍰",
    "飲料": "🥤",
  },
  "義式料理": {
    "前菜": "🧀",
    "義大利麵": "🍝",
    "披薩": "🍕",
    "主菜": "🥩",
    "甜點": "🍰",
  },
  "泰式料理": {
    "開胃菜": "🦐",
    "咖哩": "🍛",
    "炒飯麵": "🍜",
    "湯類": "🍲",
    "甜品": "🥭",
  },
};

/**
 * 取得類別圖示
 * @param category 類別名稱（例如：「冷菜」）
 * @param cuisineType 餐廳類型（例如：「中式餐館」）
 * @returns 類別圖示 Emoji
 */
export function getCategoryIcon(category: string, cuisineType: string): string {
  return CATEGORY_ICONS[cuisineType]?.[category] || "🍽️";
}

/**
 * 取得排序後的類別列表
 * @param categories 實際出現的類別列表
 * @param cuisineType 餐廳類型
 * @returns 排序後的類別列表
 */
export function getSortedCategories(
  categories: string[],
  cuisineType: string
): string[] {
  const order = CATEGORY_ORDER[cuisineType];

  if (!order) {
    // 未知餐廳類型，使用字母排序
    return [...categories].sort();
  }

  // 依預設順序排序，未定義的類別放在最後
  const sorted: string[] = [];
  const remaining = new Set(categories);

  order.forEach(cat => {
    if (remaining.has(cat)) {
      sorted.push(cat);
      remaining.delete(cat);
    }
  });

  // 加入未定義的類別（字母排序）
  sorted.push(...Array.from(remaining).sort());

  return sorted;
}
