# D-012: 佔位圖與插圖規範

**任務狀態**: ✅ 規範完成（可依此繪製與導出）  
**建立日期**: 2025-02-13

## 風格
- 扁平線性 + 柔和填色，雜誌插畫感。
- 線條 2px 圓角，主色調沿用 cream/caramel/terracotta/sage/charcoal。
- 背景使用淡色塊或柔和漸層，避免過度細節。

## 必備插圖
1) **首頁 Hero**：美食桌景，含餐具與菜餚擺盤；背景淡奶油漸層。
2) **菜色照片佔位圖**：矩形卡片，中央食材線描 + 背景色塊；提供冷菜/熱菜/甜點/飲品四類變體。
3) **空狀態**：空盤與叉子，搭配提示文字區域；動物氣泡或手寫小註記可選。
4) **錯誤頁 (404/500)**：掉落的餐具或傘狀餐布，保留可放文案的留白。

## 尺寸與匯出
- Hero：1400×900 (桌面)，768×900 (行動)；建議 2x PNG + SVG 背景元素分層。
- 卡片佔位：1:1 與 4:3 兩組；導出 SVG（主），PNG 2x（備用）。
- 空狀態/錯誤：800×600；SVG 為主。

## 顏色 Token 對照
- 背景：`--color-cream-100` / `--gradient-hero`
- 主體：`--color-caramel`, `--color-terracotta`, `--color-sage`
- 線條：`--color-charcoal`

## 檔案命名建議
```
frontend/public/illustrations/
  hero-desktop.svg
  hero-mobile.svg
  placeholder-cold.svg
  placeholder-hot.svg
  placeholder-dessert.svg
  placeholder-drink.svg
  empty-state.svg
  error-404.svg
  error-500.svg
```

## 製作備註
- 線稿與填色分層，方便日後變更色票。
- 保留 16px 以上留白，避免 UI 壓住焦點。
- 若需要動態效果，可輸出 Lottie 12fps 簡化版（<300KB）。
