# 更簡單的國際化開發工作流程

## 🎯 目標

- ✅ **全頁面完整翻譯** (保持)
- ✅ **架構簡單易管理** (改進)
- ✅ **容易擴展新語言** (改進)
- ✅ **開發體驗友好** (改進)

---

## 💡 核心改進方案

### 問題診斷

**當前痛點**：
1. 翻譯 keys 散落在各個頁面 (`HomePage.title`, `InputPage.step1_title`)
2. 新增語言要複製貼上整個檔案結構
3. 很難確保所有語言的 keys 一致
4. 翻譯檔案越來越大，難以維護

### 解決方案：型別安全 + 自動化工具

---

## 🚀 方案 1: TypeScript 型別定義（推薦）

### 概念

使用 TypeScript 定義翻譯結構，讓 IDE 自動提示，避免手動維護。

### 實作步驟

#### 1. 創建翻譯型別定義

`frontend/src/types/i18n.ts`:

```typescript
/**
 * 翻譯結構定義
 * 只需在這裡維護一次，所有語言自動同步
 */
export type Messages = {
  Common: {
    loading: string;
    error: string;
    submit: string;
    cancel: string;
    back: string;
    next: string;
    confirm: string;
  };

  HomePage: {
    title: string;
    subtitle: string;
    cta_button: string;
    features: {
      smart_title: string;
      smart_desc: string;
      context_title: string;
      context_desc: string;
      fast_title: string;
      fast_desc: string;
    };
  };

  InputPage: {
    step1: {
      title: string;
      subtitle: string;
      placeholder: string;
    };
    step2: {
      title: string;
      subtitle: string;
      mode_sharing: string;
      mode_sharing_desc: string;
      mode_individual: string;
      mode_individual_desc: string;
    };
  };

  // ... 其他頁面
};
```

#### 2. 更新 i18n 配置

`frontend/src/i18n.ts`:

```typescript
import { getRequestConfig } from 'next-intl/server';
import type { Messages } from './types/i18n';

export default getRequestConfig(async ({ locale }) => {
    const messages: Messages = (await import(`../messages/${locale}.json`)).default;

    return {
        locale,
        messages
    };
});
```

#### 3. 使用 - 享受 TypeScript 自動補全

```typescript
"use client";

import { useTranslations } from 'next-intl';

export default function HomePage() {
    const t = useTranslations('HomePage');

    return (
        <div>
            {/* IDE 會自動提示所有可用的 keys */}
            <h1>{t('title')}</h1>
            <p>{t('subtitle')}</p>

            {/* 巢狀結構也能自動補全 */}
            <h2>{t('features.smart_title')}</h2>
            <p>{t('features.smart_desc')}</p>
        </div>
    );
}
```

### 優點

- ✅ **IDE 自動補全** - 寫 `t('` 就會列出所有可用 keys
- ✅ **型別檢查** - 拼錯會立即報錯
- ✅ **重構友好** - 改變 key 名稱，所有使用處都會報錯
- ✅ **新語言簡單** - 只需複製 JSON 並翻譯，結構自動同步

---

## 🚀 方案 2: 自動化腳本管理

### 創建管理工具

`scripts/i18n-tools.js`:

