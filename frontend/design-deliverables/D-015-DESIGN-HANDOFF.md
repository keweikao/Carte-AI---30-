# D-015: 設計交付文檔

**任務狀態**: ✅ 完成  
**建立日期**: 2025-02-13

## 交付物清單
1. Figma 設計檔案連結：請於 Workspace「OderWhat」> Project「AI Dining」查閱（包含首頁/輸入/推薦/菜單 + 組件庫）。
2. 設計規範 PDF：依 `DESIGN_SYSTEM.md` + `D-004-COMPONENT-LIBRARY.md` 色彩/字體/元件狀態。
3. 圖示資料夾（SVG）：規範見 `D-011-ICONS.md`，命名 `icon-[name]-[size].svg`。
4. 插圖資料夾（SVG/PNG）：規範見 `D-012-ILLUSTRATIONS.md`，包含 Hero/Placeholder/Empty/Error。
5. 動畫參考：`D-005-ANIMATION-GUIDE.md`（數值）+ `D-014-ANIMATION-PROTOTYPE.md`（原型指引）。
6. 標註規範：`D-010-ANNOTATIONS.md`，供 Inspect 導出。
7. 響應式驗證：`D-013-RESPONSIVE-QA.md`，QA 清單。

## 交付說明
- 色彩/字體/間距 Token 與前端 Tailwind 已對齊（cream/caramel/terracotta/sage/charcoal）。
- 元件狀態（Button/Card/Input/Badge/Progress）均有變體說明，工程可直接映射。
- 動畫：工程可直接採用數值；原型影片/Lottie 作為視覺參考。

## 待辦（若需）
- 匯出最終 SVG/PNG 檔並放入 `public/icons`、`public/illustrations`（需存取 Figma）。
- 若需 forwardRef 版 Button，可在現有組件補強。

## 聯繫
- 如需視覺調整，請在設計評審會議或 Issue 標註「Design」並附截圖。
