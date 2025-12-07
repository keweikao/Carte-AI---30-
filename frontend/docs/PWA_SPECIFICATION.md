# PWA 開發規格書

## 專案資訊

- **功能名稱**: Progressive Web App (PWA) 支援
- **版本**: v1.0.0
- **開發日期**: 2025-12-03
- **負責團隊**: Frontend Team
- **優先級**: High
- **狀態**: ✅ 已完成

## 1. 需求背景

### 1.1 業務需求
使用者希望能夠將 Carte AI 安裝到桌面或手機主畫面，享受接近原生應用程式的體驗，包括：
- 快速啟動（從主畫面圖示直接開啟）
- 全螢幕體驗（無瀏覽器 UI）
- 離線基本功能
- 更快的載入速度（透過快取）

### 1.2 技術目標
1. 符合 PWA 標準規範
2. 支援主流瀏覽器和平台
3. 提供流暢的安裝體驗
4. 實現智慧快取策略
5. 保持良好的效能指標

### 1.3 成功指標
- Lighthouse PWA Score ≥ 90
- 安裝轉換率 > 5%
- 快取命中率 > 70%
- 首次載入時間 < 3s

## 2. 技術架構

### 2.1 核心元件

```
┌─────────────────────────────────────────┐
│           User Interface                │
│  ┌───────────────────────────────────┐  │
│  │      PWA Install Prompt UI        │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         Service Worker (sw.js)          │
│  ┌──────────┐  ┌──────────┐  ┌───────┐ │
│  │  Cache   │  │ Network  │  │ Fetch │ │
│  │ Strategy │  │ Strategy │  │ Event │ │
│  └──────────┘  └──────────┘  └───────┘ │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          Browser Cache API              │
│  ┌──────────────┐  ┌─────────────────┐ │
│  │  Static      │  │  Runtime Cache  │ │
│  │  Cache (v1)  │  │  (Runtime)      │ │
│  └──────────────┘  └─────────────────┘ │
└─────────────────────────────────────────┘
```

### 2.2 技術棧

| 技術 | 版本 | 用途 |
|------|------|------|
| Next.js | 14+ | 應用框架 |
| Service Worker API | - | 離線支援與快取 |
| Web App Manifest | - | PWA 配置 |
| Cache API | - | 資源快取 |
| React | 18+ | UI 元件 |

## 3. 功能規格

### 3.1 Web App Manifest

**檔案位置**: `public/manifest.json`

#### 3.1.1 基本資訊

```json
{
  "name": "Carte AI 點餐助手 - 智慧餐廳點餐",
  "short_name": "Carte AI",
  "description": "30秒快速決定吃什麼！AI 分析 Google 評論，推薦最適合您的菜色",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "orientation": "portrait-primary"
}
```

**規格說明**:
- `name`: 完整應用程式名稱（最多 45 字元）
- `short_name`: 短名稱，用於主畫面圖示下方（最多 12 字元）
- `description`: 應用程式描述
- `start_url`: 應用程式啟動 URL
- `scope`: 應用程式範圍
- `display`: 顯示模式（standalone = 全螢幕無瀏覽器 UI）
- `orientation`: 預設螢幕方向

#### 3.1.2 品牌色彩

```json
{
  "background_color": "#FAF7F2",
  "theme_color": "#2C3539"
}
```

**規格說明**:
- `background_color`: 啟動畫面背景色（Carte AI Cream 色）
- `theme_color`: 瀏覽器工具列顏色（Carte AI Charcoal 色）

#### 3.1.3 圖示配置

```json
{
  "icons": [
    {
      "src": "/logo-icon.svg",
      "sizes": "any",
      "type": "image/svg+xml",
      "purpose": "any"
    },
    {
      "src": "/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
```

**圖示規格**:

| 尺寸 | 格式 | Purpose | 用途 |
|------|------|---------|------|
| Any | SVG | any | 向量圖示，適用於所有尺寸 |
| 192x192 | PNG | any maskable | 標準圖示 + Android 適配 |
| 512x512 | PNG | any maskable | 高解析度圖示 + Android 適配 |