```javascript
#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const MESSAGES_DIR = path.join(__dirname, '../frontend/messages');
const LOCALES = ['zh-TW', 'en', 'ja', 'ko']; // 支援的語言
const BASE_LOCALE = 'zh-TW';

/**
 * 檢查所有語言的 keys 是否一致
 */
function checkConsistency() {
    console.log('🔍 檢查翻譯一致性...\n');

    const baseMessages = JSON.parse(
        fs.readFileSync(path.join(MESSAGES_DIR, `${BASE_LOCALE}.json`), 'utf-8')
    );

    const baseKeys = getAllKeys(baseMessages);
    let hasErrors = false;

    LOCALES.forEach(locale => {
        if (locale === BASE_LOCALE) return;

        const filePath = path.join(MESSAGES_DIR, `${locale}.json`);
        if (!fs.existsSync(filePath)) {
            console.log(`⚠️  ${locale}.json 不存在\n`);
            return;
        }

        const messages = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
        const keys = getAllKeys(messages);

        // 檢查缺少的 keys
        const missing = baseKeys.filter(k => !keys.includes(k));
        const extra = keys.filter(k => !baseKeys.includes(k));

        if (missing.length > 0) {
            console.log(`❌ ${locale} 缺少以下 keys:`);
            missing.forEach(k => console.log(`   - ${k}`));
            console.log('');
            hasErrors = true;
        }

        if (extra.length > 0) {
            console.log(`⚠️  ${locale} 有多餘的 keys:`);
            extra.forEach(k => console.log(`   - ${k}`));
            console.log('');
        }

        if (missing.length === 0 && extra.length === 0) {
            console.log(`✅ ${locale} 完整`);
        }
    });

    if (!hasErrors) {
        console.log('\n✨ 所有翻譯檔案結構一致！');
    }
}

/**
 * 初始化新語言
 */
function initLocale(locale) {
    console.log(`🌍 初始化新語言: ${locale}\n`);

    const baseFile = path.join(MESSAGES_DIR, `${BASE_LOCALE}.json`);
    const newFile = path.join(MESSAGES_DIR, `${locale}.json`);

    if (fs.existsSync(newFile)) {
        console.log(`❌ ${locale}.json 已存在`);
        return;
    }

    const baseMessages = JSON.parse(fs.readFileSync(baseFile, 'utf-8'));
    const newMessages = createPlaceholders(baseMessages, locale);

    fs.writeFileSync(newFile, JSON.stringify(newMessages, null, 2), 'utf-8');
    console.log(`✅ 已創建 ${locale}.json`);
    console.log(`   請翻譯檔案中的內容`);
}

/**
 * 同步結構（添加缺少的 keys）
 */
function syncStructure(locale) {
    console.log(`🔄 同步 ${locale} 的結構...\n`);

    const baseMessages = JSON.parse(
        fs.readFileSync(path.join(MESSAGES_DIR, `${BASE_LOCALE}.json`), 'utf-8')
    );

    const filePath = path.join(MESSAGES_DIR, `${locale}.json`);
    const messages = fs.existsSync(filePath)
        ? JSON.parse(fs.readFileSync(filePath, 'utf-8'))
        : {};

    const synced = syncObjects(baseMessages, messages, locale);

    fs.writeFileSync(filePath, JSON.stringify(synced, null, 2), 'utf-8');
    console.log(`✅ 已同步 ${locale}.json`);
}

/**
 * 輔助函數：取得所有 keys（扁平化）
 */
function getAllKeys(obj, prefix = '') {
    let keys = [];

    Object.keys(obj).forEach(key => {
        const fullKey = prefix ? `${prefix}.${key}` : key;

        if (typeof obj[key] === 'object' && obj[key] !== null) {
            keys = keys.concat(getAllKeys(obj[key], fullKey));
        } else {
            keys.push(fullKey);
        }
    });

    return keys;
}

/**
 * 創建帶有 TODO 標記的佔位符
 */
function createPlaceholders(obj, locale) {
    const result = {};

    Object.keys(obj).forEach(key => {
        if (typeof obj[key] === 'object' && obj[key] !== null) {
            result[key] = createPlaceholders(obj[key], locale);
        } else {
            result[key] = `[TODO:${locale}] ${obj[key]}`;
        }
    });

    return result;
}

/**
 * 同步物件結構
 */
function syncObjects(base, target, locale) {
    const result = { ...target };

    Object.keys(base).forEach(key => {
        if (typeof base[key] === 'object' && base[key] !== null) {
            result[key] = syncObjects(
                base[key],
                target[key] || {},
                locale
            );
        } else if (!(key in target)) {
            // 新增缺少的 key
            result[key] = `[TODO:${locale}] ${base[key]}`;
            console.log(`   + 新增: ${key}`);
        }
    });

    return result;
}

// CLI
const command = process.argv[2];
const arg = process.argv[3];

switch (command) {
    case 'check':
        checkConsistency();
        break;

    case 'init':
        if (!arg) {
            console.log('❌ 請指定語言代碼，例如: npm run i18n:init ja');
            break;
        }
        initLocale(arg);
        break;

    case 'sync':
        if (!arg) {
            console.log('同步所有語言...');
            LOCALES.forEach(locale => {
                if (locale !== BASE_LOCALE) {
                    syncStructure(locale);
                }
            });
        } else {
            syncStructure(arg);
        }
        break;

    default:
        console.log(`
i18n 管理工具

指令:
  npm run i18n:check        - 檢查所有語言的一致性
  npm run i18n:init <locale> - 初始化新語言
  npm run i18n:sync [locale] - 同步結構（添加缺少的 keys）

範例:
  npm run i18n:check
  npm run i18n:init ja
  npm run i18n:sync en
        `);
}
```

### 添加 npm scripts

`frontend/package.json`:

```json
{
  "scripts": {
    "i18n:check": "node ../scripts/i18n-tools.js check",
    "i18n:init": "node ../scripts/i18n-tools.js init",
    "i18n:sync": "node ../scripts/i18n-tools.js sync"
  }
}
```

### 使用方式

