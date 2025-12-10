# 簡化的國際化方案

## 🎯 問題分析

當前問題：
1. 需要為每個頁面手動添加翻譯
2. 英文和中文要完全同步維護
3. 未來添加新語言會更複雜
4. 硬編碼文字散落各處

## 💡 簡化方案：Fallback + 部分翻譯

### 核心概念

**不需要翻譯所有內容**，只需要：
1. **中文作為主要語言** (完整內容)
2. **英文只翻譯關鍵介面文字**
3. **自動 fallback 機制** - 沒有翻譯時顯示中文

### 實作步驟

#### Step 1: 簡化 i18n 配置 (啟用 fallback)

更新 `frontend/src/i18n.ts`:

```typescript
import { getRequestConfig } from 'next-intl/server';
import { notFound } from 'next/navigation';

// 支援的語言
export const locales = ['zh', 'en'] as const;
export const defaultLocale = 'zh' as const;

export default getRequestConfig(async ({ locale }) => {
    // 驗證 locale
    if (!locales.includes(locale as any)) {
        notFound();
    }

    const messages = (await import(`../messages/${locale}.json`)).default;

    // 如果是英文，載入中文作為 fallback
    const fallbackMessages = locale !== 'zh'
        ? (await import(`../messages/zh.json`)).default
        : {};

    return {
        locale,
        messages: {
            ...fallbackMessages,  // 中文作為底層
            ...messages           // 英文覆蓋
        },
        // 啟用 fallback
        getMessageFallback({ namespace, key }) {
            return `${namespace}.${key}`;
        }
    };
});
```

#### Step 2: 簡化翻譯檔案結構

**中文 (`messages/zh.json`)** - 完整內容：
```json
{
  "Common": {
    "loading": "載入中...",
    "error": "發生錯誤",
    "back": "返回",
    "next": "下一步",
    "confirm": "確認",
    "cancel": "取消"
  },
  "HomePage": {
    "title": "讓 AI 為你策劃完美的用餐體驗",
    "subtitle": "不再為點餐煩惱...",
    "features": {
      "smart": "智慧推薦",
      "context": "情境感知",
      "fast": "節省時間"
    }
  }
}
```

**英文 (`messages/en.json`)** - 只翻譯必要內容：
```json
{
  "Common": {
    "loading": "Loading...",
    "back": "Back",
    "next": "Next"
  },
  "HomePage": {
    "title": "Let AI Plan Your Perfect Dining Experience"
  }
}
```

**未翻譯的內容會自動顯示中文** ✨

#### Step 3: 使用統一的組件模式

創建 `components/ui/text.tsx`:

```typescript
"use client";

import { useTranslations } from 'next-intl';

interface TextProps {
  ns: string;  // namespace
  k: string;   // key
  defaultText?: string;
  className?: string;
}

export function T({ ns, k, defaultText, className }: TextProps) {
  const t = useTranslations(ns);

  return (
    <span className={className}>
      {t(k, defaultText)}
    </span>
  );
}
```

使用範例：
```tsx
// 舊方式：硬編碼
<h1>讓 AI 為你策劃完美的用餐體驗</h1>

// 新方式：使用組件
<h1><T ns="HomePage" k="title" /></h1>

// 或更簡單的方式：
const t = useTranslations('HomePage');
<h1>{t('title')}</h1>
```

#### Step 4: 極簡方案 - 只翻譯按鈕和標籤

**最簡單的做法：只維護一個小的共用翻譯檔**

`messages/zh.json`:
```json
{
  "ui": {
    "submit": "提交",
    "back": "返回",
    "next": "下一步",
    "loading": "載入中",
    "error": "錯誤"
  }
}
```

`messages/en.json`:
```json
{
  "ui": {
    "submit": "Submit",
    "back": "Back",
    "next": "Next",
    "loading": "Loading",
    "error": "Error"
  }
}
```

**其他內容保持原樣，不使用翻譯**。

---

## 🚀 推薦方案：混合策略

### 策略 A: 最小化翻譯 (推薦)

**適用於**: 主要用戶是中文使用者，英文只是輔助

**做法**:
1. **介面元素**使用翻譯 (按鈕、標籤、錯誤訊息)
2. **內容文字**保持中文 (說明文字、標題等)
3. 英文用戶看到：英文按鈕 + 中文內容

**優點**:
- ✅ 維護成本極低
- ✅ 新增語言只需翻譯 UI 元素
- ✅ 不會出現翻譯不同步問題

**範例**:
```tsx
export default function InputPage() {
  const t = useTranslations('ui');

  return (
    <div>
      <h1>怎麼吃？</h1>  {/* 保持中文 */}
      <p>選擇您的用餐形式</p>  {/* 保持中文 */}

      <button>{t('next')}</button>  {/* 翻譯：下一步 / Next */}
      <button>{t('back')}</button>  {/* 翻譯：返回 / Back */}
    </div>
  );
}
```

### 策略 B: 關鍵頁面翻譯

