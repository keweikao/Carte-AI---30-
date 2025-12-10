# OderWhat 國際化 (i18n) 實作狀態報告

**檢查日期**: 2025-12-10
**檢查者**: Claude Code
**專案**: OderWhat Dining AI

---

## 📊 總體狀態概覽

### ✅ 已完成國際化的頁面 (3/10)

| 頁面 | 狀態 | 翻譯檔案 | 組件使用 |
|------|------|---------|---------|
| **Input Page** (輸入頁面) | ✅ 完成 | `InputPage.*` | `useTranslations('InputPage')` |
| **Recommendation Page** (推薦頁面) | ✅ 完成 | `RecommendationPage.*` | `useTranslations('RecommendationPage')` |
| **Menu Page** (菜單頁面) | ✅ 完成 | `MenuPage.*` | `useTranslations('MenuPage')` |

### ❌ 尚未完成國際化的頁面 (7/10)

| 頁面 | 狀態 | 硬編碼文字位置 | 翻譯檔案準備 |
|------|------|--------------|------------|
| **Home Page** (首頁) | ❌ 未完成 | `page.tsx:72-84` | ✅ 已有 `LandingPage.*` |
| **Waiting Page** (等待頁面) | ❌ 未完成 | 待檢查 | ⚠️ 需檢查 |
| **Final Menu Page** | ❌ 未完成 | 待檢查 | ⚠️ 需檢查 |
| **Onboarding Page** | ❌ 未完成 | 待檢查 | ⚠️ 需檢查 |
| **Error Page** | ❌ 未完成 | `error.tsx` | ⚠️ 需新增 |
| **Not Found Page** | ❌ 未完成 | `not-found.tsx` | ⚠️ 需新增 |
| **Header Component** | ❌ 未完成 | `carte/header.tsx:36-39,83,119` | ⚠️ 需新增 |

---

## 🔍 詳細發現

### 1. 首頁 (Home Page) - `app/[locale]/page.tsx`

**問題**:
- 已有翻譯檔案 (`LandingPage` section in `en.json` 和 `zh-TW.json`)
- **但組件中未使用 `useTranslations`**

**硬編碼文字示例**:
```tsx
// Line 72-74
讓 AI 為你策劃
完美的用餐體驗

// Line 84
不再為點餐煩惱。告訴我們你的喜好與情境...
```

**需要修改**:
```tsx
import { useTranslations } from 'next-intl';

const t = useTranslations('LandingPage');

// 使用
{t('landing_title')}
{t('landing_subtitle')}
```

---

### 2. Header Component - `components/carte/header.tsx`

**問題**: 導航選單和按鈕文字全部硬編碼

**硬編碼文字**:
```tsx
// Line 36-39
const navLinks = [
    { href: "#features", label: "功能介紹" },
    { href: "#how-it-works", label: "使用方式" },
    { href: "#about", label: "關於我們" },
];

// Line 83, 119
開始探索
```

**建議**: 新增 `Header` 或 `Common` section 到翻譯檔案

---

### 3. 語言切換功能

**狀態**: ❌ **不存在**

**發現**:
- 沒有找到語言切換器組件
- Header 中沒有語言選擇按鈕
- 無法在 UI 中切換語言

**URL 路由支援**:
- ✅ 專案使用 `[locale]` 動態路由
- ✅ 可以通過 URL 切換: `/zh/...` vs `/en/...`
- ❌ 但無 UI 控制元件

---

## 📝 翻譯檔案狀態

### 已存在的翻譯 sections:

#### `en.json` & `zh-TW.json`
- ✅ `HomePage`
- ✅ `InputPage` (已使用)
- ✅ `LoadingPage`
- ✅ `RecommendationPage` (已使用)
- ✅ `MenuPage` (已使用)
- ✅ `LandingPage` (未使用)

### 缺少的翻譯 sections:
- ❌ `Header` / `Navigation`
- ❌ `WaitingPage`
- ❌ `FinalMenuPage`
- ❌ `OnboardingPage`
- ❌ `ErrorPage`
- ❌ `NotFoundPage`
- ❌ `Common` (共用文字，如按鈕、標籤等)

---

## 🎯 優先修復清單

### 高優先級 (Critical) - 影響用戶體驗

1. **新增語言切換器** ⭐⭐⭐
   - 在 Header 中新增語言切換按鈕 (中/EN)
   - 使用 next-intl 的 `useRouter` 和 `usePathname` 切換 locale

2. **修復首頁國際化** ⭐⭐⭐
   - 檔案: `app/[locale]/page.tsx`
   - 翻譯已存在，只需導入並使用

3. **修復 Header 國際化** ⭐⭐⭐
   - 檔案: `components/carte/header.tsx`
   - 需新增翻譯檔案

### 中優先級 (Important) - 完整性

4. **Waiting Page 國際化**
   - 檢查並新增翻譯

