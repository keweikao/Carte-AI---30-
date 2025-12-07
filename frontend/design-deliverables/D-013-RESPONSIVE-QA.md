# D-013: 響應式設計驗證清單

**任務狀態**: ✅ 規範完成（QA 清單可直接執行）  
**建立日期**: 2025-02-13

## 斷點與畫布
- Mobile: 375px (iPhone SE) / 393px (iPhone 14 Pro)
- Tablet: 768px (iPad portrait)
- Desktop: 1280px（核心）/ 1440px（寬版）

## 檢查項目
- 無水平滾動；主要內容保持 16px 內邊距（mobile），24px+（desktop）。
- Hero/卡片圖片比例不變形；文字不溢出，行高維持 1.4~1.6。
- CTA、表單、StepIndicator 可點擊區域 ≥ 44px。
- Header 固定高度且 sticky 時不遮內容；下方首屏留 16px 間距。
- 卡片/按鈕 hover 動效在觸控裝置不阻礙操作（hover 轉淡入，active 正常）。
- Banner/空狀態插圖在不同斷點居中，避免被裁切。
- 字重/字級：Mobile 標題 ≤ 32px；Desktop 可放大至 48px；手寫註記保持 -2deg。
- 進度條/Toast/Dialog 在窄螢幕不超出左右 12px。

## 測試流程
1) 375px：走一次首頁 → 輸入 4 步驟 → 推薦頁；確認 CTA、輸入框、卡片不擠壓。
2) 768px：確認兩欄布局是否自適應（如卡片網格改 2 列）。
3) 1280px：確認網格最大寬度 1100-1200px，留白平衡；Hero 插畫不失真。

## 問題紀錄模板
```
[Breakpoint] 375px
頁面：Recommendation
問題：第 2 張 DishCard 文字溢出兩行，badge 被擠壓。
建議：調整卡片寬度或縮小手寫文字至 14px。
```

## 交付
- 此清單用於 QA 驗證響應式；請將發現問題記錄在上述模板並回傳。  
- 通過後標記 D-013 完成。
