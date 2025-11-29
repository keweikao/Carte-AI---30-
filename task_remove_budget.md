# 任務清單：移除預算限制與優化點餐自由度

> **規格文件**: [specs/remove_budget_constraint.md](./specs/remove_budget_constraint.md)  
> **實作計畫**: [implementation_plan_remove_budget.md](./implementation_plan_remove_budget.md)

## 任務狀態圖例
- ✅ 已完成
- 🚧 進行中
- ⏳ 待執行

---

- [x] **Phase 1: Backend Refactoring**
    - [x] Modify `UserInputV2` schema to make `budget` optional.
    - [x] Remove `BudgetOptimizerAgent` from `recommendation_agents.py`.
    - [x] Update `OrchestratorAgent` to remove budget optimization step.
    - [x] Update `DishSelectorAgent` prompt to handle "no budget" scenario and "All Signatures" logic.
    - [x] Update `QualityAssuranceAgent` to remove budget checks and add "Over-ordering Check".

- [x] **Phase 2: Frontend Input UX**
    - [x] Remove Budget Input Page (`frontend/src/app/input/budget/page.tsx` - if exists, or modify main input page).
    - [x] Update `frontend/src/app/input/page.tsx` to remove budget slider/input.
    - [x] Add "All Signatures" (👑) option to Occasion selector.
    - [x] Update API calls to send `budget: null` or omit it.

- [x] **Phase 3: Frontend Recommendation UX**
    - [x] Remove "Budget Utilization" display from Recommendation Page.
    - [x] Implement "Free Selection" mode (no forced completion).
    - [x] Add "Live Calculator" (Sticky Bar) for total price.
    - [x] Add "Mode Badge" for special occasions (e.g., All Signatures).

- [x] **Phase 4: Verification**
    - [x] Create test script `test_no_budget.py`.
    - [x] Verify "No Budget" flow.
    - [x] Verify "All Signatures" flow.
    - [x] Verify "Over-ordering Check" (via logs).
