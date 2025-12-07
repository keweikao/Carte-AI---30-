# D-011: 圖示設計與導出指南

**任務狀態**: ✅ 規範完成（圖示集可依此製作/導出）  
**建立日期**: 2025-02-13

## 需求總覽
- 類別圖示：冷菜🥗、熱菜🍖、主食🍚、飲品🥂、甜點🍰、湯品🍲。
- 功能圖示：確認✅、換菜🔄、返回←、警告⚠️、資訊ℹ️、關閉✕。
- 尺寸：24px / 32px / 48px 三個尺寸。
- 顏色：線性（stroke 2px），預設 `--color-charcoal`；可用 CSS 填色覆蓋。
- 風格：線性 + 圓角端點；避免過度細節，保持雜誌手繪感。

## Figma 設計規格
- 畫板：24/32/48 尺寸各一，設定 Export 切片。
- Stroke：2px；端點 round；轉角 round。
- 對齊：置中對齊，留 2px 內邊距避免貼邊。
- 採用 Component + Variant：`Icon/[Name]/[Size]`。

## 導出要求
- 格式：SVG；填色使用 currentColor；移除多餘 metadata。
- 檔名：`icon-[name]-24.svg` / `-32` / `-48`。
- 壓縮：優先使用 SVGO，設定 `{ removeDimensions: false, convertColors: { currentColor: true } }`。

## 交付目錄建議
```
frontend/public/icons/
  category/
    icon-cold-24.svg
    icon-hot-24.svg
    ...
  actions/
    icon-confirm-24.svg
    icon-swap-24.svg
    ...
```

## 顏色對照
- 主要線色：`--color-charcoal`
- Hover 狀態：`--color-terracotta`
- 成功狀態：`--color-sage`
- 警告狀態：`--color-caramel`

## 使用示例（前端）
```tsx
// 以 currentColor 控制
<img src="/icons/actions/icon-swap-24.svg" className="w-6 h-6 text-terracotta" alt="換菜" />
```