```bash
# 檢查所有翻譯是否一致
npm run i18n:check

# 初始化新語言（自動創建帶 TODO 標記的模板）
npm run i18n:init ja

# 同步結構（將新 keys 添加到現有語言）
npm run i18n:sync en

# 同步所有語言
npm run i18n:sync
```

---

## 🚀 方案 3: 扁平化結構（最簡單）

### 概念

不使用巢狀結構，使用扁平化 keys，更容易管理。

### 範例

**舊方式（巢狀）**:
```json
{
  "HomePage": {
    "features": {
      "smart": {
        "title": "智慧推薦",
        "description": "AI 分析..."
      }
    }
  }
}
```

**新方式（扁平）**:
```json
{
  "home_title": "首頁標題",
  "home_feature_smart_title": "智慧推薦",
  "home_feature_smart_desc": "AI 分析...",
  "input_step1_title": "選擇餐廳",
  "input_step2_title": "設定人數"
}
```

### 使用

```typescript
const t = useTranslations();

// 直接使用，不需要指定 namespace
<h1>{t('home_title')}</h1>
<p>{t('home_feature_smart_desc')}</p>
```

### 優點

- ✅ 結構超級簡單
- ✅ 容易比對不同語言
- ✅ 使用 spreadsheet 管理翻譯
- ✅ 容易導入/導出 CSV

---

## 🚀 方案 4: 使用翻譯管理平台

### 推薦工具

1. **Lokalise** (https://lokalise.com)
2. **Phrase** (https://phrase.com)
3. **Crowdin** (https://crowdin.com)
4. **Tolgee** (開源，self-hosted)

### 工作流程

```
1. 開發者在程式碼中使用翻譯 keys
   ↓
2. 自動上傳到翻譯平台
   ↓
3. 翻譯人員在平台上翻譯
   ↓
4. 自動下載最新翻譯
   ↓
5. CI/CD 自動部署
```

### 整合範例（Tolgee - 開源）

```typescript
// 1. 安裝
npm install @tolgee/react

// 2. 設定
import { TolgeeProvider } from '@tolgee/react';

export default function App({ children }) {
  return (
    <TolgeeProvider
      apiUrl="https://app.tolgee.io"
      apiKey={process.env.TOLGEE_API_KEY}
    >
      {children}
    </TolgeeProvider>
  );
}

// 3. 使用（和 next-intl 類似）
import { useTranslate } from '@tolgee/react';

const { t } = useTranslate();
<h1>{t('home_title')}</h1>
```

**優點**:
- ✅ 視覺化翻譯介面
- ✅ 可以直接在網頁上點擊翻譯（in-context editing）
- ✅ 自動檢測缺少的翻譯
- ✅ 協作友好（多人翻譯）

---

## 📊 方案比較

| 方案 | 開發體驗 | 維護成本 | 擴展性 | 協作友好 | 推薦度 |
|-----|---------|---------|--------|---------|-------|
| **TypeScript 型別** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 🏆 最推薦 |
| **自動化腳本** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 🏆 最推薦 |
| **扁平化結構** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ 推薦 |
| **翻譯平台** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ 進階 |

---

## 🎯 我的建議

### 組合方案：TypeScript + 自動化腳本

**理由**：
1. TypeScript 提供開發時的自動補全和型別檢查
2. 自動化腳本確保所有語言結構一致
3. 不依賴第三方服務
4. 免費且完全掌控

### 實施步驟

```bash
# 1. 創建型別定義（15 分鐘）
touch frontend/src/types/i18n.ts

# 2. 創建自動化腳本（30 分鐘）
touch scripts/i18n-tools.js
chmod +x scripts/i18n-tools.js

# 3. 更新現有翻譯檔案（30 分鐘）
npm run i18n:check  # 檢查一致性
npm run i18n:sync   # 同步結構

# 4. 未來新增語言（5 分鐘）
npm run i18n:init ja  # 初始化日文
# 翻譯 [TODO:ja] 標記的內容
npm run i18n:check    # 確認完整性
```

### 日常工作流程

```bash
# 開發新功能時
1. 在 zh-TW.json 添加新 keys
2. 執行 npm run i18n:sync 同步到其他語言
3. 翻譯 [TODO:xx] 標記的內容
4. 執行 npm run i18n:check 確認
5. Commit
```

---

## 📝 總結

**最佳實踐**：

✅ 使用 **TypeScript 型別定義** → IDE 自動補全
✅ 使用 **自動化腳本** → 結構自動同步
✅ 定期執行 **i18n:check** → 確保一致性
✅ 使用 **扁平化或淺層巢狀** → 容易維護

**避免**：

❌ 深層巢狀結構（超過 3 層）
❌ 手動複製貼上翻譯檔案
❌ 不檢查就直接上線

要我幫你實施這個組合方案嗎？