**Maskable 圖示設計要點**:
- Safe Zone: 中心 80% 區域放置主要內容
- 邊緣 20% 可能被裁切（Android Adaptive Icons）
- 使用品牌背景色填滿整個畫布

#### 3.1.4 其他配置

```json
{
  "lang": "zh-TW",
  "dir": "ltr",
  "categories": ["food", "lifestyle", "utilities"],
  "screenshots": [...],
  "shortcuts": [...],
  "prefer_related_applications": false
}
```

### 3.2 Service Worker

**檔案位置**: `public/sw.js`

#### 3.2.1 快取版本管理

```javascript
const CACHE_NAME = 'carte-ai-v1';
const RUNTIME_CACHE = 'carte-ai-runtime';
```

**版本命名規則**:
- `carte-ai-v{主版本號}`: 靜態資源快取
- `carte-ai-runtime`: 執行時期快取
- 主版本號更新時，舊版本快取會自動清除

#### 3.2.2 預快取資源清單

```javascript
const PRECACHE_ASSETS = [
  '/',
  '/manifest.json',
  '/logo-icon.svg',
  '/icon-192x192.png',
  '/icon-512x512.png',
];
```

**選擇原則**:
- 關鍵路徑資源（首頁、manifest）
- 品牌資產（logo、icons）
- 體積小、變動少的檔案

#### 3.2.3 快取策略

##### A. Static Assets - Cache First

**適用對象**:
- 圖片 (`request.destination === 'image'`)
- 字型 (`request.destination === 'font'`)
- 樣式表 (`request.destination === 'style'`)
- JavaScript (`request.destination === 'script'`)

**流程**:
```
Request → Check Cache → Cache Hit?
                         ↓ Yes: Return Cache
                         ↓ No: Fetch Network → Cache → Return
```

**優點**:
- 最快的載入速度
- 減少網路請求
- 支援離線瀏覽

**程式碼範例**:
```javascript
caches.match(request)
  .then((response) => {
    if (response) return response;
    return fetch(request).then((response) => {
      if (response.status === 200) {
        const responseClone = response.clone();
        caches.open(RUNTIME_CACHE).then((cache) => {
          cache.put(request, responseClone);
        });
      }
      return response;
    });
  });
```

##### B. HTML Pages - Network First

**適用對象**:
- HTML 頁面
- 動態內容頁面

**流程**:
```
Request → Fetch Network → Success?
                           ↓ Yes: Cache → Return
                           ↓ No: Check Cache → Return or Offline Page
```

**優點**:
- 優先獲取最新內容
- 網路失敗時有備援
- 保證內容即時性

**程式碼範例**:
```javascript
fetch(request)
  .then((response) => {
    if (response.status === 200) {
      const responseClone = response.clone();
      caches.open(RUNTIME_CACHE).then((cache) => {
        cache.put(request, responseClone);
      });
    }
    return response;
  })
  .catch(() => {
    return caches.match(request);
  });
```

##### C. API Requests - Network Only

**適用對象**:
- `/api/*` 路徑
- 動態數據請求

**流程**:
```
Request → Fetch Network → Return (不快取)
```

**優點**:
- 始終獲取最新數據
- 避免快取過期問題
- 簡化邏輯

**程式碼範例**:
```javascript
fetch(request, { timeout: 10000 })
  .catch(() => {
    return new Response(
      JSON.stringify({ error: 'Network unavailable' }),
      { status: 503, headers: { 'Content-Type': 'application/json' }}
    );
  });
```

#### 3.2.4 生命週期事件

##### Install Event
```javascript
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_ASSETS))
      .then(() => self.skipWaiting())
  );
});
```

**職責**:
1. 建立快取空間
2. 預快取關鍵資源
3. 立即啟用（skipWaiting）

##### Activate Event
```javascript
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE) {
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => self.clients.claim())
  );
});
```

**職責**:
1. 清理舊版本快取
2. 取得所有客戶端控制權（claim）