5. **Onboarding Page 國際化**
   - 檢查並新增翻譯

6. **Final Menu Page 國際化**
   - 檢查並新增翻譯

### 低優先級 (Nice to have)

7. **Error 與 404 頁面國際化**
8. **新增 Common section**
   - 共用文字: "確認", "取消", "儲存", "載入中" 等

---

## 📋 Git 狀態中的修改

根據 git status，以下檔案有未提交的國際化修改：

```
M frontend/messages/en.json
M frontend/messages/zh-TW.json
M frontend/src/app/[locale]/input/page.tsx
```

這些是 **Input Page 的國際化更新**，應該提交。

---

## 🚀 建議實作步驟

### Step 1: 提交現有修改
```bash
git add frontend/messages/en.json frontend/messages/zh-TW.json
git add frontend/src/app/[locale]/input/page.tsx
git commit -m "feat: 完成 Input Page 國際化支援"
```

### Step 2: 建立語言切換器組件

創建 `frontend/src/components/language-switcher.tsx`:

```tsx
"use client";

import { useLocale } from 'next-intl';
import { useRouter, usePathname } from 'next/navigation';
import { Globe } from 'lucide-react';

export function LanguageSwitcher() {
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();

  const switchLanguage = (newLocale: string) => {
    // Remove current locale from pathname
    const pathWithoutLocale = pathname.replace(/^\/(zh|en)/, '');
    // Navigate to new locale
    router.push(`/${newLocale}${pathWithoutLocale}`);
  };

  return (
    <div className="flex items-center gap-2">
      <Globe className="w-4 h-4 text-charcoal" />
      <button
        onClick={() => switchLanguage(locale === 'zh' ? 'en' : 'zh')}
        className="text-sm font-medium text-charcoal hover:text-caramel"
      >
        {locale === 'zh' ? 'EN' : '中文'}
      </button>
    </div>
  );
}
```

### Step 3: 更新 Header 使用語言切換器

在 `components/carte/header.tsx` 中整合。

### Step 4: 修復首頁國際化

在 `app/[locale]/page.tsx` 中使用 `useTranslations('LandingPage')`。

### Step 5: 完成其他頁面國際化

逐一檢查並修復 waiting, onboarding, final-menu 等頁面。

---

## 📌 重要注意事項

### Next-intl 配置確認

需確認以下配置檔案正確:
- ✅ `i18n.ts` 或 `i18n/request.ts`
- ✅ `next.config.js` 中的 i18n 設定
- ✅ `middleware.ts` 處理 locale routing

### 測試清單

完成修復後需測試:
- [ ] 所有頁面中文顯示正確
- [ ] 所有頁面英文顯示正確
- [ ] 語言切換器正常運作
- [ ] 切換語言後 URL 正確更新
- [ ] 切換語言後頁面內容即時更新
- [ ] 不同頁面間導航保持選擇的語言

---

## 📊 進度追蹤

**整體完成度**: 30% (3/10 頁面)

```
國際化完成度: ████████░░░░░░░░░░░░░░░░░░░░░░ 30%

✅ Input Page       [████████████████████] 100%
✅ Recommendation   [████████████████████] 100%
✅ Menu Page        [████████████████████] 100%
⚠️  Home Page       [████████████░░░░░░░░]  60% (翻譯檔案已有)
❌ Header           [░░░░░░░░░░░░░░░░░░░░]   0%
❌ Language Switch  [░░░░░░░░░░░░░░░░░░░░]   0%
❌ Waiting Page     [░░░░░░░░░░░░░░░░░░░░]   0%
❌ Onboarding       [░░░░░░░░░░░░░░░░░░░░]   0%
❌ Final Menu       [░░░░░░░░░░░░░░░░░░░░]   0%
❌ Error Pages      [░░░░░░░░░░░░░░░░░░░░]   0%
```

---

## 🎯 結論與建議

### 現況總結

✅ **優點**:
- Input、Recommendation、Menu 三個核心頁面已完成國際化
- 翻譯檔案結構清晰，使用 next-intl 標準格式
- 已有部分翻譯內容準備好但未使用（如 LandingPage）

❌ **缺點**:
- **最大問題**: 沒有語言切換器，用戶無法切換語言
- 首頁等重要頁面未完成國際化
- Header 導航未國際化

### 建議行動

**立即行動** (1-2 小時):
1. 新增語言切換器組件並整合到 Header
2. 修復首頁國際化（翻譯已存在，快速完成）
3. 測試語言切換功能

**短期目標** (1-2 天):
4. 完成 Header 導航國際化
5. 完成 Waiting、Onboarding、Final Menu 頁面

**長期目標**:
6. 建立 Common 翻譯 section
7. 完善 Error 和 404 頁面國際化
8. 建立國際化測試流程

---

**報告完成日期**: 2025-12-10
**下次檢查建議**: 完成語言切換器後
