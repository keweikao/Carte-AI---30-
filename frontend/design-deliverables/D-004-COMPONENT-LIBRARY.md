# D-004: 基礎組件庫設計規格

**任務狀態**: ✅ 規格完成（Figma 實稿可依此快速建立）  
**建立日期**: 2025-02-13

## 🎨 設計語言錨點
- **字體**: Display = Cormorant Garamond / Body = Noto Sans TC / Handwriting = Caveat
- **色彩 Token**: caramel (#D4A574), terracotta (#C85A54), sage (#8B9D83), cream-100 (#FFF8F0), charcoal (#2D2D2D)
- **圓角**: sm=8px, md=12px, lg=16px（卡片預設 16px）
- **陰影**: card = 0 10px 30px rgba(0,0,0,0.08); floating = 0 18px 40px rgba(0,0,0,0.12)
- **間距**: 8px 基準；常用 12/16/24px（space-3/4/5）

> 命名規則：`OW/[Component]/[Variant]/[State]`（Figma Styles & Components）。

## 🧩 Button（Primary/Secondary/Outline/Ghost）
| Variant | 填色 / 邊框 | 文字色 | 陰影 | Hover | Active | Disabled |
|---------|-------------|--------|------|-------|--------|----------|
| Primary | gradient-accent / none | #FFF | shadow-card | 漸層亮度 +4%，上移 1px | 降亮度 -6%，下沉 1px | 背景 40%，文字 #FFF/60 |
| Secondary | sage / none | #FFF | shadow-card | 提亮 4%，上移 1px | 降亮度 6%，下沉 1px | sage/40，文字 #FFF/60 |
| Outline | transparent / 1px terracotta | terracotta | none | 背景 terracotta/12 | 背景 terracotta/18 | 邊框 & 字色 40% |
| Ghost | transparent / none | charcoal | none | 背景 cream-200 | 背景 cream-200 + 邊框 1px caramel/40 | 字色 40% |

- 圓角: 999px（膠囊）。Padding: 12px 18px(sm)/16px 22px(md)/18px 26px(lg)。
- Icon Button: 左 icon 16px，文字間距 8px。

## 🃏 Card（default/selected/hover）
| 狀態 | 背景 | 邊框 | 陰影 | 其他 |
|------|------|------|------|------|
| default | #FFF | 1px rgba(45,45,45,0.06) | shadow-card | 圓角 16px，內距 20-24px |
| hover | #FFF | 1px caramel/30 | shadow-floating | 輕微上移 2px |
| selected | gradient-accent/6 覆蓋 | 1px terracotta | shadow-floating | 左上角角標 ✓（sage 背景，icon 白） |

- 手寫推薦理由使用 Caveat，文字 -2deg，顏色 terracotta-700。

## ✏️ Input（text/number/search/error）
- 背景: surface，邊框 1px border，圓角 12px，內距 14px 16px。
- Placeholder: charcoal/40；輸入文字: charcoal。
- Focus: 邊框 1px caramel，陰影 0 0 0 4px caramel/16。
- Error: 邊框 error，輔助文字 error；icon (AlertCircle) terracotta。
- 搜尋框: 左側 icon 16px，icon 與文字間距 10px。

## 🏷️ Badge（類別標籤）
- Variants: neutral (cream-200, charcoal/80)、accent (terracotta, #FFF)、success (sage, #FFF)、warning (caramel, charcoal)。
- Style: 高度 28px，圓角 999px，Padding 10px 14px，字體 Noto Sans TC 13px/500。
- 可加入左側 icon 14px，間距 6px。

## 📊 Progress（載入/完成）
- 軌道: cream-200，高度 10px，圓角 999px。
- 進度條: gradient-accent；動態使用 Framer Motion 6s 緩動（easeInOut）循環。
- 完成狀態: 進度條顏色切換為 sage，末端放大 1.1 並脈衝 2 次。

## 🔖 樣式標註範例（CSS 變數對應）
```css
.button-primary { background: var(--gradient-accent); color: #fff; }
.card-default { box-shadow: var(--shadow-card); border: 1px solid var(--color-border); }
.input-focus { box-shadow: 0 0 0 4px rgba(212,165,116,0.16); }
```

## 📎 交付
- 本文件為工程交接用規格，對應 `DESIGN_SYSTEM.md` 色彩/字體/間距 Token。
- Figma Components 可按表格設定 Auto Layout 與 Style 名稱生成。