##### Fetch Event
```javascript
self.addEventListener('fetch', (event) => {
  // 實作快取策略（見 3.2.3）
});
```

**職責**:
- 攔截所有網路請求
- 根據資源類型應用快取策略

### 3.3 PWA Installer 元件

**檔案位置**: `src/components/pwa-installer.tsx`

#### 3.3.1 元件職責

1. **Service Worker 註冊**
   - 在 `window.load` 事件後註冊
   - 定期檢查更新（每 60 秒）
   - 處理註冊錯誤

2. **安裝提示管理**
   - 監聽 `beforeinstallprompt` 事件
   - 儲存安裝提示物件
   - 顯示自訂安裝 UI

3. **使用者互動**
   - 提供「安裝」按鈕
   - 提供「稍後」按鈕
   - 追蹤使用者選擇

#### 3.3.2 狀態管理

```typescript
const [deferredPrompt, setDeferredPrompt] = useState<any>(null);
const [isInstallable, setIsInstallable] = useState(false);
```

**狀態說明**:
- `deferredPrompt`: 儲存瀏覽器的安裝提示物件
- `isInstallable`: 控制安裝 UI 顯示/隱藏

#### 3.3.3 事件處理

##### beforeinstallprompt
```typescript
const handleBeforeInstallPrompt = (e: Event) => {
  e.preventDefault();
  setDeferredPrompt(e);
  setIsInstallable(true);
};
```

**時機**: 瀏覽器偵測到應用符合 PWA 條件
**行為**: 阻止預設提示，顯示自訂 UI

##### Install Click
```typescript
const handleInstallClick = async () => {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  const { outcome } = await deferredPrompt.userChoice;
  if (outcome === 'accepted') {
    setDeferredPrompt(null);
    setIsInstallable(false);
  }
};
```

**流程**:
1. 檢查 deferredPrompt 是否存在
2. 呼叫 `prompt()` 顯示瀏覽器安裝對話框
3. 等待使用者選擇
4. 根據結果更新 UI 狀態

##### appinstalled
```typescript
window.addEventListener('appinstalled', () => {
  setDeferredPrompt(null);
  setIsInstallable(false);
});
```

**時機**: 應用程式成功安裝後
**行為**: 隱藏安裝 UI

#### 3.3.4 UI 規格

**位置**: 固定在右下角 (`fixed bottom-4 right-4`)

**結構**:
```
┌─────────────────────────────────┐
│  [Icon]  安裝 Carte AI          │
│          將應用程式新增至主畫面，│
│          享受更快速的體驗        │
│          [安裝] [稍後]          │
└─────────────────────────────────┐
```

**視覺設計**:
- 白色背景 (`bg-white`)
- 深色邊框 (`border-2 border-charcoal`)
- 陰影效果 (`shadow-lg`)
- 圓角 (`rounded-lg`)
- 滑入動畫 (`animate-in slide-in-from-bottom`)

**按鈕樣式**:
- 安裝按鈕: `bg-sage-600 text-white` (主要 CTA)
- 稍後按鈕: `bg-cream-200 text-charcoal` (次要)

### 3.4 Meta Tags

**檔案位置**: `src/app/[locale]/layout.tsx`

#### 3.4.1 必要 Meta Tags

```html
<!-- PWA 基本資訊 -->
<meta name="application-name" content="Carte AI 點餐助手" />
<meta name="theme-color" content="#2C3539" />

<!-- Apple Mobile Web App -->
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="default" />
<meta name="apple-mobile-web-app-title" content="Carte AI" />

<!-- 通用 Mobile Web App -->
<meta name="mobile-web-app-capable" content="yes" />
```

#### 3.4.2 Apple Touch Icons

```html
<link rel="apple-touch-icon" href="/icon-192x192.png" />
<link rel="apple-touch-icon" sizes="192x192" href="/icon-192x192.png" />
<link rel="apple-touch-icon" sizes="512x512" href="/icon-512x512.png" />
```

