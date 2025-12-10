# i18n 工作流程指南

**最後更新**: 2025-12-10

這份文件說明 OderWhat 專案改進後的國際化（i18n）工作流程，讓管理多語言翻譯變得更簡單、更可維護。

---

## 🎯 改進重點

### 之前的痛點
1. ❌ 需要手動檢查所有語言檔案的一致性
2. ❌ 容易遺漏翻譯或出現結構不同步
3. ❌ 沒有 IDE 自動完成，容易打錯 key
4. ❌ 新增語言時需要大量手動工作

### 改進後的優勢
1. ✅ TypeScript 類型定義 - IDE 自動完成和類型檢查
2. ✅ 自動化一致性檢查 - 一鍵檢查所有語言檔案
3. ✅ 自動化結構同步 - 自動修復結構不一致
4. ✅ 新語言初始化 - 一行指令建立新語言檔案
5. ✅ TODO 追蹤 - 清楚知道哪些翻譯還沒完成

---

## 📁 檔案結構

```
frontend/
├── messages/           # 翻譯檔案目錄
│   ├── zh-TW.json     # 繁體中文（台灣）- 主要參考語言
│   └── en.json        # 英文
├── scripts/           # 自動化腳本
│   └── i18n-tools.js  # i18n 管理工具
└── src/
    └── types/
        └── messages.ts # TypeScript 類型定義
```

---

## 🛠️ 可用指令

### 1. `npm run i18n:check`
**用途**: 檢查所有語言檔案的一致性

```bash
npm run i18n:check
```

**檢查項目**:
- ✓ 所有語言是否有相同的 keys
- ✓ 是否有遺漏的翻譯
- ✓ 是否有多餘的 keys
- ✓ 是否有 TODO 或空白值

**輸出範例**:
```
🔍 Checking i18n consistency...

📋 Reference (zh-TW): 155 keys

Checking en...
  ✓ Perfect! All 155 keys match

✅ All locale files are consistent!
```

### 2. `npm run i18n:sync`
**用途**: 自動同步所有語言檔案的結構

```bash
npm run i18n:sync
```

**功能**:
- 根據 zh-TW.json（參考語言）同步結構
- 新增遺漏的 keys（標記為 TODO）
- 移除多餘的 keys
- 保留現有的翻譯內容

**輸出範例**:
```
🔄 Syncing locale file structures...

Syncing en...
  Adding 5 missing keys...
  ✓ Updated successfully

✅ Structure sync complete!
```

### 3. `npm run i18n:init <locale>`
**用途**: 初始化新的語言檔案

```bash
npm run i18n:init ja  # 日文
npm run i18n:init ko  # 韓文
npm run i18n:init fr  # 法文
```

**功能**:
- 根據 zh-TW.json 建立新語言檔案
- 所有值標記為 "TODO: Translate from zh-TW"
- 保持完整的結構和 keys

**輸出範例**:
```
🌐 Initializing new locale: ja

✅ Created ja.json with 155 keys (all marked TODO)
💡 Next step: Translate the TODO values in messages/ja.json
```

### 4. `npm run i18n:todos`
**用途**: 列出所有需要翻譯的項目

```bash
npm run i18n:todos
```

**功能**:
- 找出所有包含 "TODO" 的翻譯
- 找出所有空白的翻譯
- 按語言分組顯示

**輸出範例**:
```
📝 Finding all TODO translations...

ja: 155 TODOs
  - HomePage.title: "TODO: Translate from zh-TW"
  - HomePage.subtitle: "TODO: Translate from zh-TW"
  ...

Total: 155 translations need work
```

---

## 🎓 使用方式

### TypeScript 類型支援

在組件中使用翻譯時，TypeScript 會提供自動完成和類型檢查：

```typescript
"use client";

import { useTranslations } from 'next-intl';
import type { MessageNamespace } from '@/types/messages';

export default function MyPage() {
    const t = useTranslations('HomePage'); // 自動完成命名空間

    return (
        <div>
            <h1>{t('title')}</h1>  {/* 自動完成 key，打錯會報錯 */}
            <p>{t('subtitle')}</p>
        </div>
    );
}
```

**好處**:
- ✅ 輸入 `t('` 時會自動列出所有可用的 keys
- ✅ 打錯 key 時 TypeScript 會報錯
- ✅ 重構時可以安全地修改 key 名稱

### 工作流程範例

#### 場景 1: 新增頁面的翻譯

1. **更新主要語言檔案** (zh-TW.json):
```json
{
    "NewPage": {
        "title": "新頁面標題",
        "description": "這是新頁面的描述"
    }
}
```

2. **同步結構到其他語言**:
```bash
npm run i18n:sync
```

3. **檢查 TODO 項目**:
```bash
npm run i18n:todos
```

4. **翻譯其他語言** (en.json):
```json
{
    "NewPage": {
        "title": "New Page Title",
        "description": "This is the description of the new page"
    }
}
```

5. **驗證一致性**:
```bash
npm run i18n:check
```

#### 場景 2: 新增日文支援

1. **初始化日文檔案**:
```bash
npm run i18n:init ja
```

2. **翻譯 TODO 項目**:
```json
{
    "HomePage": {
        "title": "完璧な食事体験をAIが計画",  // 從 "TODO: Translate from zh-TW" 改成日文
        ...
    }
}
```

