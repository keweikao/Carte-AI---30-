# 規格文件：移除預算限制與優化點餐自由度

> **狀態**: Draft
> **日期**: 2025-11-29
> **相關檔案**: `frontend/src/app/input/page.tsx`, `agent/recommendation_agents.py`, `schemas/recommendation.py`

## 1. 背景與目標

目前的推薦系統強制使用者設定預算，這導致了兩個問題：
1. **限制了美食體驗**：對於想體驗所有招牌菜的使用者，預算限制會導致 AI 為了湊金額而犧牲掉核心美味。
2. **操作不自由**：推薦結果頁面強制綁定選擇，使用者無法靈活決定最終菜單。

本計畫的目標是將 AI 從「預算管家」轉型為「美食顧問」，專注於根據人數、情境與偏好提供最佳配餐，並賦予使用者完全的選擇權。

## 2. 使用者體驗 (UX) 變更

### 2.1 輸入頁面 (`input/page.tsx`)
- **移除**: 預算設定區塊（包含 Slider、客單/總價切換、金額輸入框）。
- **新增**: 在「用餐情境 (Occasion)」中新增選項：
  - **ID**: `all_signatures`
  - **Label**: "招牌全制霸"
  - **Icon**: 👑 (Crown) 或 🔥 (Fire)
  - **描述**: "不錯過任何必吃美味"

### 2.2 推薦結果頁面 (`recommendation/page.tsx`)
- **移除**: 強制選擇所有推薦菜色的驗證邏輯。
- **新增 UI 元素**:
  - **Sticky Bar (動態金額計算器)**: 在底部固定顯示 `總金額` 與 `人均`，當使用者取消勾選時即時更新。
  - **Mode Badge**: 當 `occasion == 'all_signatures'` 時，在頂部顯示 "👑 老饕全制霸模式：已為您網羅必吃招牌"。
- **行為**:
  - 使用者可以取消勾選任何 AI 推薦的菜色。
  - 即使只選 1 道菜，也能點擊「確認菜單」或「下一步」。
  - 移除「預算使用率」的顯示。

## 3. 後端與 Agent 邏輯變更

### 3.1 資料結構 (`schemas/recommendation.py`)
- `UserInputV2` 模型：
  - `budget`: 欄位改為 Optional，或在後端預設為 `None` / 無限大。
  - `occasion`: Enum 新增 `all_signatures`。

### 3.2 Agent 架構調整 (`agent/recommendation_agents.py`)

#### A. BudgetOptimizerAgent (移除/停用)
- **現況**: 負責計算預算使用率，並在超支時替換菜色。
- **變更**: **完全移除** 或 **停用** 此 Agent。
  - 在 `DiningAgent` 的流程中，不再呼叫 `budget_optimizer`。
  - 相關的 `run` 方法和 Prompt 可以保留但標記為 Deprecated。

#### B. DishSelectorAgent (核心調整)
- **Prompt 調整重點**:
  1. **移除預算約束**: 刪除所有關於 "Stay within budget", "Cost efficiency" 的指令。
  2. **強化份量控制**: 強調 "Portion control based on party size" (例如 N+1 規則)，確保點的菜夠吃且不浪費，但不受價格影響。
  3. **新增「招牌全制霸」邏輯**:
     - 當 `occasion == 'all_signatures'` 時：
       - **指令**: "Identify ALL dishes tagged as 'Signature', 'Must Order', or 'Chef's Special'."
       - **指令**: "Include ALL identified signature dishes in the menu, regardless of variety balance, unless they violate dietary restrictions."
       - **指令**: "If signature dishes exceed reasonable portion for the party size, prioritize the most popular ones but try to include as many as possible."

#### C. Orchestrator / QualityAssuranceAgent
- **評分邏輯調整**:
  - 移除 `budget_utilization` 的評分項目。
  - 提高 `satisfaction` (招牌覆蓋率) 的權重。
- **檢查邏輯**:
  - 移除 "Budget Check"。
  - 保留 "Dietary Check" (最重要)。
  - **新增 "Over-ordering Check" (暴食偵測)**:
    - 檢查是否點了過多菜色 (例如 > N + 4)。
    - 如果是，產生 Warning 提示前端 (但不阻擋)。

## 4. Prompt 設計草案

### DishSelectorAgent Prompt (更新版)

```python
ROLE = """
You are the "Culinary Experience Curator." You are not an accountant; you are a gastronome. Your goal is to maximize **Flavor** and **Experience**.
"""

TASK = """
# Decision Logic

## 1. The "All Signatures" Protocol (Crown Mode 👑)
**Trigger:** If `occasion` == 'all_signatures'
**Rule:**
1.  **Aggressive Inclusion:** You MUST include dishes tagged as "Signature", "Must Order", or "Chef's Special".
2.  **Category Override:** Ignore standard balance rules (e.g., it's okay to have 3 meat dishes if they are all signatures).
3.  **Portion Reality Check (Gluttony Protocol):**
    - If (Count of Signatures) <= (N + 2): **Select ALL of them.**
    - If (Count of Signatures) > (N + 3): **Prioritize Top N+3 Signatures** based on popularity/reviews. (Do not overwhelm the user with too many dishes).
4.  **Filler Strategy:** Do NOT add filler dishes (rice/soup/greens) unless necessary to cleanse the palate or if signatures are insufficient for the party size.

## 2. The Standard Protocol (Balanced Mode)
**Trigger:** All other occasions
**Rule:**
1.  **Anchor:** Start with Top 1-2 Verified Signatures.
2.  **Structure:** Target **N+1 dishes** (Sharing logic).
    - Mix: Meat + Veg + Carb/Soup.
3.  **Vibe Match:**
    - *Date:* Avoid messy food.
    - *Business:* Safe & Presentable.
"""
```

## 5. 實作計畫摘要

1. **Schema Update**: 修改 `UserInputV2`，讓 budget 可選。
2. **Frontend**: 修改 Input Page (移除預算, 新增情境) & Recommendation Page (移除驗證)。
3. **Backend**:
   - 修改 `DiningAgent` 流程，移除 `BudgetOptimizerAgent`。
   - 更新 `DishSelectorAgent` 的 Prompt。
   - 更新 `QualityAssuranceAgent` 的評分邏輯。
4. **Testing**: 驗證「招牌全制霸」情境是否真的推薦了所有招牌菜。