**規格說明**:
- iOS Safari 需要特定的 Apple Touch Icon
- 建議提供多種尺寸
- 圖示應為正方形 PNG 格式

## 4. 開發指南

### 4.1 開發環境設定

#### 4.1.1 本地測試 Service Worker

**注意事項**:
- Service Worker 只在 HTTPS 或 localhost 運作
- 開發時使用 `npm run dev` 會在 localhost
- 使用 Chrome DevTools 的 Application 標籤調試

**測試步驟**:
1. 啟動開發伺服器: `npm run dev`
2. 開啟 Chrome DevTools (F12)
3. 切換到 Application 標籤
4. 檢查 Service Workers 區塊
5. 檢查 Cache Storage

#### 4.1.2 手動觸發安裝提示

由於安裝提示有條件限制，可使用以下方法測試：

**Method 1: Chrome DevTools**
```
1. Application 標籤
2. Manifest 區塊
3. 點擊 "Add to home screen"
```

**Method 2: Chrome Flags**
```
chrome://flags/#bypass-app-banner-engagement-checks
啟用此 flag 可跳過安裝條件檢查
```

### 4.2 圖示生成流程

#### 4.2.1 自動生成腳本

```python
from PIL import Image

def generate_pwa_icons(source_path, output_dir):
    img = Image.open(source_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    sizes = [192, 512]
    for size in sizes:
        canvas = Image.new('RGBA', (size, size), (250, 247, 242, 255))
        img_copy = img.copy()
        img_copy.thumbnail((size - 40, size - 40), Image.Resampling.LANCZOS)

        x = (size - img_copy.width) // 2
        y = (size - img_copy.height) // 2
        canvas.paste(img_copy, (x, y), img_copy)

        output_path = f"{output_dir}/icon-{size}x{size}.png"
        canvas.save(output_path, 'PNG', optimize=True)
```

**參數說明**:
- `source_path`: 來源圖片路徑（建議 SVG 或高解析度 PNG）
- `output_dir`: 輸出目錄（通常是 `public/`）
- 背景色: `(250, 247, 242, 255)` = Carte AI Cream
- Padding: 每邊 20px

#### 4.2.2 手動檢查清單

圖示生成後，請檢查：
- [ ] 檔案大小 < 500KB
- [ ] 圖示清晰無模糊
- [ ] Safe Zone 內容可見
- [ ] 背景色正確
- [ ] 在深色/淺色背景都可辨識

### 4.3 測試指南

#### 4.3.1 PWA 功能測試

**Lighthouse 審核**:
```bash
# Chrome DevTools
1. F12 開啟 DevTools
2. Lighthouse 標籤
3. 勾選 "Progressive Web App"
4. 點擊 "Generate report"
```

**目標分數**:
- PWA Score: ≥ 90
- Performance: ≥ 85
- Accessibility: ≥ 90

**Lighthouse 檢查項目**:
- [x] Registers a service worker
- [x] Responds with 200 when offline
- [x] Contains valid manifest.json
- [x] Has a valid theme color
- [x] Has icons for add to home screen
- [x] Uses HTTPS

#### 4.3.2 跨瀏覽器測試

| 瀏覽器 | 版本 | 測試項目 |
|--------|------|----------|
| Chrome Desktop | Latest | 完整 PWA 功能 |
| Chrome Android | Latest | 安裝流程、離線功能 |
| Safari iOS | 14+ | Add to Home Screen |
| Safari macOS | Latest | 基本功能（有限 PWA 支援）|
| Edge | Latest | 完整 PWA 功能 |
| Firefox | Latest | Service Worker、Manifest |

**測試場景**:
1. **安裝流程**
   - [ ] 看到安裝提示
   - [ ] 點擊安裝成功
   - [ ] 圖示出現在桌面/主畫面
   - [ ] 應用程式名稱正確

2. **啟動體驗**
   - [ ] 從圖示啟動成功
   - [ ] 顯示啟動畫面（splash screen）
   - [ ] 進入全螢幕模式
   - [ ] 主題色正確應用

