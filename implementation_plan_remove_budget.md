# 實作計畫：移除預算限制與優化點餐自由度

> **規格文件**: [specs/remove_budget_constraint.md](./specs/remove_budget_constraint.md)

## Phase 1: Schema & Backend Core (後端核心調整)

### Task 1.1: 修改資料模型
- **目標**: 讓 `budget` 變為非必填，新增 `occasion` 選項。
- **檔案**: `schemas/recommendation.py`
- **變更**:
  - `UserInputV2.budget`: 改為 `Optional[BudgetV2] = None`。
  - `OccasionEnum` (如果有的話): 新增 `all_signatures`。

### Task 1.2: 停用 BudgetOptimizerAgent
- **目標**: 從推薦流程中移除預算優化步驟。
- **檔案**: `agent/recommendation_agents.py`
- **變更**:
  - 在 `DiningAgent.run` (或 `Orchestrator.run`) 中，註解掉或移除 `budget_optimizer.run()` 的呼叫。
  - 移除 `_calculate_menu_score` 中的預算評分邏輯。

## Phase 2: Prompt Engineering (Agent 邏輯優化)

### Task 2.1: 更新 DishSelectorAgent Prompt
- **目標**: 移除價格限制，加入「招牌全制霸」邏輯。
- **檔案**: `agent/recommendation_agents.py` (`DishSelectorAgent` class)
- **變更**:
  - 重寫 `SYSTEM_PROMPT` 或 `run` 方法中的 Prompt 建構邏輯。
  - 加入 `if occasion == 'all_signatures'` 的條件分支指令。
  - 強調 "Ignore Price, Focus on Experience"。

### Task 2.2: 更新 QualityAssuranceAgent 評分
- **目標**: 調整評分標準，不再因超預算而扣分。
- **檔案**: `agent/recommendation_agents.py`
- **變更**:
  - 移除預算檢查相關代碼。
  - 增加對 "Signature Coverage" (招牌覆蓋率) 的評分權重。
  - **新增 "Over-ordering Check"**: 檢查是否點太多菜，產生 Warning。

## Phase 3: Frontend UX (前端介面調整)

### Task 3.1: 修改輸入頁面 (Input Page)
- **目標**: 移除預算輸入，新增情境選項。
- **檔案**: `frontend/src/app/input/page.tsx`
- **變更**:
  - 移除 `Budget` 相關的 State, Slider, Toggle Button。
  - 在 `Occasion` RadioGroup 中新增 `{ id: "all_signatures", label: "招牌全制霸", icon: Crown }`。
  - 更新 `handleNext` 邏輯，不再驗證預算。

### Task 3.2: 修改推薦頁面 (Recommendation Page)
- **目標**: 解除選擇限制，增強互動體驗。
- **檔案**: `frontend/src/app/recommendation/page.tsx`
- **變更**:
  - 移除「必須選滿 X 道菜」的阻擋邏輯。
  - 允許 `selectedItems` 為空或任意數量時提交。
  - **新增 Sticky Bar**: 在底部顯示即時總金額與人均。
  - **新增 Mode Badge**: 當 `all_signatures` 時顯示特殊標記。
  - 隱藏或移除 UI 上的預算進度條/警示。

## Phase 4: Verification (驗證與測試)

### Task 4.1: 測試腳本
- **目標**: 驗證新邏輯是否生效。
- **檔案**: `test_no_budget.py` (新增)
- **內容**:
  - 模擬 `all_signatures` 情境。
  - 驗證推薦結果是否包含高價招牌菜。
  - 驗證是否沒有預算錯誤。

### Task 4.2: 前端測試
- **目標**: 手動驗證 UI 流程。
- **步驟**:
  - 進入 Input Page，確認無預算欄位。
  - 選擇「招牌全制霸」。
  - 進入 Recommendation Page，確認可自由勾選並送出。
