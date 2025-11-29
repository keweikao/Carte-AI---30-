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

    def __init__(self):
        super().__init__(model_name='gemini-2.5-pro')

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
You are the **"Culinary Experience Curator."** You are not an accountant; you are a gastronome. Your goal is to maximize **Flavor** and **Experience**.

# Language Requirement
**IMPORTANT:** The user's preferred language is **{user_input.language}**.
- You MUST output `dish_name` exactly as it appears in the menu (usually Traditional Chinese).
- You MUST output `reason` and `rationale` in **{user_input.language}**.
- If `language` is "繁體中文" or "zh-TW", use Traditional Chinese for all explanations.

# ⚠️ CRITICAL FEEDBACK FROM PREVIOUS ATTEMPT
{critique_section}
*Instruction:* If feedback exists, you MUST adjust your selection logic to fix the reported issues. (e.g., "Add more food", "Remove spicy items").

# User Context
- Party Size: {user_input.party_size} (N people)
- Occasion: {user_input.occasion or 'casual'}
- Dining Goal: {user_input.occasion or 'General Dining'}
- Dietary Restrictions: {', '.join(user_input.preferences) if user_input.preferences else 'None'} (STRICT FILTER)
- User Note: "{user_note}" (Highest Priority Override)

# Data Sources
- Verified Signatures: {verified_dishes} (Must prioritize these)
- Candidate Pool: {json.dumps(candidates[:30], ensure_ascii=False, indent=2, default=str)}

# Decision Logic (The Protocol)

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
4.  **Dietary Filter:** Strictly remove items violating restrictions.

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
            "has_vegetable": any(
                '蔬菜' in dish.get(
                    'category',
                    '') or '青菜' in dish.get(
                    'dish_name',
                    '') for dish in menu),
            "has_soup": any(
                '湯' in dish.get(
                    'category',
                    '') for dish in menu),
            "has_staple": any(
                '主食' in dish.get(
                    'category',
                    '') or '飯' in dish.get(
                    'dish_name',
                    '') or '麵' in dish.get(
                    'dish_name',
                    '') for dish in menu),
            "cooking_methods": cooking_methods,
            "greasy_ratio": greasy_ratio}

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
{json.dumps(current_menu, ensure_ascii=False, indent=2, default=str)}

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

        all_passed = hard_checks['all_passed'] and soft_checks.get(
            'approved', False)

        if all_passed:
            print(f"✓ All quality checks passed!")
            return AgentDecision(
                agent_name="QualityAssurance",
                approved=True,
                data=final_menu,
                metadata={
                    "hard_checks": hard_checks,
                    "soft_checks": soft_checks})
        else:
            failed_items = []
            if not hard_checks['all_passed']:
                failed_items.extend([k for k, v in hard_checks.items(
                ) if k != 'all_passed' and k != 'fatal_error' and not v])
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
                metadata={
                    "hard_checks": hard_checks,
                    "soft_checks": soft_checks},
                critique=critique)

    def _perform_hard_checks(self, final_menu, user_input) -> Dict[str, Any]:
        """Code-based hard constraint checks"""
        checks = {}

        # 1. Has signature dish?
        has_signature = any(
            dish.get('tag') in [
                '必點',
                '招牌',
                '主秀'] for dish in final_menu)
        checks['has_signature'] = has_signature

        # 2. Dietary restrictions respected? (CRITICAL)
        dietary_safe = True
        violation_details = []
        for dish in final_menu:
            dish_name = dish.get('dish_name', '').lower()
            for pref in (user_input.preferences or []):
                if '不吃牛' in pref and ('牛' in dish_name or 'beef' in dish_name):
                    dietary_safe = False
                    violation_details.append(
                        f"Found beef in '{dish.get('dish_name')}' but user has 'No Beef' restriction")
                if '不吃豬' in pref and ('豬' in dish_name or 'pork' in dish_name):
                    dietary_safe = False
                    violation_details.append(
                        f"Found pork in '{dish.get('dish_name')}' but user has 'No Pork' restriction")
                if '素食' in pref and any(
                    meat in dish_name for meat in [
                        '肉', '雞', '魚', '蝦', '牛', '豬']):
                    dietary_safe = False
                    violation_details.append(
                        f"Found meat in '{dish.get('dish_name')}' but user is vegetarian")

        checks['dietary_safe'] = dietary_safe
        checks['fatal_error'] = not dietary_safe
        if not dietary_safe:
            checks['critique'] = "Dietary restriction violated: " + \
                "; ".join(violation_details)

        # 3. Quantity logic correct?
        quantity_correct = all(dish.get('quantity', 0) >
                               0 for dish in final_menu)
        checks['quantity_logic'] = quantity_correct

        checks['all_passed'] = all(
            [has_signature, dietary_safe, quantity_correct])

        return checks

    async def _perform_soft_checks(self, final_menu, user_input) -> Dict[str, Any]:
        """LLM-based semantic validation"""

        prompt = f"""
# Role
You are the **"Restaurant Manager"** performing the final sanity check before presenting the menu to the guest.

# Context
- Scenario: {user_input.occasion or 'casual'} ({user_input.occasion or 'General Dining'})
- Party Size: {user_input.party_size}
- Menu: {json.dumps(final_menu, ensure_ascii=False, indent=2, default=str)}

# Inspection Checklist (Strict)
1.  **Logic Check (The "Per Head" Rule):**
    - Are "Unit-based items" (Rice, Tea, Single Dessert, Oysters) equal to Party Size?
    - *Tolerance:* +/- 1 is acceptable for sharing, but "2 desserts for 4 people" is REJECTED.
2.  **Social Appropriateness:**
    - If "Business": Is the menu too cheap/simple? Is there a Centerpiece? Are there messy items (Ribs)?
    - If "Solo": Is there too much food?
3.  **Constraint Validation:**
    - Double check Dietary Restrictions (e.g., "No Beef" but "Beef Soup" is present) -> FATAL ERROR.
4.  **Over-ordering Check (Gluttony Protocol):**
    - IF `occasion` == 'all_signatures': Allow more dishes (up to N+4).
    - ELSE: If dish count > N + 3, issue a WARNING (but do not reject unless absurd).

# Output Format (JSON)
{{
  "approved": Boolean,
  "critique": "String (If rejected, explain EXACTLY what to fix. This will be sent to the DishSelector. e.g., 'Rejected because desserts are insufficient for 4 people.')",
  "fatal_error": Boolean,
  "warning": "String (Optional warning for frontend display, e.g., 'This menu is quite large for 2 people.')"
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
            return {
                "approved": True,
                "critique": "Soft check unavailable, relying on hard checks"}

    async def consolidate(self,
                          base_menu: List[Dict[str, Any]],
                          balance_decision: AgentDecision,
                          user_input: UserInputV2) -> AgentDecision:
        """
        Consolidates feedback from Balance agent to produce the final menu.
        This is the 'Aggregator' role.
        """
        print("✅ QualityAssuranceAgent: Consolidating feedback...")

        balance_feedback = "None"
        if not balance_decision.approved:
            balance_feedback = f"Issues: {balance_decision.issues}. Suggestions: {balance_decision.suggestions}"

        # If approved, just return base menu
        if balance_decision.approved:
            print("   Balance approved. Returning menu.")
            return AgentDecision(
                agent_name="QualityAssurance",
                approved=True,
                data=base_menu,
                metadata={"source": "auto-approval"}
            )

        prompt = f"""
