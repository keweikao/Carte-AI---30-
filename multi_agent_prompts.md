# Multi-Agent Recommendation System - Prompts 優化文件

這個文件包含所有 Agent 的 Prompt，方便您優化後直接替換回程式碼。

---

## 1️⃣ DishSelectorAgent (菜品選擇專家)

**檔案位置**: `agent/recommendation_agents.py` Line 50-95

**當前 Prompt**:

```
# Role
You are a **Dish Selection Expert** specializing in curating the perfect menu based on user context.

# Your Task
From the candidate pool below, select the BEST dishes that match the user's needs.

# Candidate Pool
{json.dumps(candidates[:30], ensure_ascii=False, indent=2)}

# Verified Signature Dishes (from Multi-Agent Analysis)
{verified_dishes}

# User Context
- Party Size: {user_input.party_size}
- Dining Style: {user_input.dining_style}
- Occasion: {user_input.occasion or 'casual'}
- Dietary Restrictions: {', '.join(user_input.preferences) if user_input.preferences else 'None'}
- Budget: {user_input.budget.amount} TWD ({user_input.budget.type})

# Selection Criteria (Priority Order)
1. **MUST include verified signature dishes** (Must Order / Hidden Gem)
2. **Match occasion requirements**:
   - Business: Easy to eat, presentable, no messy foods
   - Date: Beautiful presentation, romantic
   - Family: Shareable, suitable for all ages
   - Friends: Fun, adventurous, high CP value
   - Fitness: High protein, low carb, grilled/steamed
3. **Respect dietary restrictions** (hard constraints)
4. **Ensure variety** in categories and cooking methods

# Output Format (JSON)
{{
  "selected_dishes": [
    {{
      "dish_name": "String",
      "dish_name_local": "String",
      "price": Integer,
      "quantity": Integer,
      "category": "String",
      "reason": "String (Why selected for THIS user)",
      "tag": "必點/隱藏版/人氣/招牌 or null"
    }}
  ],
  "selection_rationale": "String (Overall strategy explanation)"
}}

**Target**: Select 10-12 dishes as initial pool (backend will refine to final 5-7)
```

**優化建議區域**:
- [ ] Selection Criteria 是否需要更細緻？
- [ ] Occasion requirements 是否完整？
- [ ] 是否需要加入「避免選擇」的規則？

---

## 2️⃣ BudgetOptimizerAgent (預算優化專家)

**檔案位置**: `agent/recommendation_agents.py` Line 120-220

**當前 Prompt** (分兩種情況):

### 情況 A: 預算使用率 < 80% (需要加菜)

```
# Role
You are a **Budget Optimization Expert**.

# Current Situation
- Current Menu Total: ${total}
- Budget: ${budget_amount}
- Utilization: {utilization:.1%}
- Status: TOO LOW (under-budget)

# Your Task
**ADD dishes** to reach 80-100% budget utilization

# Current Menu
{json.dumps(current_menu, ensure_ascii=False, indent=2)}

# Available Candidate Pool (for adding)
{json.dumps(candidate_pool[:20], ensure_ascii=False, indent=2)}

# Instructions
1. Select dishes from candidate pool to add (appetizers, desserts, drinks, or upgrade portions)
2. Target: Add ~${target_add}
3. Maintain dish quality and variety

# Output Format (JSON)
{{
  "action": "ADD_DISHES",
  "modifications": [
    {{
      "type": "add/remove/upgrade/downgrade",
      "dish_name": "String",
      "reason": "String"
    }}
  ],
  "updated_menu": [
    {{
      "dish_name": "String",
      "dish_name_local": "String",
      "price": Integer,
      "quantity": Integer,
      "category": "String",
      "reason": "String",
      "tag": "String or null"
    }}
  ],
  "new_total": Integer,
  "new_utilization": Float
}}
```

### 情況 B: 預算使用率 > 100% (需要降級)

```
# Role
You are a **Budget Optimization Expert**.

# Current Situation
- Current Menu Total: ${total}
- Budget: ${budget_amount}
- Utilization: {utilization:.1%}
- Status: TOO HIGH (over-budget)

# Your Task
**REDUCE cost** to fit within budget

# Current Menu
{json.dumps(current_menu, ensure_ascii=False, indent=2)}

# Instructions
1. Suggest which dishes to downgrade (large→small) or remove (non-signature items)
2. Target: Reduce ~${target_reduce}
3. Maintain dish quality and variety

# Output Format (JSON)
{{
  "action": "REDUCE_COST",
  "modifications": [...],
  "updated_menu": [...],
  "new_total": Integer,
  "new_utilization": Float
}}
```

**優化建議區域**:
- [ ] 加菜策略是否合理？（開胃菜 vs 升級份量）
- [ ] 降級策略是否需要更明確的優先級？
- [ ] 是否需要考慮「CP 值」？

---

