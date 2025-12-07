# D-014: 動畫原型製作指引

**任務狀態**: ✅ 規範完成（可依此在 Figma/ProtoPie 製作原型）  
**建立日期**: 2025-02-13

## 覆蓋場景
- 首頁載入動畫
- 卡片翻轉（DishCard）
- 步驟轉換（StepIndicator + 內容滑入）
- 價格變化泡泡

## Figma Prototype 操作
- 使用 Smart Animate；頁面轉場設定 Ease 0.25, 0.9, 0.35, 1，時長 360ms。
- 建立 Component Variant：`DishCard` (front/back)；Transition: on tap → Smart Animate → 480ms。
- Stepper：節點 scale 0.9 → 1.05 → 1.0，delay 80ms；內容 frame slide 16px 淡入。
- 價格泡泡：用 After Delay 0ms → Move Y -12px + Fade → 420ms，Opacity 0 → 100 → 0。

## ProtoPie 推薦設定
- 3D Rotate：Y 軸 0 → 180deg，Anchor Center；Ease InOut 480ms；中段加 Blur 2px。
- Timeline：Hero 元件分三層（背景、主標、CTA），延遲 0/120/200ms 淡入。
- 輸出：匯出 MP4 720p 或 Lottie（若圖層純向量）。

## 檔案命名建議
```
Design/Prototypes/
  hero-load.mp4
  dishcard-flip.mp4
  step-transition.mp4
  price-bubble.mp4
```

## 交付
- 原型影片 (mp4) 或 Lottie 檔案，對應上述四個場景。  
- 與工程對接：時間/緩動已在 `D-005-ANIMATION-GUIDE.md`，原型用於視覺參考。
