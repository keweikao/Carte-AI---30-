# D-005: 動畫規範設計

**任務狀態**: ✅ 規格完成（Figma/ProtoPie 可依此實作）  
**建立日期**: 2025-02-13

## 🎬 視覺節奏原則
- 動畫時間軸：入場 320–420ms、離場 240–320ms、微互動 120–200ms。
- 緩動：Enter/Exit 使用 `cubic-bezier(0.25, 0.9, 0.35, 1)`；微互動用 `easeOut`。
- 層次：背景元素輕微淡入；主要卡片平移 + 淡入；手寫文字延遲 80ms。

## 🏠 頁面轉場（Input → Recommendation → Menu）
- **入場**: 整體上移 12px → 0px，透明度 0 → 1，時長 360ms。
- **退場**: 下沉 8px，透明度 1 → 0.4 → 0，時長 260ms。
- **分段延遲**: Header 0ms、主區塊 80ms、浮動提示 140ms。

## 🃏 卡片翻轉動畫（DishCard）
- **幀設計 (5 幀)**:
  1. F0: 正面，scale 1.0
  2. F1: rotateY 15deg, scale 0.98
  3. F2: rotateY 90deg, scale 0.96（模糊 2px，快速過渡）
  4. F3: rotateY 165deg, scale 0.98（背面淡入）
  5. F4: rotateY 180deg, scale 1.0
- **時長**: 480ms；中段（F1→F3）使用 `easeInOut`。
- **光影**: 中段增加投影模糊 4px，結束回到 shadow-floating。

## 💸 價格變化動畫（+/-）
- **指示泡泡**: 圓角 12px，背景 success 或 warning。
- **動作**: 從卡片右上角向上漂移 12px，scale 0.94 → 1.0，透明度 0 → 1 → 0；時長 420ms。
- **色彩**: 降價用 success (#6B9D7F)、漲價用 warning (#E89C5C)。

## 🎉 慶祝動畫（完成決策）
- **觸發**: 所有菜品已確認且總價落在預算 ±20%。
- **設定**: canvas-confetti 角度 75°，散射 55，粒子 120，重力 0.9，顏色 palette = caramel/terracotta/sage/cream。
- **補充**: 1.2s 內淡出，背景增加微弱 vignette。

## 🔄 步驟轉換（Stepper）
- **Indicator**: 活動節點 scale 0.9 → 1.05 → 1.0，時長 220ms。
- **內容區塊**: 左/右滑入 16px，淡入 0 → 1，時長 280ms。
- **鍵盤/滑動**: Mobile 允許向左/右滑切換，採相同時間與緩動。

## 📦 交付與原型建議
- Figma: 使用 Smart Animate，為卡片翻轉建立 Component Variant 動畫；頁面轉場可用 Overlay 模擬。
- ProtoPie: 可導入 SVG 卡片，使用 3D rotate 實作翻轉；匯出 .mp4 供工程參考。
- Lottie: 如需導出，優先將價格變化泡泡轉為 Lottie 12fps 版本（<150KB）。

## ✅ 驗收對照
- 以上動畫時間與緩動可直接轉為工程數值，覆蓋 D-005 需求（頁面轉場、卡片翻轉、價格變化、慶祝效果）。