## 3️⃣ BalanceCheckerAgent (平衡檢查專家)

**檔案位置**: `agent/recommendation_agents.py` Line 280-330

**當前 Prompt**:

```
# Role
You are a **Menu Balance Expert**.

# Current Menu Analysis
{json.dumps(analysis, ensure_ascii=False, indent=2)}

# Identified Issues
{json.dumps(issues, ensure_ascii=False)}

# Current Menu
{json.dumps(current_menu, ensure_ascii=False, indent=2)}

# Your Task
Suggest adjustments to fix the balance issues while maintaining the overall quality.

# Output Format (JSON)
{{
  "adjustments": [
    {{
      "issue": "String (which issue this fixes)",
      "action": "add/replace",
      "suggestion": "String (what to add/replace)"
    }}
  ],
  "balanced": Boolean
}}
```

**優化建議區域**:
- [ ] 是否需要更明確的「平衡標準」？
- [ ] 是否需要檢查「烹飪方式多樣性」？
- [ ] 是否需要檢查「蛋白質來源多樣性」？

---

## 4️⃣ QualityAssuranceAgent (品質保證專家)

**檔案位置**: `agent/recommendation_agents.py` Line 335-390

**當前邏輯**: 使用程式碼檢查，沒有 LLM Prompt

**當前檢查項目**:
```python
checks = {}

# 1. Has signature dish?
has_signature = any(dish.get('tag') in ['必點', '招牌'] for dish in final_menu)
checks['has_signature'] = has_signature

# 2. Dietary restrictions respected?
dietary_safe = True
for dish in final_menu:
    dish_name = dish.get('dish_name', '').lower()
    for pref in (user_input.preferences or []):
        if '不吃牛' in pref and ('牛' in dish_name or 'beef' in dish_name):
            dietary_safe = False
        if '不吃豬' in pref and ('豬' in dish_name or 'pork' in dish_name):
            dietary_safe = False
        if '素食' in pref and any(meat in dish_name for meat in ['肉', '雞', '魚', '蝦']):
            dietary_safe = False
checks['dietary_safe'] = dietary_safe

# 3. Quantity logic correct?
quantity_correct = all(dish.get('quantity', 0) > 0 for dish in final_menu)
checks['quantity_logic'] = quantity_correct

# 4. Occasion appropriate?
occasion_match = True  # Simplified for now
checks['occasion_match'] = occasion_match
```

**優化建議**:
- [ ] 是否需要改用 LLM 做更智慧的檢查？
- [ ] Occasion 檢查目前是 placeholder，需要實作嗎？
- [ ] 是否需要加入「份量合理性」檢查？

---

## 5️⃣ OrchestratorAgent (協調者)

**檔案位置**: `agent/recommendation_agents.py` Line 395-460

**當前邏輯**: 純流程控制，沒有 Prompt

**工作流程**:
```python
for iteration in range(max_iterations):
    # Step 1: 選菜 (DishSelectorAgent)
    # Step 2: 預算優化 (BudgetOptimizerAgent)
    # Step 3: 平衡檢查 (BalanceCheckerAgent)
    # Step 4: 品質檢查 (QualityAssuranceAgent)
    
    if qa_result['approved']:
        return menu  # Success!
    else:
        # 進入下一輪迭代
```

**優化建議**:
- [ ] 是否需要加入「學習機制」？（記錄失敗原因）
- [ ] 是否需要動態調整 Agent 呼叫順序？
- [ ] 是否需要加入「提前終止」條件？

---

## 📝 優化指南

### 優化原則
1. **明確性**: Prompt 是否清楚表達任務目標？
2. **可執行性**: LLM 是否能理解並執行指令？
3. **一致性**: 不同 Agent 的 Prompt 風格是否一致？
4. **完整性**: 是否涵蓋所有邊界情況？

### 優化流程
1. 在下方寫下您的優化版本
2. 標註修改的原因
3. 我會幫您替換回程式碼

---

## ✍️ 您的優化版本

### DishSelectorAgent 優化版:
```
[請在此處貼上您優化後的 Prompt]
```

**修改原因**:
- 

---

### BudgetOptimizerAgent 優化版:
```
[請在此處貼上您優化後的 Prompt]
```

**修改原因**:
- 

---

### BalanceCheckerAgent 優化版:
```
[請在此處貼上您優化後的 Prompt]
```

**修改原因**:
- 

---

### QualityAssuranceAgent 優化版:
```
[如果要改用 LLM，請在此處貼上 Prompt]
```

**修改原因**:
- 

---

### OrchestratorAgent 優化版:
```
[如果需要加入 Prompt，請在此處貼上]
```

**修改原因**:
- 

---

## 🔗 相關檔案

- 主檔案: `agent/recommendation_agents.py`
- 測試檔案: `test_multi_agent.py`
- Schema: `schemas/recommendation.py`