**適用於**: 需要完整雙語支援，但不想維護所有頁面

**做法**:
1. **首頁、Landing Page** - 完整翻譯
2. **應用內頁面** - 只翻譯 UI 元素
3. 使用 fallback 自動處理未翻譯內容

**優點**:
- ✅ 對外頁面專業
- ✅ 內部頁面簡化維護
- ✅ 平衡翻譯成本和效果

### 策略 C: 動態語言檔案

**適用於**: 未來可能支援多語言

**做法**:
使用語言檔案分割 + 動態載入

```
messages/
  ├── zh/
  │   ├── common.json
  │   ├── home.json
  │   └── input.json
  ├── en/
  │   ├── common.json
  │   └── home.json  (其他 fallback 到中文)
  └── ja/
      └── common.json  (只翻譯常用詞)
```

更新 `i18n.ts`:
```typescript
export default getRequestConfig(async ({ locale }) => {
    // 動態載入語言檔案
    const messages = {};
    const files = ['common', 'home', 'input'];

    for (const file of files) {
        try {
            const content = await import(`../messages/${locale}/${file}.json`);
            Object.assign(messages, content.default);
        } catch {
            // Fallback 到中文
            const fallback = await import(`../messages/zh/${file}.json`);
            Object.assign(messages, fallback.default);
        }
    }

    return { locale, messages };
});
```

---

## 📋 具體實施建議

### 立即行動 (1 小時)

1. **簡化現有翻譯檔案**

保留 `zh.json`:
```json
{
  "ui": {
    "submit": "提交",
    "back": "返回",
    "next": "下一步",
    "prev": "上一步",
    "loading": "載入中",
    "error": "發生錯誤",
    "confirm": "確認",
    "cancel": "取消",
    "close": "關閉",
    "save": "儲存"
  },
  "HomePage": {
    "title": "讓 AI 為你策劃完美的用餐體驗",
    "cta": "開始探索"
  }
}
```

簡化 `en.json` - 只翻譯 UI:
```json
{
  "ui": {
    "submit": "Submit",
    "back": "Back",
    "next": "Next",
    "prev": "Previous",
    "loading": "Loading",
    "error": "Error",
    "confirm": "Confirm",
    "cancel": "Cancel",
    "close": "Close",
    "save": "Save"
  },
  "HomePage": {
    "title": "Let AI Plan Your Perfect Dining Experience",
    "cta": "Get Started"
  }
}
```

2. **統一按鈕使用方式**

創建 `components/ui/button.tsx`:
```typescript
import { useTranslations } from 'next-intl';

type ButtonType = 'submit' | 'back' | 'next' | 'prev' | 'cancel' | 'confirm';

export function Button({ type, onClick }: { type: ButtonType, onClick?: () => void }) {
  const t = useTranslations('ui');

  return (
    <button onClick={onClick}>
      {t(type)}
    </button>
  );
}
```

使用：
```tsx
<Button type="next" onClick={handleNext} />
<Button type="back" onClick={handleBack} />
```

3. **移除不必要的完整翻譯**

把大段描述文字改回硬編碼，只翻譯關鍵字：
```tsx
// ❌ 舊方式 - 維護困難
<p>{t('feature1_desc')}</p>

// ✅ 新方式 - 只翻譯標題
<h3>{t('features.smart')}</h3>
<p>AI 分析數千則評論與菜單資訊，找出最適合你的選擇</p>
```

---

## 🎯 最終建議

### 方案選擇矩陣

| 方案 | 維護成本 | 國際化程度 | 擴展性 | 推薦場景 |
|-----|---------|-----------|--------|---------|
| **方案 A: 最小化翻譯** | ⭐ 極低 | ⭐⭐ 基本 | ⭐⭐⭐ 高 | 🏆 主要中文用戶 |
| **方案 B: 關鍵頁面** | ⭐⭐ 低 | ⭐⭐⭐ 中 | ⭐⭐⭐ 高 | 🏆 對外需要專業形象 |
| **方案 C: 完整翻譯** | ⭐⭐⭐ 高 | ⭐⭐⭐⭐ 高 | ⭐⭐ 中 | 國際化產品 |

**我推薦：方案 A (最小化翻譯)**

理由：
1. ✅ 你的主要用戶是台灣/中文使用者
2. ✅ 維護成本極低，未來加日文/韓文也容易
3. ✅ 按鈕和介面元素英文化就能讓英文用戶基本使用
4. ✅ 不會出現中英文翻譯不同步的問題

### 實施步驟

```bash
# 1. 簡化翻譯檔案 (30 分鐘)
- 保留 ui 共用元素
- 保留首頁關鍵文字
- 刪除其他完整翻譯

# 2. 更新組件使用統一按鈕 (30 分鐘)
- 創建 Button 組件
- 替換現有按鈕

# 3. 測試 (30 分鐘)
- 測試中文介面
- 測試英文介面 (英文按鈕 + 中文內容)
```

要我幫你實施這個簡化方案嗎？
