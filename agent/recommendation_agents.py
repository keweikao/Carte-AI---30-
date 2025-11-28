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
        
        # NEW: Fetch enriched personal memory (includes restaurant history)
        memory_context = ""
        user_id = getattr(user_input, 'user_id', None)
        if user_id:
            try:
                from agent.memory_agent import MemoryAgent
                memory_agent = MemoryAgent()
                memory_context = await memory_agent.get_enriched_memory_context(
                    user_id=user_id,
                    occasion=user_input.occasion,
                    restaurant_name=user_input.restaurant_name
                )
                if memory_context:
                    print(f"  📚 Loaded enriched memory for user {user_id}")
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
You are the **"Menu Architect,"** an expert dining concierge. Your goal is to curate the INITIAL menu draft.

# ⚠️ CRITICAL FEEDBACK FROM PREVIOUS ATTEMPT
{critique_section}
*Instruction:* If feedback exists, you MUST adjust your selection logic to fix the reported issues. (e.g., "Add more food", "Remove spicy items").

# User Context
- Party Size: {user_input.party_size}
- Occasion: {user_input.occasion or 'casual'}
- Dining Goal: {user_input.occasion or 'General Dining'}
- Dietary Restrictions: {', '.join(user_input.preferences) if user_input.preferences else 'None'} (STRICT FILTER)
- User Note: "{user_note}" (Highest Priority Override)

# Data Sources
- Verified Signatures: {verified_dishes} (Must prioritize these)
- Candidate Pool: {json.dumps(candidates[:30], ensure_ascii=False, indent=2)}

# Decision Logic (The Protocol)
1.  **Dietary Filter:** Strictly remove items violating restrictions.
2.  **Goal Alignment:**
    * *Quick Fix:* Focus on Sets/Rice Bowls.
    * *Treat Yourself:* Focus on Premium ingredients (Wagyu/Seafood).
    * *Business:* Must include a "Centerpiece" (Whole fish/Steak). No messy food.
    * *Date:* No garlic, no bones, no mess.
3.  **Quantity Rule:** Target N+1 dishes for sharing (N = Party Size).

# Output Format (JSON)
{{
  "selected_dishes": [
    {{
      "dish_name": "String",
      "price": Integer,
      "quantity": Integer,
      "category": "String",
      "tag": "Signature/Centerpiece/Hidden Gem/Standard",
      "reason": "String (Why this specific dish for this specific User Context?)"
    }}
  ],
  "rationale": "String (Brief strategy explanation)"
}}
"""
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            
            selected = data.get("selected_dishes", [])
            rationale = data.get("rationale", "")
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
        
        occasion = user_input.occasion or 'casual'
        
        # Refactored to use a single prompt for all budget scenarios
        prompt = f"""
# Role
You are the **"Value-First Budget Manager."** Your goal is to optimize the menu to fit the budget while maximizing dining experience value.

# Current Status
- Current Menu: {json.dumps(current_menu, ensure_ascii=False, indent=2)}
- Current Menu Total: ${total}
- Target Budget: ${budget_amount}
- Utilization: {utilization * 100:.1f}%
- Occasion: {occasion}
- Party Size: {user_input.party_size}

# Optimization Strategy

## If Under Budget (< 80% utilization): UPSELL.
1.  **Upgrade Portions:** Change "Small" to "Large" for shared dishes.
2.  **Add Experience:** Add Appetizers, Desserts, or a Pitcher of Drink.
3.  **Premium Swap:** Swap a standard dish for a Premium version (e.g., Regular Fried Rice -> Truffle Fried Rice).
4.  **Prioritize:** Add dishes that enhance the occasion (e.g., a centerpiece for Business).

## If Over Budget (> 100% utilization): SMART CUT.
1.  **Authorized Overspend:** If Occasion is "Business" or "Treat Yourself" AND the overage is caused by a Signature Centerpiece (e.g., Whole Fish), you are authorized to **KEEP IT** (Authorized Overspend up to 120% of budget).
2.  **Downgrade:** Large -> Small portions.
3.  **Trim:** Remove extra Soups or expensive Sides.
4.  **Protection:** NEVER remove the #1 Verified Signature Dish or dishes crucial for dietary restrictions.

## If Optimal Budget (80-100% utilization): NO ACTION.
- If utilization is already between 80% and 100%, no changes are needed unless there's a specific instruction to improve value.

# Output Format (JSON)
{{
  "action": "ADD_DISHES" / "REDUCE_COST" / "AUTHORIZED_OVERSPEND" / "NO_ACTION",
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
      "price": Integer,
      "quantity": Integer,
      "category": "String",
      "tag": "String",
      "reason": "String"
    }}
  ],
  "final_adjustment_note": "String (Explain the overall budget strategy and outcome)"
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
            # Recalculate total
            new_total = sum(d.get('price', 0) * d.get('quantity', 1) for d in updated_menu)
            new_util = new_total / budget_amount if budget_amount > 0 else 0
            
            action_taken = data.get("action", "NO_ACTION")
            justification = data.get("final_adjustment_note", "")
            
            print(f"✓ Action: {action_taken}")
            print(f"  New Total: ${new_total} ({new_util:.1%})")
            
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
You are the **"Executive Chef"** responsible for Menu Flow & Harmony.

# Current Menu
{json.dumps(current_menu, ensure_ascii=False, indent=2)}

# Balance Rules (The Chef's Eye)
1.  **Grease Control:** If > 50% of dishes are Deep Fried/Stir-fry -> MUST add an Acidic/Pickled/Fresh dish (e.g., Cucumber salad, Tea).
2.  **Texture Contrast:** Ensure a mix of Crispy, Soft, and Chewy.
3.  **Color check:** Is everything Brown/Red? Suggest a Green Vegetable.
4.  **Repetition:** Do not repeat the main ingredient (e.g., Beef Soup + Beef Stir-fry).

# Task
If balance is poor, suggest a **SWAP** (Replace X with Y) to fix the issue without breaking the budget/quantity.

# Output Format (JSON)
{{
  "is_balanced": Boolean,
  "adjustments": [
    {{
      "issue": "String (e.g., Too much fried food)",
      "action": "replace",
      "target_dish": "String (Dish to remove)",
      "suggestion": "String (Dish category/name to add, e.g., 'Refreshing Salad')"
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
                approved=data.get("is_balanced", False),
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
You are the **"Restaurant Manager"** performing the final sanity check before presenting the menu to the guest.

# Context
- Scenario: {user_input.occasion or 'casual'} ({user_input.occasion or 'General Dining'})
- Party Size: {user_input.party_size}
- Menu: {json.dumps(final_menu, ensure_ascii=False, indent=2)}

# Inspection Checklist (Strict)
1.  **Logic Check (The "Per Head" Rule):**
    - Are "Unit-based items" (Rice, Tea, Single Dessert, Oysters) equal to Party Size?
    - *Tolerance:* +/- 1 is acceptable for sharing, but "2 desserts for 4 people" is REJECTED.
2.  **Social Appropriateness:**
    - If "Business": Is the menu too cheap/simple? Is there a Centerpiece? Are there messy items (Ribs)?
    - If "Solo": Is there too much food?
3.  **Constraint Validation:**
    - Double check Dietary Restrictions (e.g., "No Beef" but "Beef Soup" is present) -> FATAL ERROR.

# Output Format (JSON)
{{
  "approved": Boolean,
  "critique": "String (If rejected, explain EXACTLY what to fix. This will be sent to the DishSelector. e.g., 'Rejected because desserts are insufficient for 4 people.')",
  "fatal_error": Boolean
}}
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
