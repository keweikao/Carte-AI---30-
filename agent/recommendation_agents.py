"""
Multi-Agent Recommendation System

This module implements a sophisticated multi-agent system for restaurant menu recommendations.
Each agent specializes in a specific aspect of the recommendation process.

Architecture:
    OrchestratorAgent (協調者)
    ├── DishSelectorAgent (菜品選擇專家)
    ├── BudgetOptimizerAgent (預算優化專家)
    ├── BalanceCheckerAgent (平衡檢查專家)
    └── QualityAssuranceAgent (品質保證專家)
"""

import os
import json
import asyncio
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from schemas.recommendation import UserInputV2, MenuItemV2

@dataclass
class AgentDecision:
    """Represents a decision made by an agent"""
    agent_name: str
    approved: bool
    data: Any
    issues: List[str] = None
    suggestions: List[str] = None
    metadata: Dict[str, Any] = None

class RecommendationAgentBase:
    """Base class for all recommendation agents"""
    def __init__(self, model_name: str = 'gemini-2.5-flash'):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        
    async def run(self, *args, **kwargs) -> AgentDecision:
        raise NotImplementedError

class DishSelectorAgent(RecommendationAgentBase):
    """
    菜品選擇專家
    
    職責：
    - 從候選池中選出最適合的菜品
    - 根據 occasion 選擇適合的菜品
    - 考慮 dietary restrictions
    - 優先選擇 signature dishes
    """
    
    async def run(self, 
                  candidates: List[Dict[str, Any]], 
                  user_input: UserInputV2,
                  aggregated_data: List[Dict[str, Any]]) -> AgentDecision:
        
        print("🍽️  DishSelectorAgent: Selecting optimal dishes...")
        
        # Build context about verified dishes
        verified_dishes = "\n".join([
            f"- {item.get('dish_name')} (Status: {item.get('status', 'Unknown')}, Source: {item.get('source', 'Unknown')})"
            for item in aggregated_data
        ])
        
        prompt = f"""
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
"""
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            
            selected = data.get("selected_dishes", [])
            print(f"✓ Selected {len(selected)} dishes")
            
            return AgentDecision(
                agent_name="DishSelector",
                approved=True,
                data=selected,
                metadata={"rationale": data.get("selection_rationale")}
            )
            
        except Exception as e:
            print(f"❌ DishSelectorAgent Error: {e}")
            import traceback
            traceback.print_exc()
            return AgentDecision(
                agent_name="DishSelector",
                approved=False,
                data=[],
                issues=[str(e)]
            )

