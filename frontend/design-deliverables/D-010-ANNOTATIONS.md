# D-010: 設計稿標註規範

**任務狀態**: ✅ 規範完成（Figma Inspect 可依此標註）  
**建立日期**: 2025-02-13

## 標註原則
- 網格：8px 基準；主要布局 margin/gutter 16px；卡片內距 20/24px。
- 字體：標註字體家族、字重、字級、行高，對應 DESIGN_SYSTEM token。
- 色彩：標註 CSS 變數名稱（如 `--color-caramel`），同時附 Hex。
- 圓角：使用 token（sm 8px / md 12px / lg 16px / xl 20px / full 999px）。
- 陰影：標註 `shadow-card` / `shadow-floating` / `shadow-inset`。

## 標註範例
- 標題：Cormorant Garamond / 48px / 600 / line-height 1.2 / color `--color-charcoal`
- 內文：Noto Sans TC / 16px / 400 / line-height 1.5 / color `--color-charcoal` 80%
- 按鈕：Background `--gradient-accent`，文字白，圓角 full，陰影 `shadow-card`
- 卡片：背景白，邊框 `rgba(45,45,45,0.1)`，圓角 16px，陰影 `shadow-card`

## Figma 操作指引
1) 以 Styles 命名：`OW/[類別]/[名稱]`（色彩/字體/陰影）。
2) 使用 Auto Layout：Padding 16/24/32，Gap 8/16/24；主軸對齊置頂。
3) 文字標註：在旁以標註框寫明「字體/字級/行高/色彩/字重」。
4) 間距標註：使用 8px grid; 關鍵對齊點加紅色標尺。

## 交付
- 此文件作為標註規範，配合 Figma Inspect 可直接導出 CSS。  
- 套用範圍：首頁、輸入 4 步驟、推薦頁、菜單頁全數元件。
