"""
Recommendation Agent - Two-stage recommendation system
Implements Hard Filter (Python) + Soft Ranking (LLM) for dish recommendations
"""

import os
import json
import time
import google.generativeai as genai
from typing import List, Optional, Dict
from schemas.recommendation import UserInputV2, RecommendationResponseV2, DishSlotResponse, MenuItemV2
from schemas.restaurant_profile import RestaurantProfile, MenuItem


class RecommendationService:
    """
    Two-stage recommendation system:
    1. Hard Filter: Python-based filtering on dish attributes
    2. Soft Ranking: LLM-based ranking considering context and preferences
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        genai.configure(api_key=self.api_key)

    async def generate_recommendation(
        self,
        user_input: UserInputV2,
        profile: RestaurantProfile
    ) -> RecommendationResponseV2:
        """
        Generate dish recommendations based on user preferences

        Args:
            user_input: User preferences and constraints
            profile: Restaurant profile with menu items

        Returns:
            RecommendationResponseV2 with recommended dishes
        """
        print(f"[RecommendationService] Generating recommendations for {user_input.party_size} people")
        print(f"[RecommendationService] Dining style: {user_input.dining_style}")
        print(f"[RecommendationService] Preferences: {user_input.preferences}")

        # Step 1: Hard Filter (Python-based)
        filtered_items = self._hard_filter(profile.menu_items, user_input)
        print(f"[RecommendationService] Hard filter: {len(profile.menu_items)} → {len(filtered_items)} items")

        if not filtered_items:
            return RecommendationResponseV2(
                recommendation_id=f"rec_{int(time.time())}",
                restaurant_name=profile.name,
                recommendation_summary="No dishes match your preferences. Please adjust your constraints.",
                items=[],
                total_price=0,
                cuisine_type="中式餐館",
                category_summary={},
                currency="TWD"
            )

        # Step 2: Soft Ranking (LLM-based)
        recommendations = await self._soft_ranking(filtered_items, user_input, profile)

        return recommendations

    def _hard_filter(self, menu_items: List[MenuItem], user_input: UserInputV2) -> List[MenuItem]:
        """
        Hard filter dishes based on binary constraints

        Filters out:
        - Dishes with unwanted attributes (spicy, beef, pork, etc.)
        - Dishes that violate allergen constraints
        - Dishes outside budget range (if specified)

        Args:
            menu_items: All menu items from restaurant
            user_input: User preferences

        Returns:
            Filtered list of menu items
        """
        filtered = []

        for item in menu_items:
            # Skip if no analysis (cannot filter properly)
            if not item.analysis:
                print(f"[HardFilter] Skipping {item.name} - no analysis data")
                continue

            # Check preferences for hard constraints
            skip = False
            for pref in user_input.preferences:
                pref_lower = pref.lower()

                # No spicy constraint
                if pref_lower in ['no_spicy', 'not_spicy', '不辣', '微辣']:
                    if item.analysis.is_spicy:
                        print(f"[HardFilter] Rejected {item.name} - is spicy")
                        skip = True
                        break

                # No beef constraint
                if pref_lower in ['no_beef', '不吃牛', '不要牛肉']:
                    if item.analysis.contains_beef:
                        print(f"[HardFilter] Rejected {item.name} - contains beef")
                        skip = True
                        break

                # No pork constraint
                if pref_lower in ['no_pork', '不吃豬', '不要豬肉']:
                    if item.analysis.contains_pork:
                        print(f"[HardFilter] Rejected {item.name} - contains pork")
                        skip = True
                        break

                # No seafood constraint
                if pref_lower in ['no_seafood', '不吃海鮮', '不要海鮮']:
                    if item.analysis.contains_seafood:
                        print(f"[HardFilter] Rejected {item.name} - contains seafood")
                        skip = True
                        break

                # Vegan constraint
                if pref_lower in ['vegan', '素食', '全素']:
                    if not item.analysis.is_vegan:
                        print(f"[HardFilter] Rejected {item.name} - not vegan")
                        skip = True
                        break

            if skip:
                continue

            # Check allergens
            if user_input.preferences:
                allergen_keywords = ['allergy', 'allergic', '過敏']
                for pref in user_input.preferences:
                    if any(keyword in pref.lower() for keyword in allergen_keywords):
                        # Extract allergen name (e.g., "allergic to peanuts" → "peanuts")
                        allergen = pref.lower().split('to')[-1].strip() if 'to' in pref.lower() else pref
                        if any(allergen in a.lower() for a in item.analysis.allergens):
                            print(f"[HardFilter] Rejected {item.name} - contains allergen: {allergen}")
                            skip = True
                            break

            if skip:
                continue

            # Budget filter (if specified)
            if user_input.budget and user_input.budget.max_per_dish:
                if item.price and item.price > user_input.budget.max_per_dish:
                    print(f"[HardFilter] Rejected {item.name} - price ${item.price} > max ${user_input.budget.max_per_dish}")
                    continue

            # Passed all filters
            filtered.append(item)

        print(f"[HardFilter] Kept {len(filtered)} items after filtering")
        return filtered

    async def _soft_ranking(
        self,
        filtered_items: List[MenuItem],
        user_input: UserInputV2,
        profile: RestaurantProfile
    ) -> RecommendationResponseV2:
        """
        Use LLM to rank and select optimal dishes based on soft constraints

        Considers:
        - Party size and dining style
        - Budget and dish count targets
        - Occasion and natural language preferences
        - Dish diversity and balance
        - Review sentiments and popularity

        Args:
            filtered_items: Items that passed hard filter
            user_input: User preferences
            profile: Full restaurant profile

        Returns:
            RecommendationResponseV2 with ranked recommendations
        """
        print(f"[SoftRanking] Ranking {len(filtered_items)} filtered items")

        # Use fast model for ranking
        generation_config = {
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "OBJECT",
                "properties": {
                    "recommendations": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "dish_name": {"type": "STRING"},
                                "quantity": {"type": "INTEGER"},
                                "reason": {"type": "STRING"},
                                "highlight_note": {"type": "STRING"}
                            },
                            "required": ["dish_name", "quantity", "reason"]
                        }
                    },
                    "reasoning": {"type": "STRING"}
                }
            }
        }

        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            generation_config=generation_config
        )

        # Build menu data for LLM
        menu_data = []
        for item in filtered_items:
            item_dict = {
                "name": item.name,
                "price": item.price,
                "category": item.category,
                "description": item.description,
                "is_popular": item.is_popular,
                "is_risky": item.is_risky,
            }

            # Add AI insights if available
            if item.ai_insight:
                item_dict["review_sentiment"] = item.ai_insight.sentiment
                item_dict["review_summary"] = item.ai_insight.summary
                item_dict["mention_count"] = item.ai_insight.mention_count

            # Add dish attributes if available
            if item.analysis:
                item_dict["attributes"] = {
                    "flavors": item.analysis.flavors,
                    "textures": item.analysis.textures,
                    "temperature": item.analysis.temperature,
                    "cooking_method": item.analysis.cooking_method,
                    "suitable_occasions": item.analysis.suitable_occasions,
                    "is_signature": item.analysis.is_signature,
                    "sentiment_score": item.analysis.sentiment_score,
                    "highlight_review": item.analysis.highlight_review
                }

            menu_data.append(item_dict)

        # Calculate target dish count
        if user_input.dish_count_target:
            target_count = user_input.dish_count_target
        else:
            # Heuristic: 1.5-2 dishes per person for shared, 1 per person for individual
            if user_input.dining_style == "Shared":
                target_count = max(3, int(user_input.party_size * 1.5))
            else:
                target_count = user_input.party_size

        # Build LLM prompt
        prompt = f"""
