"""
Multi-Agent Recommendation System (Enhanced Version)

This module implements a sophisticated multi-agent system with emotional intelligence
for restaurant menu recommendations. Each agent specializes in a specific aspect.

Key Enhancements:
- Centerpiece concept for special occasions
- Authorized overspend for business/treat scenarios
- Feedback loop for iterative improvement
- Early stopping for efficiency
- Custom scenario handling
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
    critique: str = None  # For feedback loop

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
    菜品選擇專家 (Menu Architect)
    
    Enhanced with:
    - Centerpiece concept
    - Occasion protocols
    - Custom scenario handling
    - Feedback loop support
    """
    
    async def run(self, 
                  candidates: List[Dict[str, Any]], 
                  user_input: UserInputV2,
                  aggregated_data: List[Dict[str, Any]],
                  previous_critique: Optional[str] = None) -> AgentDecision:
        
        print("🍽️  DishSelectorAgent: Selecting optimal dishes...")
        
        # Build context about verified dishes
        verified_dishes = "\n".join([
            f"- {item.get('dish_name')} (Status: {item.get('status', 'Unknown')}, Source: {item.get('source', 'Unknown')})"
            for item in aggregated_data
        ])
        
        # Extract user note for custom scenario handling
        user_note = getattr(user_input, 'natural_input', None) or ""
        
        # NEW: Fetch personal memory
        memory_context = ""
        user_id = getattr(user_input, 'user_id', None)
        if user_id:
            try:
                from agent.memory_agent import MemoryAgent
                memory_agent = MemoryAgent()
                memory_context = await memory_agent.get_personal_memory(
                    user_id=user_id,
                    occasion=user_input.occasion
                )
                if memory_context:
                    print(f"  📚 Loaded personal memory for user {user_id}")
            except Exception as e:
                print(f"  ⚠️  Could not load memory: {e}")
        
        # Build previous critique section
        critique_section = ""
        if previous_critique:
            critique_section = f"""
# Previous Attempt Critique
The previous menu was rejected for the following reason:
{previous_critique}

**CRITICAL**: Address this issue in your new selection.
"""
        
        # Build memory section for prompt
        memory_section = ""
        if memory_context:
            memory_section = f"""
# 🔒 Personal Memory (HIGHEST PRIORITY - Never Ignore)
{memory_context}
"""
        
        prompt = f"""
# Role
You are the **"Menu Architect,"** an expert dining concierge. You curate the perfect menu by balancing **Gastronomy (Taste)**, **Logistics (Portion)**, and **Psychology (Context)**.

{critique_section}

# User Context & Constraints
- Party Size: {user_input.party_size}
- Dining Style: {user_input.dining_style}
- Occasion: {user_input.occasion or 'casual'}
- Dietary Restrictions: {', '.join(user_input.preferences) if user_input.preferences else 'None'} (STRICT HARD FILTER)
- User Note (HIGHEST PRIORITY): "{user_note}"
- Budget: {user_input.budget.amount} TWD ({user_input.budget.type})

{memory_section}
# Data Sources
## Candidate Pool
{json.dumps(candidates[:30], ensure_ascii=False, indent=2)}

## Verified Signature Dishes (from Multi-Agent Analysis)
{verified_dishes}

# Decision Logic (The Decoder Ring)

## 1. Custom Scenario Handling (PRIORITY CHECK)
**If User Note is provided:**
1. Parse the note for:
   - Specific cravings (e.g., "想吃湯", "want something crispy")
   - Mood/vibe (e.g., "心情不好", "celebrating", "tired")
   - Special requests (e.g., "不要太油", "要清淡")
2. **User Note OVERRIDES standard occasion rules** if there's a conflict
3. Example: Occasion=Fitness + Note="今天想放縱吃炸雞" → ALLOW fried chicken (small portion)

## 2. Occasion Protocol (The Vibe Check)
**IMPORTANT**: If User Note provides a custom scenario, adapt these rules accordingly.

* **Business:** "Safe & Impressive."
   - MUST include 1 **Centerpiece** (Whole Fish, Steak, Premium Soup, Signature Set) if budget allows
   - BAN: Messy food (Ribs, Shell-on Shrimp/Crab, Whole Chicken with bones), Spicy food that causes sweating
   - BAN: Foods requiring hands to peel/crack (Lobster, Crab, unless pre-shelled)
   - PREFER: Dishes that can be elegantly shared with serving spoons

* **Date:** "Mess-Free & Aesthetic."
   - BAN: Garlic/Onion heavy, Teeth-staining (Squid Ink, Beets), Unglamorous eating (Big Bones, Whole Fish with head)
   - BAN: Foods that require messy eating (Ribs, Shell-on seafood)
   - PREFER: Beautifully plated dishes, Boneless options, Shareable small plates
   - BONUS: Instagram-worthy presentation

* **Family:** "Inclusivity."
   - MUST include: 1 Soft dish (Elderly/kids friendly - Steamed Egg, Tofu, Soup), 1 Vegetable
   - CONSIDER: Kid-friendly options (Not too spicy, Not too exotic)
   - PREFER: Large shareable portions

* **Friends:** "Fun & Value."
   - PREFER: High CP value items, Adventurous/unique dishes
   - ALLOW: Messy foods (it's casual!)
   - BONUS: Conversation starters (unique presentations)

* **Fitness:** "Protein & Clean."
   - BOOST: High Protein (Grilled Chicken, Fish, Tofu), Steamed/Grilled items
   - BAN: Deep Fried (unless User Note overrides)
   - PREFER: Vegetables, Lean proteins

* **Custom/Other:** 
   - If occasion is not standard OR User Note provides context:
   - Extract intent from User Note (e.g., "comfort food" → warm soups, "light meal" → salads/small portions)
   - Adapt rules flexibly based on the vibe

## 3. Quantity & Structure Logic
* **Group (Sharing):** Target N+1 dishes (N = Party Size)
  - Structure: 1-2 Mains + 1 Veg + 1 Soup + 1 Starch + Others
  - If budget allows: Add Centerpiece
* **Individual:** 1 Main + 1 Staple OR 1 Set Meal per person

# Output Format (JSON)
{{
  "selected_dishes": [
    {{
      "dish_name": "String",
      "dish_name_local": "String",
      "price": Integer,
      "quantity": Integer,
      "category": "String",
      "reason": "String (MUST link to specific context: e.g., 'Selected for Date Night because boneless and elegant' or 'User requested soup, this is the signature option')",
      "tag": "必點/隱藏版/主秀/人氣/招牌 or null"
    }}
  ],
  "selection_rationale": "String (Explain overall strategy, especially if adapting to custom scenario)"
}}

**Target**: Select 10-12 dishes as initial pool
**CRITICAL**: If User Note conflicts with Occasion, prioritize User Note and explain in rationale.
"""
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            
            selected = data.get("selected_dishes", [])
            rationale = data.get("selection_rationale", "")
            print(f"✓ Selected {len(selected)} dishes")
            print(f"  Strategy: {rationale[:100]}...")
            
            return AgentDecision(
                agent_name="DishSelector",
                approved=True,
                data=selected,
                metadata={"rationale": rationale}
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
    預算優化專家 (Strategic Upselling Expert)
    
    Enhanced with:
    - Authorized overspend for special occasions
    - Quality upgrade priority
    - Portion adjustment
    """
    
    async def run(self,
                  current_menu: List[Dict[str, Any]],
                  budget_amount: int,
                  candidate_pool: List[Dict[str, Any]],
                  user_input: UserInputV2) -> AgentDecision:
        
        print("💰 BudgetOptimizerAgent: Optimizing budget utilization...")
        
        # Calculate current total
        total = sum(dish.get('price', 0) * dish.get('quantity', 1) for dish in current_menu)
        utilization = total / budget_amount if budget_amount > 0 else 0
        
        print(f"   Current: ${total} / ${budget_amount} = {utilization:.1%}")
        
        # Check if within target range (80-100%)
        if 0.8 <= utilization <= 1.0:
            print(f"✓ Budget utilization is optimal: {utilization:.1%}")
            return AgentDecision(
                agent_name="BudgetOptimizer",
                approved=True,
                data=current_menu,
                metadata={"total": total, "utilization": utilization}
            )
        
        # Determine action
        occasion = user_input.occasion or 'casual'
        
        if utilization < 0.8:
            action = "ADD_DISHES"
            target_add = int((budget_amount * 0.9) - total)
            prompt = self._build_upsell_prompt(current_menu, total, budget_amount, utilization, target_add, candidate_pool)
        else:
            # Over budget - check for authorized overspend
            action = "REDUCE_COST"
            target_reduce = int(total - (budget_amount * 0.95))
            prompt = self._build_reduce_prompt(current_menu, total, budget_amount, utilization, target_reduce, occasion)
        
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
            action_taken = data.get("action", action)
            justification = data.get("justification", "")
            
            print(f"✓ Action: {action_taken}")
            print(f"  New Total: ${new_total} ({new_util:.1%})")
            if justification:
                print(f"  Reason: {justification[:100]}...")
            
            # Check if optimization was successful
            # Allow authorized overspend
            approved = (0.8 <= new_util <= 1.0) or (action_taken == "AUTHORIZED_OVERSPEND" and new_util <= 1.2)
            
            return AgentDecision(
                agent_name="BudgetOptimizer",
                approved=approved,
                data=updated_menu,
                metadata={
                    "modifications": data.get("modifications", []),
                    "total": new_total,
                    "utilization": new_util,
                    "action": action_taken,
                    "justification": justification
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
    
    def _build_upsell_prompt(self, current_menu, total, budget_amount, utilization, target_add, candidate_pool):
        return f"""
# Role
You are a **Strategic Upselling Expert**. Your goal is to maximize the dining experience, not just stuff the user with food.

# Current Status
- Total: ${total} (Utilization: {utilization:.1%})
- Budget: ${budget_amount}
- Target to Add: ~${target_add}

# Current Menu
{json.dumps(current_menu, ensure_ascii=False, indent=2)}

# Available Candidates for Adding
{json.dumps(candidate_pool[:20], ensure_ascii=False, indent=2)}

# Upsell Strategy (Priority Order)
1. **Quality Upgrade (First Priority):** Can we upgrade a "Small" portion to "Large"? Can we swap a standard dish for a Premium Version (e.g., Fried Rice → Truffle Fried Rice)?
2. **Experience Add-on:** Add Drinks, Desserts, or Appetizers to complete the meal experience.
3. **The "More Food" Trap:** Do NOT add more Main Courses if the dish_count is already sufficient. Only add Mains if clearly needed.
4. **CP Value Check**: If budget has lots of room (< 60% used), prioritize high CP value add-ons (e.g., $200 dessert rather than $800 third main course).

# Output Format (JSON)
{{
  "action": "ADD_DISHES",
  "modifications": [
    {{
      "type": "upgrade/add",
      "dish_name": "String",
      "reason": "String (e.g., 'Upgraded to Large for sharing', 'Added Dessert to complete the meal')"
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
  "new_utilization": Float,
  "justification": "String (Brief explanation of strategy)"
}}
"""
    
    def _build_reduce_prompt(self, current_menu, total, budget_amount, utilization, target_reduce, occasion):
        return f"""
# Role
You are a **Value-First Budget Manager**.

# Current Status
- Total: ${total} (Utilization: {utilization:.1%} - OVER BUDGET)
- Budget: ${budget_amount}
- Overage: ${total - budget_amount}
- Occasion: {occasion}

# Current Menu
{json.dumps(current_menu, ensure_ascii=False, indent=2)}

# Logic: "Soft Limit" vs "Hard Limit"
**Check:** Is the over-budget caused by a **Centerpiece** (tag="主秀" or high-value signature dish) in a **Business/Date/Treat** scenario?
   - **YES:** You are authorized to **KEEP** it if overage is within 20%. Set action as "AUTHORIZED_OVERSPEND".
   - **NO:** Proceed to cut costs.

# Cost Cutting Strategy (if not authorized overspend)
1. **Portion Adjustment**: Reduce quantity (e.g., 4 portions → 2 portions of staple)
2. **Downgrade Portions**: Large → Small/Regular
3. **Remove Non-Essentials**: Remove extra Soups or expensive Sides
4. **Swap**: Replace Premium ingredients with Standard ones (e.g., Grouper → Bass)
5. **Protector Rule**: NEVER remove the #1 Verified Signature Dish (tag="必點")

# Output Format (JSON)
{{
  "action": "REDUCE_COST" or "AUTHORIZED_OVERSPEND",
  "justification": "String (Explain why we kept the expensive dish OR what we cut)",
  "modifications": [
    {{
      "type": "remove/downgrade/reduce_quantity",
      "dish_name": "String",
      "reason": "String"
    }}
  ],
  "updated_menu": [...],
  "new_total": Integer,
  "new_utilization": Float
}}

**CRITICAL**: If authorizing overspend, clearly state the reason (e.g., "Kept Whole Fish as centerpiece for business dinner, overage is acceptable").
"""

class BalanceCheckerAgent(RecommendationAgentBase):
    """
    平衡檢查專家 (Executive Chef)
    
    Enhanced with:
    - Grease control
    - Texture contrast
    - Temperature balance
    - Flavor profile diversity
    """
    
    def _analyze_menu(self, menu: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze menu composition"""
        categories = {}
        cooking_methods = []
        has_fried = 0
        
        for dish in menu:
            cat = dish.get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
            
            dish_name = dish.get('dish_name', '').lower()
            # Detect cooking methods
            if any(word in dish_name for word in ['炸', 'fried', '酥']):
                cooking_methods.append('fried')
                has_fried += 1
            elif any(word in dish_name for word in ['蒸', 'steamed']):
                cooking_methods.append('steamed')
            elif any(word in dish_name for word in ['烤', 'grilled', '燒']):
                cooking_methods.append('grilled')
            elif any(word in dish_name for word in ['炒', 'stir-fry']):
                cooking_methods.append('stir-fried')
        
        greasy_ratio = has_fried / len(menu) if menu else 0
        
        return {
            "categories": categories,
            "dish_count": len(menu),
            "has_vegetable": any('蔬菜' in dish.get('category', '') or '青菜' in dish.get('dish_name', '') for dish in menu),
            "has_soup": any('湯' in dish.get('category', '') for dish in menu),
            "has_staple": any('主食' in dish.get('category', '') or '飯' in dish.get('dish_name', '') or '麵' in dish.get('dish_name', '') for dish in menu),
            "cooking_methods": cooking_methods,
            "greasy_ratio": greasy_ratio
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
            if analysis['greasy_ratio'] > 0.5:
                issues.append("油炸/油膩菜品比例過高（> 50%），建議加入清爽/酸味菜品")
        
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
You are the **"Executive Chef"** checking the menu flow. A menu is not just a list; it is a symphony.

# Current Menu
{json.dumps(current_menu, ensure_ascii=False, indent=2)}

# Current Menu Analysis
{json.dumps(analysis, ensure_ascii=False, indent=2)}

# Identified Issues
{json.dumps(issues, ensure_ascii=False)}

# Balance Rules (The "Chef's Eye")

## 1. The Flavor Balance
* **Grease Control:** If > 50% dishes are Fried/Stir-fry → MUST add Acidic/Pickled/Fresh (e.g., Cucumber Salad, Pickled Vegetables, Citrus-based dish).
* **Texture Contrast:** Ensure mix of Crispy, Soft, Chewy. (Don't order 3 soft tofu-like dishes).

## 2. The Color & Category
* **Visuals:** Is everything Brown/Red? Suggest a Green Vegetable.
* **Category:** Do we have Protein? Veg? Carb? Soup? (Unless "Quick Fix").

## 3. Repetition Check
* **Ingredient:** Avoid repeating main ingredients (e.g., Beef Soup + Beef Stir-fry).
* **Method:** Avoid repeating cooking methods (e.g., 3 Deep Fried items).
* **Sauce/Flavor Profile**: Avoid repeating sauce flavors (e.g., Two "Three-Cup" dishes = too similar).

## 4. Temperature Balance
* **Hot vs Cold**: Ensure temperature contrast (e.g., All hot dishes → suggest adding a cold appetizer or salad).

# Task
Suggest a **SWAP** (Replace X with Y) rather than just adding Z (to preserve budget/quantity).
If adding is necessary, suggest the category/type to add.

# Output Format (JSON)
{{
  "balanced": Boolean,
  "adjustments": [
    {{
      "issue": "String (e.g., 'Too much Grease', 'Repetitive Beef', 'Missing vegetable')",
      "action": "replace/add",
      "target_dish": "String (Dish to remove, if action=replace)",
      "suggestion": "String (Dish category/type to add, e.g., 'Refreshing Cucumber Salad', 'Steamed Vegetable')"
    }}
  ]
}}
"""
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            
            adjustments = data.get("adjustments", [])
            print(f"  Suggested {len(adjustments)} adjustments")
            
            return AgentDecision(
                agent_name="BalanceChecker",
                approved=data.get("balanced", False),
                data=current_menu,
                issues=issues,
                suggestions=[adj.get("suggestion") for adj in adjustments],
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
    品質保證專家 (Restaurant Manager)
    
    Enhanced with:
    - LLM-based semantic checks
    - Social appropriateness validation
    - Price sanity check
    """
    
    async def run(self,
                  final_menu: List[Dict[str, Any]],
                  user_input: UserInputV2,
                  aggregated_data: List[Dict[str, Any]]) -> AgentDecision:
        
        print("✅ QualityAssuranceAgent: Final quality check...")
        
        # Hard checks (code-based)
        hard_checks = self._perform_hard_checks(final_menu, user_input)
        
        # If hard checks fail (e.g., dietary violation), reject immediately
        if hard_checks.get('fatal_error'):
            print(f"❌ FATAL ERROR: {hard_checks.get('critique')}")
            return AgentDecision(
                agent_name="QualityAssurance",
                approved=False,
                data=final_menu,
                issues=["FATAL: " + hard_checks.get('critique')],
                metadata={"checks": hard_checks},
                critique=hard_checks.get('critique')
            )
        
        # Soft checks (LLM-based semantic validation)
        soft_checks = await self._perform_soft_checks(final_menu, user_input)
        
        all_passed = hard_checks['all_passed'] and soft_checks.get('approved', False)
        
        if all_passed:
            print(f"✓ All quality checks passed!")
            return AgentDecision(
                agent_name="QualityAssurance",
                approved=True,
                data=final_menu,
                metadata={"hard_checks": hard_checks, "soft_checks": soft_checks}
            )
        else:
            failed_items = []
            if not hard_checks['all_passed']:
                failed_items.extend([k for k, v in hard_checks.items() if k != 'all_passed' and k != 'fatal_error' and not v])
            if not soft_checks.get('approved'):
                failed_items.append("Semantic check failed")
            
            critique = soft_checks.get('critique', 'Quality checks failed')
            print(f"⚠️  Failed checks: {failed_items}")
            print(f"   Critique: {critique}")
            
            return AgentDecision(
                agent_name="QualityAssurance",
                approved=False,
                data=final_menu,
                issues=failed_items,
                metadata={"hard_checks": hard_checks, "soft_checks": soft_checks},
                critique=critique
            )
    
    def _perform_hard_checks(self, final_menu, user_input) -> Dict[str, Any]:
        """Code-based hard constraint checks"""
        checks = {}
        
        # 1. Has signature dish?
        has_signature = any(dish.get('tag') in ['必點', '招牌', '主秀'] for dish in final_menu)
        checks['has_signature'] = has_signature
        
        # 2. Dietary restrictions respected? (CRITICAL)
        dietary_safe = True
        violation_details = []
        for dish in final_menu:
            dish_name = dish.get('dish_name', '').lower()
            for pref in (user_input.preferences or []):
                if '不吃牛' in pref and ('牛' in dish_name or 'beef' in dish_name):
                    dietary_safe = False
                    violation_details.append(f"Found beef in '{dish.get('dish_name')}' but user has 'No Beef' restriction")
                if '不吃豬' in pref and ('豬' in dish_name or 'pork' in dish_name):
                    dietary_safe = False
                    violation_details.append(f"Found pork in '{dish.get('dish_name')}' but user has 'No Pork' restriction")
                if '素食' in pref and any(meat in dish_name for meat in ['肉', '雞', '魚', '蝦', '牛', '豬']):
                    dietary_safe = False
                    violation_details.append(f"Found meat in '{dish.get('dish_name')}' but user is vegetarian")
        
        checks['dietary_safe'] = dietary_safe
        checks['fatal_error'] = not dietary_safe
        if not dietary_safe:
            checks['critique'] = "Dietary restriction violated: " + "; ".join(violation_details)
        
        # 3. Quantity logic correct?
        quantity_correct = all(dish.get('quantity', 0) > 0 for dish in final_menu)
        checks['quantity_logic'] = quantity_correct
        
        checks['all_passed'] = all([has_signature, dietary_safe, quantity_correct])
        
        return checks
    
    async def _perform_soft_checks(self, final_menu, user_input) -> Dict[str, Any]:
        """LLM-based semantic validation"""
        
        prompt = f"""
# Role
You are the **Restaurant Manager** performing the final inspection before presenting the menu to the guest.

# Context
- Occasion: {user_input.occasion or 'casual'}
- Party Size: {user_input.party_size}
- Dining Style: {user_input.dining_style}
- Budget: {user_input.budget.amount} TWD

# Menu to Inspect
{json.dumps(final_menu, ensure_ascii=False, indent=2)}

# Inspection Checklist

## 1. Social Appropriateness
- Is the menu weird for the occasion? 
  Examples of WEIRD:
  * 4 desserts and 1 meat for a Business Dinner
  * Solo diner ordering a Whole Chicken
  * Date night with 3 garlic-heavy dishes
- If Business/Date: Are there any messy items left? (Shell-on seafood, ribs, etc.)

## 2. Logic Check
- Are "Per Head" items (Rice, Tea, Single Dessert) count reasonable for Party Size?
  * Tolerance: +/- 1 is ok
  * WRONG: 2 rice for 4 people, or 8 desserts for 2 people
- Is the dish count reasonable? (Not too few, not too many)

## 3. Price Sanity Check
- Check for abnormal pricing:
  * Budget $3000 but only ordered $500 worth (too low)
  * Single dish costs $2000 out of $3000 budget (too concentrated)

## 4. Signature Dish Presence
- Is there at least 1 signature/must-order dish?
- If not, this is a WARNING (not fatal, but worth noting)

# Output Format (JSON)
{{
  "approved": Boolean,
  "critique": "String (If rejected, explain exactly what looks weird. If approved, say 'All checks passed.')",
  "warnings": ["String (Non-fatal issues worth noting)"]
}}

**Be strict but fair. If something is genuinely weird from a human perspective, reject it.**
"""
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            return data
            
        except Exception as e:
            print(f"⚠️  Soft check failed: {e}")
            # Fallback: approve if hard checks passed
            return {"approved": True, "critique": "Soft check unavailable, relying on hard checks"}

class OrchestratorAgent:
    """
    協調者 - 管理整個 Multi-Agent 推薦流程
    
    Enhanced with:
    - Feedback loop (critique passing)
    - Early stopping
    - Scoring mechanism for best fallback
    - Adaptive iteration
    """
    
    def __init__(self):
        self.dish_selector = DishSelectorAgent()
        self.budget_optimizer = BudgetOptimizerAgent()
        self.balance_checker = BalanceCheckerAgent()
        self.qa_agent = QualityAssuranceAgent()
    
    def _calculate_menu_score(self, qa_result: AgentDecision, menu: List[Dict], user_input: UserInputV2) -> float:
        """Calculate menu quality score for fallback selection"""
        score = 0.0
        
        # Get checks from metadata
        hard_checks = qa_result.metadata.get('hard_checks', {})
        soft_checks = qa_result.metadata.get('soft_checks', {})
        
        # Critical checks (high weight)
        if hard_checks.get('dietary_safe', False):
            score += 40  # Dietary safety is paramount
        if hard_checks.get('has_signature', False):
            score += 20
        if hard_checks.get('quantity_logic', False):
            score += 10
        
        # Soft checks
        if soft_checks.get('approved', False):
            score += 20
        
        # Budget utilization bonus
        total = sum(dish.get('price', 0) * dish.get('quantity', 1) for dish in menu)
        utilization = total / user_input.budget.amount if user_input.budget.amount > 0 else 0
        if 0.8 <= utilization <= 1.0:
            score += 10
        elif 0.7 <= utilization < 0.8 or 1.0 < utilization <= 1.1:
            score += 5  # Close enough
        
        return score
    
    async def run(self,
                  user_input: UserInputV2,
                  candidates: List[Dict[str, Any]],
                  aggregated_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        
        print("\n" + "="*80)
        print("🤖 Multi-Agent Recommendation System (Enhanced) Starting...")
        print("="*80 + "\n")
        
        max_iterations = 3
        current_menu = []
        previous_critique = None
        best_menu = None
        best_score = 0.0
        
        for iteration in range(max_iterations):
            print(f"\n{'─'*80}")
            print(f"🔄 Iteration {iteration + 1}/{max_iterations}")
            print(f"{'─'*80}\n")
            
            # Step 1: Dish Selection (with feedback loop)
            if iteration == 0 or not current_menu:
                decision = await self.dish_selector.run(
                    candidates, user_input, aggregated_data
                )
            else:
                # Pass previous critique for improvement
                print(f"📝 Applying feedback from previous iteration...")
                decision = await self.dish_selector.run(
                    candidates, user_input, aggregated_data,
                    previous_critique=previous_critique
                )
            
            if not decision.approved:
                print("❌ Dish selection failed, using candidates as fallback")
                current_menu = candidates[:10]
            else:
                current_menu = decision.data
            
            # Step 2: Budget Optimization
            decision = await self.budget_optimizer.run(
                current_menu,
                user_input.budget.amount,
                candidates,
                user_input
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
                # Note: In a full implementation, we could loop back to DishSelector with these suggestions
            
            # Step 4: Quality Assurance
            qa_result = await self.qa_agent.run(current_menu, user_input, aggregated_data)
            
            # Calculate score for this attempt
            score = self._calculate_menu_score(qa_result, current_menu, user_input)
            print(f"📊 Menu Score: {score:.1f}/100")
            
            if score > best_score:
                best_menu = current_menu.copy()
                best_score = score
                print(f"   ⭐ New best menu!")
            
            # Early stopping if approved
            if qa_result.approved:
                print(f"\n{'='*80}")
                print(f"✅ Menu approved in iteration {iteration + 1}! (Score: {score:.1f}/100)")
                print(f"{'='*80}\n")
                return current_menu
            else:
                # Store critique for next iteration
                previous_critique = qa_result.critique
                print(f"⚠️  QA issues: {qa_result.issues}")
                if previous_critique:
                    print(f"💬 Critique: {previous_critique[:150]}...")
        
        # If we exhausted iterations, return best attempt
        print(f"\n{'='*80}")
        print(f"⚠️  Max iterations reached. Returning best attempt.")
        print(f"   Best Score: {best_score:.1f}/100")
        print(f"{'='*80}\n")
        return best_menu or current_menu