3. **更新 middleware.ts** 支援日文:
```typescript
export default createMiddleware({
    locales: ['en', 'zh-TW', 'zh', 'ja'],  // 加入 'ja'
    defaultLocale: 'zh-TW',
    // ...
});
```

4. **更新 i18n.ts** 支援日文:
```typescript
export const locales = ['zh-TW', 'zh', 'en', 'ja'] as const;
```

5. **驗證**:
```bash
npm run i18n:check
```

#### 場景 3: 重構翻譯 keys

1. **更新 TypeScript 類型** (src/types/messages.ts):
```typescript
export interface Messages {
  HomePage: {
    mainTitle: string;  // 從 'title' 改名為 'mainTitle'
    // ...
  }
}
```

2. **更新所有語言檔案**:
```bash
# zh-TW.json
"mainTitle": "讓 AI 為你策劃"  # 從 "title" 改名

# en.json
"mainTitle": "Let AI Plan"

# zh.json
"mainTitle": "讓 AI 為你策劃"
```

3. **更新組件使用**:
```typescript
const t = useTranslations('HomePage');
<h1>{t('mainTitle')}</h1>  // TypeScript 會提示這裡需要更新
```

4. **驗證**:
```bash
npm run i18n:check
```

---

## 🔄 日常工作流程

### 開發新功能時

```bash
# 1. 在 zh-TW.json 新增翻譯
vim messages/zh-TW.json

# 2. 同步結構（會自動在其他語言加入 TODO）
npm run i18n:sync

# 3. 翻譯英文版本
vim messages/en.json

# 4. 最後檢查
npm run i18n:check
```

### 提交前檢查

建議在 Git commit 前執行：

```bash
npm run i18n:check
```

或加入 pre-commit hook（可選）:

```json
// package.json
"lint-staged": {
  "*.{js,jsx,ts,tsx}": ["eslint --fix"],
  "messages/*.json": ["npm run i18n:check"]
}
```

---

## 📋 最佳實踐

### 1. Key 命名規範

✅ **推薦**:
```json
{
  "HomePage": {
    "hero_title": "標題",
    "hero_subtitle": "副標題",
    "cta_button": "按鈕文字"
  }
}
```

❌ **避免**:
```json
{
  "HomePage": {
    "1": "標題",  // 不要用數字
    "titleText": "標題",  // 駝峰式不如底線
    "按鈕": "按鈕文字"  // 不要用中文 key
  }
}
```

### 2. 組織結構

按**頁面/組件**分組：
```json
{
  "HomePage": { /* 首頁翻譯 */ },
  "Header": { /* Header 組件翻譯 */ },
  "InputPage": { /* Input 頁面翻譯 */ }
}
```

### 3. 共用翻譯

對於常用的 UI 文字，建立共用命名空間：
```json
{
  "Common": {
    "loading": "載入中...",
    "error": "發生錯誤",
    "save": "儲存",
    "cancel": "取消",
    "confirm": "確認"
  }
}
```

使用方式：
```typescript
const t = useTranslations('Common');
<button>{t('save')}</button>
```

### 4. 參數化翻譯

使用 `{variable}` 語法：
```json
{
  "MenuPage": {
    "party_info": "{people} 人用餐 · {dishes} 道菜",
    "share_text": "我在「{restaurant}」找到了完美組合！"
  }
}
```

使用方式：
```typescript
t('party_info', { people: 4, dishes: 6 })
// 輸出: "4 人用餐 · 6 道菜"
```

---

## 🐛 常見問題

### Q1: 執行 `npm run i18n:check` 失敗怎麼辦？

**A**: 執行 `npm run i18n:sync` 自動修復結構問題，然後再檢查。

### Q2: 新增的 key 在其他語言顯示 TODO，會影響網站嗎？

**A**:
- next-intl 會使用 fallback 機制
- 建議在上線前確保所有翻譯完成
- 使用 `npm run i18n:todos` 檢查待完成項目

### Q3: TypeScript 類型定義需要手動更新嗎？

**A**:
- 是的，新增 key 時需要手動更新 `src/types/messages.ts`
- 未來可以考慮自動生成（從 zh-TW.json）

### Q4: 可以同時支援多個 fallback 語言嗎？

**A**:
- 目前設定：非中文 fallback 到英文
- 如需複雜的 fallback 鏈，需要調整 `src/i18n.ts`

---

## 🚀 未來改進方向

### 短期 (1-2 週)
- [ ] 自動從 zh-TW.json 生成 TypeScript 類型
- [ ] Pre-commit hook 自動檢查一致性
- [ ] CI/CD 整合（PR 時自動檢查）

### 中期 (1-2 月)
- [ ] 翻譯進度儀表板
- [ ] 自動偵測程式碼中使用但未定義的 key
- [ ] 自動偵測已定義但未使用的 key

### 長期 (3+ 月)
- [ ] 整合翻譯管理平台（Lokalise/Tolgee）
- [ ] 支援翻譯外包/協作
- [ ] A/B 測試不同翻譯版本

---

## 📚 相關文件

- [I18N_COMPLETION_SUMMARY.md](./I18N_COMPLETION_SUMMARY.md) - 翻譯完成度總結
- [SIMPLIFIED_I18N_APPROACH.md](./SIMPLIFIED_I18N_APPROACH.md) - 簡化方案建議
- [BETTER_I18N_WORKFLOW.md](./BETTER_I18N_WORKFLOW.md) - 工作流程改進方案

---

**維護者**: Claude Code
**專案**: OderWhat
**最後更新**: 2025-12-10