你是一個專業的餐廳點餐顧問。請根據用餐需求，從以下菜單中挑選最合適的菜色組合。

## 用餐資訊
- 餐廳：{profile.name}
- 人數：{user_input.party_size} 人
- 用餐方式：{user_input.dining_style} (Shared=合菜共享, Individual=各點各的)
- 目標菜色數：{target_count} 道

## 預算限制
{self._format_budget(user_input.budget)}

## 用餐偏好
{self._format_preferences(user_input)}

## 可選菜單（已過濾不符合硬性限制的菜色）
{json.dumps(menu_data, ensure_ascii=False, indent=2)}

## 推薦原則
1. **多樣性**：選擇不同類別、烹飪方式、口味的菜色
2. **平衡性**：
   - 共享式：考慮冷熱、葷素、主食配菜的平衡
   - 個人式：每人推薦 1 道主菜
3. **價格控制**：符合預算限制
4. **評價優先**：優先選擇 is_popular=true 或 sentiment_score 高的菜色
5. **場合適配**：{user_input.occasion or "一般聚餐"}

請分析並挑選菜色。
"""

        try:
            response = await model.generate_content_async(prompt)
            result_text = response.text

            # Parse JSON (no need to clean markdown code blocks as response is pure JSON)
            result = json.loads(result_text)

            # Build response
            recommendations = []
            total_price = 0

            for rec_data in result.get("recommendations", []):
                dish_name = rec_data.get("dish_name")

                # Find corresponding MenuItem (simple exact match for now, could be improved)
                menu_item = next((item for item in filtered_items if item.name == dish_name), None)
                
                # If exact match fails, try partial match
                if not menu_item:
                    menu_item = next((item for item in filtered_items if dish_name in item.name or item.name in dish_name), None)

                if not menu_item:
                    print(f"[SoftRanking] Warning: LLM recommended unknown dish: {dish_name}")
                    continue

                quantity = rec_data.get("quantity", 1)
                reason = rec_data.get("reason", "Recommended based on preferences")

                # Convert to MenuItemV2 format
                # Note: MenuItemV2 requires dish_name, price, quantity, reason, category
                menu_item_v2 = MenuItemV2(
                    dish_id=menu_item.id or "",
                    dish_name=menu_item.name,
                    price=menu_item.price or 0,
                    quantity=quantity,
                    reason=reason,
                    category=menu_item.category or "其他",
                    review_count=menu_item.ai_insight.mention_count if menu_item.ai_insight else 0
                )

                dish_slot = DishSlotResponse(
                    category=menu_item.category or "其他",
                    display=menu_item_v2,
                    alternatives=[] # Alternatives can be populated later if needed
                )

                recommendations.append(dish_slot)

                if menu_item.price:
                    total_price += menu_item.price * quantity

            overall_reasoning = result.get("reasoning", "Recommendations based on your preferences and restaurant reviews.")

            print(f"[SoftRanking] Generated {len(recommendations)} recommendations, total ${total_price}")

            # Calculate category summary
            category_summary = {}
            for item in recommendations:
                cat = item.category
                category_summary[cat] = category_summary.get(cat, 0) + 1

            return RecommendationResponseV2(
                recommendation_id=f"rec_{int(time.time())}",
                restaurant_name=profile.name,
                recommendation_summary=overall_reasoning,
                items=recommendations,
                total_price=total_price,
                cuisine_type="中式餐館",  # Default, should be inferred or passed
                category_summary=category_summary,
                currency="TWD"
            )

        except json.JSONDecodeError as e:
            print(f"[SoftRanking] JSON parsing error: {e}")
            if 'result_text' in locals():
                print(f"[SoftRanking] Raw response: {result_text[:500]}")
            return self._fallback_ranking(filtered_items, user_input, profile)
        except Exception as e:
            print(f"[SoftRanking] Error during ranking: {e}")
            import traceback
            traceback.print_exc()
            return self._fallback_ranking(filtered_items, user_input, profile)

    def _format_budget(self, budget) -> str:
        """Format budget information for LLM prompt"""
        if not budget:
            return "無特別預算限制"

        lines = []
        if budget.type == "Total" and budget.amount:
             lines.append(f"- 總預算：${budget.amount}")
        elif budget.type == "Per_Person" and budget.amount:
             lines.append(f"- 每人預算：${budget.amount}")
        
        return "\n".join(lines) if lines else "無特別預算限制"

    def _format_preferences(self, user_input: UserInputV2) -> str:
        """Format user preferences for LLM prompt"""
        lines = []

        if user_input.preferences:
            lines.append("明確偏好：")
            for pref in user_input.preferences:
                lines.append(f"- {pref}")

        if user_input.natural_input:
            lines.append(f"\n自然語言需求：\n{user_input.natural_input}")

        if user_input.occasion:
            lines.append(f"\n用餐場合：{user_input.occasion}")

        return "\n".join(lines) if lines else "無特別偏好"

    def _fallback_ranking(self, filtered_items: List[MenuItem], user_input: UserInputV2, profile: RestaurantProfile) -> RecommendationResponseV2:
        """
        Fallback ranking when LLM fails
        Uses simple heuristics: prioritize popular and high-sentiment dishes
        """
        print(f"[SoftRanking] Using fallback ranking")

        # Sort by popularity and sentiment
        def score_item(item: MenuItem) -> float:
            score = 0.0

            # Popular dishes get bonus
            if item.is_popular:
                score += 10.0

            # Sentiment score bonus
            if item.analysis and item.analysis.sentiment_score:
                score += item.analysis.sentiment_score * 5.0

            # Positive AI insight bonus
            if item.ai_insight:
                if item.ai_insight.sentiment == "positive":
                    score += 3.0
                elif item.ai_insight.sentiment == "negative":
                    score -= 5.0

                # Mention count bonus
                score += min(item.ai_insight.mention_count, 5) * 0.5

            # Risky dishes get penalty
            if item.is_risky:
                score -= 10.0

            return score

        sorted_items = sorted(filtered_items, key=score_item, reverse=True)

        # Calculate target count
        if user_input.dish_count_target:
            target_count = user_input.dish_count_target
        else:
            if user_input.dining_style == "Shared":
                target_count = max(3, int(user_input.party_size * 1.5))
            else:
                target_count = user_input.party_size

        # Select top items
        selected_items = sorted_items[:target_count]
        
        recommendations = []
        total_price = 0
        category_summary = {}

        for item in selected_items:
            menu_item_v2 = MenuItemV2(
                dish_id=item.id or "",
                dish_name=item.name,
                price=item.price or 0,
                quantity=1,
                reason="Popular and highly rated",
                category=item.category or "其他",
                review_count=item.ai_insight.mention_count if item.ai_insight else 0
            )
            
            dish_slot = DishSlotResponse(
                category=item.category or "其他",
                display=menu_item_v2,
                alternatives=[]
            )
            
            recommendations.append(dish_slot)
            if item.price:
                total_price += item.price
            
            cat = item.category or "其他"
            category_summary[cat] = category_summary.get(cat, 0) + 1

        return RecommendationResponseV2(
            recommendation_id=f"rec_{int(time.time())}",
            restaurant_name=profile.name,
            recommendation_summary="Fallback recommendations based on popularity.",
            items=recommendations,
            total_price=total_price,
            cuisine_type="中式餐館",
            category_summary=category_summary,
            currency="TWD"
        )


    def get_alternatives(
        self,
        category: str,
        exclude_names: List[str],
        profile: RestaurantProfile,
        limit: int = 5
    ) -> List[MenuItemV2]:
        """
        Get alternative dishes for a specific category
        """
        candidates = []
        for item in profile.menu_items:
            # Filter by category
            if item.category != category:
                continue
            
            # Filter excluded items
            if item.name in exclude_names:
                continue
                
            candidates.append(item)
            
        # Sort candidates by score (popularity + sentiment)
        def score_item(item: MenuItem) -> float:
            score = 0.0
            if item.is_popular: score += 10.0
            if item.analysis and item.analysis.sentiment_score:
                score += item.analysis.sentiment_score * 5.0
            if item.is_risky: score -= 10.0
            return score
            
        sorted_candidates = sorted(candidates, key=score_item, reverse=True)
        
        # Convert top candidates to MenuItemV2
        results = []
        for item in sorted_candidates[:limit]:
            menu_item_v2 = MenuItemV2(
                dish_id=item.id or "",
                dish_name=item.name,
                price=item.price,
                category=item.category,
                description=item.description,
                quantity=1,
                reason="Alternative option",
                review_count=item.ai_insight.mention_count if item.ai_insight else 0
            )
            results.append(menu_item_v2)
            
        return results
