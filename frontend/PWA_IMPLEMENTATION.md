# PWA Implementation for Carte AI

## Overview
Carte AI 現已完整支援 Progressive Web App (PWA) 功能，讓使用者可以將應用程式安裝到桌面或手機主畫面，享受接近原生應用程式的體驗。

## 完成項目

### 1. Manifest.json 完整配置
**檔案位置**: `frontend/public/manifest.json`

**新增功能**:
- 完整的應用程式資訊（名稱、簡稱、描述）
- 正確的顯示模式（standalone）和方向設定（portrait-primary）
- 品牌色彩配置（背景色、主題色）
- 多尺寸 PWA 圖示支援（192x192, 512x512）
- 應用程式截圖展示
- 快捷方式（shortcuts）功能
- 語言和地區設定（zh-TW）

### 2. PWA 圖示生成
**新增檔案**:
- `frontend/public/icon-192x192.png` - 標準 PWA 圖示
- `frontend/public/icon-512x512.png` - 高解析度 PWA 圖示

**特色**:
- 從現有 logo 自動生成
- 符合 PWA 標準尺寸
- 支援 maskable 模式（Android 適配）
- 使用品牌色作為背景

### 3. Service Worker
**檔案位置**: `frontend/public/sw.js`

**功能**:
- **快取策略**:
  - Static Assets: Cache First（圖片、字型、樣式、腳本）
  - HTML Pages: Network First with Cache Fallback
  - API Requests: Network Only（不快取動態數據）

- **版本管理**: 自動清理舊版本快取
- **錯誤處理**: 網路不可用時提供友善的回應
- **效能優化**: 預快取關鍵資源

### 4. PWA Installer 元件
**檔案位置**: `frontend/src/components/pwa-installer.tsx`

**功能**:
- 自動偵測 PWA 安裝能力
- 顯示友善的安裝提示 UI
- 處理安裝事件（beforeinstallprompt, appinstalled）
- Service Worker 自動註冊與更新檢查
- 提供「安裝」和「稍後」選項

**UI 特色**:
- 固定在右下角的浮動卡片
- 品牌一致的設計風格
- 平滑的進入動畫
- 響應式設計

### 5. Layout 整合
**修改檔案**: `frontend/src/app/[locale]/layout.tsx`

**新增內容**:
- PWA meta tags（Apple Mobile Web App 支援）
- Apple Touch Icon 連結
- PWAInstaller 元件整合
- Manifest 連結（已存在，已確認）

## 使用指南

### 對使用者
1. 訪問 Carte AI 網站（https://www.carte.tw）
2. 瀏覽器會在右下角顯示安裝提示
3. 點擊「安裝」按鈕
4. 應用程式將被新增到桌面/主畫面
5. 點擊圖示即可以全螢幕模式啟動

### 測試安裝功能

#### Desktop (Chrome/Edge)
1. 開啟 DevTools (F12)
2. 切換到 Application 標籤
3. 檢查 Manifest 和 Service Worker 狀態
4. 使用 Lighthouse 執行 PWA 稽核

#### Mobile (Android)
1. 使用 Chrome 開啟網站
2. 點擊右上角選單
3. 選擇「安裝應用程式」或「新增至主畫面」

#### Mobile (iOS Safari)
1. 點擊分享按鈕
2. 選擇「加入主畫面」
3. 自訂名稱後點擊「新增」

## 技術細節

### Service Worker 快取策略

```javascript
// Static Assets - Cache First
- 優先使用快取
- 提升載入速度
- 支援離線瀏覽

// HTML Pages - Network First
- 優先載入最新內容
- 網路失敗時使用快取
- 保證內容即時性

// API Requests - Network Only
- 始終獲取最新數據
- 避免快取過期問題
```

### PWA 圖示規格

| 尺寸 | 用途 | 檔案 |
|------|------|------|
| 192x192 | 標準圖示 | icon-192x192.png |
| 512x512 | 高解析度圖示 | icon-512x512.png |
| SVG | 向量圖示 | logo-icon.svg |

### 瀏覽器支援

- ✅ Chrome/Edge (Desktop & Mobile)
- ✅ Safari (iOS 11.3+)
- ✅ Firefox
- ✅ Samsung Internet
- ⚠️ Safari (macOS) - 有限支援

## 部署檢查清單

- [x] manifest.json 配置完整
- [x] PWA 圖示已生成並正確引用
- [x] Service Worker 已建立
- [x] Service Worker 註冊邏輯已實作
- [x] PWA meta tags 已加入 HTML
- [x] PWAInstaller 元件已整合到 Layout
- [ ] HTTPS 已啟用（生產環境必需）
- [ ] 使用 Lighthouse 執行 PWA 稽核
- [ ] 在多種裝置上測試安裝流程

## 後續優化建議

1. **離線頁面**: 建立專用的離線提示頁面
2. **推播通知**: 實作 Web Push Notifications
3. **背景同步**: 使用 Background Sync API 處理離線操作
4. **更新提示**: 當有新版本時提示使用者重新載入
5. **快取管理**: 實作更精細的快取版本控制

## 監控與分析

建議追蹤以下指標：
- PWA 安裝率
- Service Worker 快取命中率
- 離線訪問次數
- 從主畫面啟動的比例

## 參考資源

- [Web.dev PWA Checklist](https://web.dev/pwa-checklist/)
- [MDN PWA Guide](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
- [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Web App Manifest](https://developer.mozilla.org/en-US/docs/Web/Manifest)

---

**實作完成日期**: 2025-12-03
**版本**: v1.0.0
**狀態**: ✅ 已完成