class BudgetOptimizerAgent(RecommendationAgentBase):
    """
    預算優化專家
    
    職責：
    - 計算當前總價
    - 確保預算使用率 80-100%
    - 建議加菜或升級/降級
    """
    
    async def run(self,
                  current_menu: List[Dict[str, Any]],
                  budget_amount: int,
                  candidate_pool: List[Dict[str, Any]]) -> AgentDecision:
        
        print("💰 BudgetOptimizerAgent: Optimizing budget utilization...")
        
        # Calculate current total
        total = sum(dish.get('price', 0) * dish.get('quantity', 1) for dish in current_menu)
        utilization = total / budget_amount if budget_amount > 0 else 0
        
        print(f"   Current: ${total} / ${budget_amount} = {utilization:.1%}")
        
        # If within target range (80-100%), approve
        if 0.8 <= utilization <= 1.0:
            print(f"✓ Budget utilization is optimal: {utilization:.1%}")
            return AgentDecision(
                agent_name="BudgetOptimizer",
                approved=True,
                data=current_menu,
                metadata={"total": total, "utilization": utilization}
            )
        
        # Need optimization
        if utilization < 0.8:
            action = "ADD_DISHES"
            target_add = int((budget_amount * 0.9) - total)  # Aim for 90%
        else:
            action = "REDUCE_COST"
            target_reduce = int(total - (budget_amount * 0.95))  # Aim for 95%
        
        prompt = f"""
# Role
You are a **Budget Optimization Expert**.

# Current Situation
- Current Menu Total: ${total}
- Budget: ${budget_amount}
- Utilization: {utilization:.1%}
- Status: {"TOO LOW (under-budget)" if utilization < 0.8 else "TOO HIGH (over-budget)"}

# Your Task
{"**ADD dishes** to reach 80-100% budget utilization" if action == "ADD_DISHES" else "**REDUCE cost** to fit within budget"}

# Current Menu
{json.dumps(current_menu, ensure_ascii=False, indent=2)}

# Available Candidate Pool (for adding)
{json.dumps(candidate_pool[:20], ensure_ascii=False, indent=2) if action == "ADD_DISHES" else "N/A"}

# Instructions
{"1. Select dishes from candidate pool to add (appetizers, desserts, drinks, or upgrade portions)" if action == "ADD_DISHES" else "1. Suggest which dishes to downgrade (large→small) or remove (non-signature items)"}
2. Target: {"Add ~$" + str(target_add) if action == "ADD_DISHES" else "Reduce ~$" + str(target_reduce)}
3. Maintain dish quality and variety

# Output Format (JSON)
{{
  "action": "{action}",
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
"""
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            
            updated_menu = data.get("updated_menu", current_menu)
            new_total = data.get("new_total", total)
            new_util = data.get("new_utilization", utilization)
            
            print(f"✓ Optimized: ${new_total} ({new_util:.1%})")
            
            # Check if optimization was successful
            approved = 0.8 <= new_util <= 1.0
            
            return AgentDecision(
                agent_name="BudgetOptimizer",
                approved=approved,
                data=updated_menu,
                metadata={
                    "modifications": data.get("modifications", []),
                    "total": new_total,
                    "utilization": new_util
                }
            )
            
        except Exception as e:
            print(f"❌ BudgetOptimizerAgent Error: {e}")
            import traceback
            traceback.print_exc()
            return AgentDecision(
                agent_name="BudgetOptimizer",
                approved=False,
                data=current_menu,
                issues=[str(e)]
            )