# Role
You are the **"Final Decision Maker"** (Restaurant Manager).
You have received a draft menu and feedback from the Executive Chef (Balance).

# Inputs
- **Original Draft:** {json.dumps(base_menu, ensure_ascii=False, indent=2, default=str)}
- **Balance Feedback:** {balance_feedback}

# User Context
- Party Size: {user_input.party_size}
- Occasion: {user_input.occasion}

# Task
Synthesize a **FINAL MENU** that resolves conflicts.
- If Balance added a dish, ensure it fits the flow.
- **Priority:** Dietary Restrictions > Balance > Flavor.

# Output Format (JSON)
{{
  "final_menu": [
    {{
      "dish_name": "String",
      "price": Integer,
      "quantity": Integer,
      "category": "String",
      "tag": "String",
      "reason": "String"
    }}
  ],
  "resolution_notes": "String (Explain how you resolved the conflict)"
}}
"""
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            final_menu = data.get("final_menu", base_menu)

            # Final sanity check (hard checks only)
            hard_checks = self._perform_hard_checks(final_menu, user_input)
            if hard_checks.get('fatal_error'):
                print(
                    f"❌ Final consolidation failed fatal check: {hard_checks.get('critique')}")
                return AgentDecision(
                    agent_name="QualityAssurance",
                    approved=False,
                    data=final_menu,
                    issues=[hard_checks.get('critique')],
                    critique=hard_checks.get('critique')
                )

            return AgentDecision(
                agent_name="QualityAssurance",
                approved=True,
                data=final_menu,
                metadata={"resolution": data.get("resolution_notes")}
            )

        except Exception as e:
            print(f"❌ Consolidation failed: {e}")
            return AgentDecision(
                agent_name="QualityAssurance",
                approved=False,
                data=base_menu,
                issues=[str(e)]
            )


class OrchestratorAgent:
    """
    協調者 - 管理整個 Multi-Agent 推薦流程

    Enhanced with:
    - Feedback loop (critique passing)
    - Early stopping
    - Scoring mechanism for best fallback
    - Adaptive iteration
    - Speculative Parallelism (Strategy 4)
    """

    def __init__(self):
        self.dish_selector = DishSelectorAgent()
        # self.budget_optimizer = BudgetOptimizerAgent() # Removed
        self.balance_checker = BalanceCheckerAgent()
        self.qa_agent = QualityAssuranceAgent()

    def _calculate_menu_score(
            self,
            qa_result: AgentDecision,
            menu: List[Dict],
            user_input: UserInputV2) -> float:
        """Calculate menu quality score for fallback selection"""
        score = 0.0

        # Get checks from metadata
        hard_checks = qa_result.metadata.get('hard_checks', {})
        soft_checks = qa_result.metadata.get('soft_checks', {})

        # Critical checks (high weight)
        if hard_checks.get('dietary_safe', False):
            score += 50  # Dietary safety is paramount (increased from 40)
        else:
            # Fatal error, return very low score
            return 0.0

        if hard_checks.get('quantity_logic', False):
            score += 15  # Increased from 10

        # Soft checks (increased weight)
        if soft_checks.get('approved', False):
            score += 25  # Increased from 20

        # Budget utilization bonus (increased)
        # total = sum((dish.get('price') or 0) * dish.get('quantity', 1)
        #             for dish in menu)
        # utilization = total / user_input.budget.amount if user_input.budget.amount > 0 else 0
        # if 0.8 <= utilization <= 1.0:
        #     score += 15  # Increased from 10
        # elif 0.7 <= utilization < 0.8 or 1.0 < utilization <= 1.1:
        #     score += 10  # Increased from 5
        # elif utilization > 0:
        #     score += 5  # Any budget usage gets some points
        
        # Bonus: has signature dish (but not required)
        if hard_checks.get('has_signature', False):
            score += 5  # Bonus points, not critical

        return score

    async def run(self,
                  user_input: UserInputV2,
                  candidates: List[Dict[str, Any]],
                  aggregated_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        print("\n" + "=" * 80)
        print("🤖 Multi-Agent Recommendation System (Parallel) Starting...")
        print("=" * 80 + "\n")

        max_iterations = 2  # Reduced from 3 for speed
        current_menu = []
        previous_critique = None
        best_menu = None
        best_score = 0.0
        target_score = 80.0  # Target score for early stopping

        for iteration in range(max_iterations):
            print(f"\n{'─'*80}")
            print(f"🔄 Iteration {iteration + 1}/{max_iterations}")
            print(f"{'─'*80}\n")

            # Step 1: Dish Selection (Serial)
            if iteration == 0 or not current_menu:
                decision = await self.dish_selector.run(
                    candidates, user_input, aggregated_data
                )
            else:
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

            # Step 2: Speculative Parallelism (Balance only now)
            print("⚡️ Running Balance Agent...")
            
            # budget_task = asyncio.create_task(self.budget_optimizer.run(
            #     current_menu,
            #     user_input.budget.amount,
            #     candidates,
            #     user_input
            # ))
            
            balance_task = asyncio.create_task(self.balance_checker.run(
                current_menu,
                user_input.dining_style,
                user_input.party_size
            ))
            
            # budget_decision, balance_decision = await asyncio.gather(budget_task, balance_task)
            balance_decision = await balance_task
            
            # Step 3: Consolidation (QA)
            qa_result = await self.qa_agent.consolidate(
                current_menu,
                balance_decision,
                user_input
            )

            # Check result
            final_menu = qa_result.data

            # Only run full QA check on final iteration or if consolidation failed
            # This saves time by avoiding redundant checks
            if not qa_result.approved or iteration == max_iterations - 1:
                qa_check_result = await self.qa_agent.run(final_menu, user_input, aggregated_data)
            else:
                # Use consolidation result for approved menus
                qa_check_result = qa_result

            score = self._calculate_menu_score(
                qa_check_result, final_menu, user_input)

            print(f"📊 Menu Score: {score:.1f}/100")

            if score > best_score:
                best_menu = final_menu.copy()
                best_score = score
                print(f"   ⭐ New best menu!")

            # Early stopping: if score >= target, return immediately
            if score >= target_score:
                print(f"\n{'='*80}")
                print(
                    f"🎯 Target score reached in iteration {iteration + 1}! (Score: {score:.1f}/100)")
                print(f"{'='*80}\n")
                return final_menu

            # Also stop if both QA checks approved (even if score < 80)
            if qa_result.approved and qa_check_result.approved:
                print(f"\n{'='*80}")
                print(
                    f"✅ Menu approved in iteration {iteration + 1}! (Score: {score:.1f}/100)")
                print(f"{'='*80}\n")
                return final_menu
            else:
                previous_critique = qa_check_result.critique or qa_result.critique
                print(f"⚠️  Issues: {qa_check_result.issues}")
                if previous_critique:
                    print(f"💬 Critique: {previous_critique[:150]}...")

        print(f"\n{'='*80}")
        print(f"⚠️  Max iterations reached. Returning best attempt.")
        print(f"   Best Score: {best_score:.1f}/100")
        print(f"{'='*80}\n")
        return best_menu or current_menu