3. **快取功能**
   - [ ] 首次載入後資源被快取
   - [ ] 二次載入速度明顯提升
   - [ ] 離線時可顯示已快取頁面
   - [ ] API 請求失敗顯示適當錯誤

4. **更新機制**
   - [ ] Service Worker 更新被偵測
   - [ ] 提示使用者重新載入
   - [ ] 舊版本快取被清除

#### 4.3.3 效能測試

**快取命中率測量**:
```javascript
// 在 Service Worker 中
let cacheHits = 0;
let cacheMisses = 0;

self.addEventListener('fetch', (event) => {
  caches.match(event.request).then((response) => {
    if (response) {
      cacheHits++;
    } else {
      cacheMisses++;
    }
    console.log(`Cache Hit Rate: ${(cacheHits / (cacheHits + cacheMisses) * 100).toFixed(2)}%`);
  });
});
```

**目標指標**:
- 快取命中率: > 70%
- 首次內容繪製 (FCP): < 1.8s
- 最大內容繪製 (LCP): < 2.5s
- 累積版面配置偏移 (CLS): < 0.1

### 4.4 部署檢查清單

部署前請確認：

#### 4.4.1 檔案完整性
- [ ] `public/manifest.json` 存在且內容正確
- [ ] `public/sw.js` 存在且內容正確
- [ ] PWA 圖示檔案都已生成
- [ ] `pwa-installer.tsx` 元件已建立
- [ ] Layout 已整合 PWA 元件

#### 4.4.2 配置正確性
- [ ] Manifest 中的 URL 指向正確的生產環境
- [ ] `start_url` 指向首頁
- [ ] `scope` 涵蓋所有應用路徑
- [ ] 圖示路徑正確（相對於根目錄）

#### 4.4.3 HTTPS 要求
- [ ] 生產環境使用 HTTPS
- [ ] SSL 憑證有效
- [ ] 所有資源都透過 HTTPS 載入（無混合內容）

#### 4.4.4 快取策略驗證
- [ ] Static assets 使用 Cache First
- [ ] HTML pages 使用 Network First
- [ ] API requests 使用 Network Only
- [ ] 快取版本號已更新（如有重大變更）

#### 4.4.5 測試驗證
- [ ] Lighthouse PWA 分數 ≥ 90
- [ ] 在 Chrome/Safari/Edge 測試安裝流程
- [ ] 測試離線功能
- [ ] 測試快取更新機制

## 5. 維護與監控

### 5.1 Service Worker 版本管理

**更新策略**:
```javascript
// 主要更新時增加版本號
const CACHE_NAME = 'carte-ai-v2'; // v1 → v2

// 觸發條件:
// 1. 重大功能變更
// 2. 關鍵資源更新
// 3. 快取策略調整
```

**更新流程**:
1. 修改 `CACHE_NAME`
2. 更新 `PRECACHE_ASSETS` 清單（如需要）
3. 部署新版本
4. Service Worker 自動更新
5. 舊版本快取自動清除

### 5.2 監控指標

#### 5.2.1 安裝追蹤

**Google Analytics 事件**:
```javascript
// 安裝提示顯示
gtag('event', 'pwa_prompt_shown', {
  event_category: 'PWA',
  event_label: 'Install Prompt'
});

// 使用者點擊安裝
gtag('event', 'pwa_install_clicked', {
  event_category: 'PWA',
  event_label: 'Install Button'
});

// 安裝成功
gtag('event', 'pwa_installed', {
  event_category: 'PWA',
  event_label: 'Installation Success'
});
```

**關鍵指標**:
- 安裝提示顯示次數
- 安裝按鈕點擊率
- 實際安裝成功率
- 從主畫面啟動比例

#### 5.2.2 快取效能

**監控項目**:
```javascript
// Service Worker 快取統計
{
  cacheHitRate: 0.75,      // 快取命中率
  cacheSizeBytes: 2048000, // 快取大小
  cacheEntries: 45,        // 快取項目數
  swUpdateFrequency: 86400 // 更新頻率（秒）
}
```