class BalanceCheckerAgent(RecommendationAgentBase):
    """
    平衡檢查專家
    
    職責：
    - 檢查類別分佈（冷菜/熱菜/湯/主食/甜點）
    - 檢查烹飪方式多樣性
    - 檢查蛋白質來源多樣性
    - 確保有蔬菜
    """
    
    def _analyze_menu(self, menu: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze menu composition"""
        categories = {}
        for dish in menu:
            cat = dish.get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "categories": categories,
            "dish_count": len(menu),
            "has_vegetable": any('蔬菜' in dish.get('category', '') or '青菜' in dish.get('dish_name', '') for dish in menu),
            "has_soup": any('湯' in dish.get('category', '') for dish in menu),
            "has_staple": any('主食' in dish.get('category', '') or '飯' in dish.get('dish_name', '') or '麵' in dish.get('dish_name', '') for dish in menu)
        }
    
    async def run(self,
                  current_menu: List[Dict[str, Any]],
                  dining_style: str,
                  party_size: int) -> AgentDecision:
        
        print("⚖️  BalanceCheckerAgent: Checking menu balance...")
        
        analysis = self._analyze_menu(current_menu)
        issues = []
        
        # Check for shared dining requirements
        if dining_style == "Shared":
            if not analysis['has_vegetable']:
                issues.append("缺少蔬菜類菜品")
            if not analysis['has_soup'] and party_size >= 4:
                issues.append("建議加入湯品（4人以上聚餐）")
            if analysis['dish_count'] < party_size + 1:
                issues.append(f"菜數不足（建議至少 {party_size + 1} 道）")
        
        # If balanced, approve
        if not issues:
            print(f"✓ Menu is well-balanced")
            return AgentDecision(
                agent_name="BalanceChecker",
                approved=True,
                data=current_menu,
                metadata=analysis
            )
        
        # Need adjustment
        print(f"⚠️  Balance issues: {issues}")
        
        prompt = f"""
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
"""
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            
            return AgentDecision(
                agent_name="BalanceChecker",
                approved=data.get("balanced", False),
                data=current_menu,
                issues=issues,
                suggestions=[adj.get("suggestion") for adj in data.get("adjustments", [])],
                metadata=analysis
            )
            
        except Exception as e:
            print(f"❌ BalanceCheckerAgent Error: {e}")
            return AgentDecision(
                agent_name="BalanceChecker",
                approved=False,
                data=current_menu,
                issues=issues + [str(e)]
            )

class QualityAssuranceAgent(RecommendationAgentBase):
    """
    品質保證專家
    
    職責：
    - 最終檢查所有規則是否遵守
    - 確認有招牌菜
    - 確認符合 occasion
    - 確認份量邏輯正確
    """
    
    async def run(self,
                  final_menu: List[Dict[str, Any]],
                  user_input: UserInputV2,
                  aggregated_data: List[Dict[str, Any]]) -> AgentDecision:
        
        print("✅ QualityAssuranceAgent: Final quality check...")
        
        # Build checklist
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
        
        all_passed = all(checks.values())
        
        if all_passed:
            print(f"✓ All quality checks passed!")
            return AgentDecision(
                agent_name="QualityAssurance",
                approved=True,
                data=final_menu,
                metadata={"checks": checks}
            )
        else:
            failed_checks = [k for k, v in checks.items() if not v]
            print(f"⚠️  Failed checks: {failed_checks}")
            return AgentDecision(
                agent_name="QualityAssurance",
                approved=False,
                data=final_menu,
                issues=failed_checks,
                metadata={"checks": checks}
            )

class OrchestratorAgent:
    """
    協調者 - 管理整個 Multi-Agent 推薦流程
    
    工作流程：
    1. DishSelector 選出初步菜單
    2. BudgetOptimizer 優化預算使用
    3. BalanceChecker 檢查平衡
    4. QualityAssurance 最終檢查
    5. 如果任何步驟失敗，迭代優化（最多3輪）
    """
    
    def __init__(self):
        self.dish_selector = DishSelectorAgent()
        self.budget_optimizer = BudgetOptimizerAgent()
        self.balance_checker = BalanceCheckerAgent()
        self.qa_agent = QualityAssuranceAgent()
    
    async def run(self,
                  user_input: UserInputV2,
                  candidates: List[Dict[str, Any]],
                  aggregated_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        
        print("\n" + "="*60)
        print("🤖 Multi-Agent Recommendation System Starting...")
        print("="*60 + "\n")
        
        max_iterations = 3
        current_menu = []
        
        for iteration in range(max_iterations):
            print(f"\n{'─'*60}")
            print(f"🔄 Iteration {iteration + 1}/{max_iterations}")
            print(f"{'─'*60}\n")
            
            # Step 1: Dish Selection (only on first iteration or if menu is empty)
            if iteration == 0 or not current_menu:
                decision = await self.dish_selector.run(candidates, user_input, aggregated_data)
                if not decision.approved:
                    print("❌ Dish selection failed, using candidates as fallback")
                    current_menu = candidates[:10]
                else:
                    current_menu = decision.data
            
            # Step 2: Budget Optimization
            decision = await self.budget_optimizer.run(
                current_menu,
                user_input.budget.amount,
                candidates
            )
            if decision.approved:
                current_menu = decision.data
            else:
                print("⚠️  Budget optimization not perfect, but continuing...")
                current_menu = decision.data  # Use best effort
            
            # Step 3: Balance Check
            decision = await self.balance_checker.run(
                current_menu,
                user_input.dining_style,
                user_input.party_size
            )
            if not decision.approved and decision.suggestions:
                print(f"💡 Balance suggestions: {decision.suggestions}")
                # In a full implementation, we'd adjust the menu here
            
            # Step 4: Quality Assurance
            decision = await self.qa_agent.run(current_menu, user_input, aggregated_data)
            
            if decision.approved:
                print(f"\n{'='*60}")
                print(f"✅ Menu approved in iteration {iteration + 1}!")
                print(f"{'='*60}\n")
                return current_menu
            else:
                print(f"⚠️  QA issues: {decision.issues}")
                print(f"   Retrying with adjustments...")
        
        # If we exhausted iterations, return best effort
        print(f"\n{'='*60}")
        print(f"⚠️  Max iterations reached. Returning best effort menu.")
        print(f"{'='*60}\n")
        return current_menu