**警示閾值**:
- 快取命中率 < 60%: 檢查快取策略
- 快取大小 > 50MB: 檢查是否快取過多資源
- Service Worker 錯誤率 > 1%: 檢查 SW 程式碼

### 5.3 常見問題處理

#### Q1: Service Worker 沒有註冊成功

**可能原因**:
1. 不在 HTTPS 環境
2. sw.js 路徑錯誤
3. 瀏覽器不支援

**解決方案**:
```javascript
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js')
    .then(reg => console.log('SW registered:', reg))
    .catch(err => console.error('SW registration failed:', err));
}
```

#### Q2: 安裝提示不出現

**可能原因**:
1. 不符合 PWA 條件（缺少 manifest 或 SW）
2. 使用者已安裝
3. 瀏覽器已拒絕過安裝提示

**解決方案**:
- 使用 Lighthouse 檢查 PWA 條件
- 檢查 Chrome DevTools Console 錯誤
- 清除瀏覽器快取和 Site Data

#### Q3: 更新的內容沒有顯示

**可能原因**:
1. Service Worker 使用舊版本快取
2. 快取版本號未更新
3. 使用者未重新啟動應用

**解決方案**:
```javascript
// 提示使用者更新
self.addEventListener('activate', (event) => {
  // 清除舊快取
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter(key => key !== CURRENT_CACHE)
          .map(key => caches.delete(key))
      );
    })
  );
});

// 通知客戶端更新
self.clients.claim();
```

## 6. 未來優化方向

### 6.1 短期優化（1-3 個月）

1. **離線頁面**
   - 建立專用的離線提示頁面
   - 顯示使用者最近瀏覽的餐廳
   - 提供離線可用的功能說明

2. **更新提示 UI**
   - 偵測 Service Worker 更新
   - 顯示「有新版本可用」提示
   - 提供「立即更新」按鈕

3. **安裝引導**
   - 首次訪問顯示 PWA 功能介紹
   - 提供安裝步驟教學
   - 追蹤使用者完成引導流程

### 6.2 中期優化（3-6 個月）

1. **Web Push Notifications**
   - 使用者訂閱推播通知
   - 推送餐廳優惠資訊
   - 推送個人化推薦

2. **Background Sync**
   - 離線時儲存使用者操作
   - 網路恢復時自動同步
   - 收藏、評論等功能支援

3. **App Shortcuts**
   - 新增應用程式捷徑
   - 快速搜尋餐廳
   - 快速查看收藏

### 6.3 長期優化（6-12 個月）

1. **Progressive Enhancement**
   - 偵測裝置能力
   - 提供漸進式功能
   - 在高階裝置啟用進階功能

2. **Advanced Caching**
   - 智慧預測使用者需求
   - 預先快取可能瀏覽的內容
   - 根據使用頻率調整快取策略

3. **Offline-First Architecture**
   - 重新設計為離線優先架構
   - 本地資料庫（IndexedDB）
   - 完整的離線功能支援

## 7. 參考資源

### 7.1 官方文件

- [Web.dev - PWA](https://web.dev/progressive-web-apps/)
- [MDN - Progressive web apps](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
- [Google - Service Worker API](https://developers.google.com/web/fundamentals/primers/service-workers)
- [W3C - Web App Manifest](https://www.w3.org/TR/appmanifest/)

### 7.2 工具與檢查器

- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [PWA Builder](https://www.pwabuilder.com/)
- [Workbox](https://developers.google.com/web/tools/workbox) - Service Worker 函式庫
- [Maskable.app](https://maskable.app/) - 圖示編輯器

### 7.3 最佳實踐

- [PWA Checklist](https://web.dev/pwa-checklist/)
- [Service Worker Best Practices](https://web.dev/service-worker-mindset/)
- [Offline UX Considerations](https://web.dev/offline-ux-considerations/)

---

**文件版本**: 1.0.0
**最後更新**: 2025-12-03
**維護者**: Frontend Team
