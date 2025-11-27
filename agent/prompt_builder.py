from schemas.recommendation import UserInputV2, MenuItemV2
import json

def create_prompt_for_gemini_v2(user_input: UserInputV2, menu_data: str, reviews_data: str, user_profile: dict = None) -> str:
    """
    Generates a structured prompt for Gemini to produce a large candidate pool of dishes.
    The backend will then process this pool into DishSlots with alternatives.
    """
    
    # Define a simplified schema for the LLM to generate a large candidate pool
    simplified_schema = {
        "type": "object",
        "properties": {
            "cuisine_type": {
                "type": "string",
                "description": "The detected cuisine type of the restaurant.",
                "enum": ["中式餐館", "日本料理", "美式餐廳", "義式料理", "泰式料理"]
            },
            "menu_items": {
                "type": "array",
                "description": "A list of 20-25 diverse and high-quality dish recommendations.",
                "items": MenuItemV2.model_json_schema()
            }
        },
        "required": ["cuisine_type", "menu_items"]
    }
    output_schema = json.dumps(simplified_schema, indent=2, ensure_ascii=False)
    
    # User preferences from profile
    past_preferences = ""
    if user_profile and user_profile.get("feedback_history"):
        history = user_profile.get("feedback_history", [])
        past_preferences = f"\n- User's Past Feedback History: {json.dumps(history[:3], ensure_ascii=False)}"

    # Construct the user input section for the prompt
    user_input_str = f"""
# User Input
- Dining_Style: "{user_input.dining_style}"
- Party_Size: {user_input.party_size}
- Budget: {{ "Type": "{user_input.budget.type}", "Amount": {user_input.budget.amount} }}
- Dish_Count_Target: {user_input.dish_count_target or "null (AI to decide)"}
- Preferences: {json.dumps(user_input.preferences, ensure_ascii=False)}
- Natural_Input: "{user_input.natural_input or 'None'}"
- Occasion: "{user_input.occasion or 'None'}"
{past_preferences}
"""

    # Occasion Logic
    occasion_instructions = ""
    if user_input.occasion == "business":
        occasion_instructions = """
- **Business Occasion**:
  - **Prioritize**: Safe, universally acceptable dishes. Focus on "easy to eat" items (no messy shells, bones, or hand-held foods).
  - **Avoid**: Extremely spicy, garlic-heavy, or messy dishes.
  - **Atmosphere**: Suggest dishes that convey a sense of quality and respect.
"""
    elif user_input.occasion == "date":
        occasion_instructions = """
- **Date/Anniversary**:
  - **Prioritize**: Dishes with beautiful presentation, "Instagrammable" items, and desserts.
  - **Atmosphere**: Romantic, high-quality ingredients.
  - **Avoid**: Messy foods (e.g., whole crab, ribs) unless they are a specialty.
"""
    elif user_input.occasion == "family":
        occasion_instructions = """
- **Family Gathering**:
  - **Prioritize**: Shareable large plates, dishes suitable for all ages (kids/elderly).
  - **Balance**: Ensure a mix of meat, vegetables, and soup.
"""
    elif user_input.occasion == "fitness":
        occasion_instructions = """
- **Fitness/Health**:
  - **Prioritize**: High protein (lean meat, seafood), low carb, high fiber (vegetables).
  - **Avoid**: Deep-fried items, heavy sauces, sugary drinks/desserts.
  - **Note**: Mention estimated protein/calories in the reason if possible.
"""
    elif user_input.occasion == "friends":
        occasion_instructions = """
- **Friends Gathering**:
  - **Prioritize**: High CP value, spicy/flavorful dishes, "beer food" (下酒菜).
  - **Vibe**: Fun, shareable, adventurous.
"""

    system_prompt = f"""
# Role
You are an expert AI Dining Consultant. Your goal is to provide the best dining recommendation 
based on the restaurant's menu, reviews, and the user's specific needs.

# Input Data Format
You will receive the following data:
1.  **User_Input**: A JSON object detailing the user's request.
2.  **Menu_Data**: A string containing the restaurant's menu.
3.  **Reviews_Data**: A string containing user reviews.

# Core Logic & Constraints

## 0. Cuisine Type Detection & Categorization (MANDATORY FIRST STEP)
... (omitted for brevity, keep existing logic) ...

## 1. Pre-processing and Filtering (Hard Bans)
- **Exclude Plain Staples**: Do NOT recommend plain white rice (白飯/米飯), plain noodles (白麵), or water as a standalone "dish" unless it is a specialty (e.g., "Truffle Risotto" or "Signature Fried Rice" is OK). Plain rice is assumed to be ordered separately or included.
- **Natural Input Priority**: If the `Natural_Input` conflicts with `Preferences` buttons, `Natural_Input` takes higher priority.
- **Absolute Prohibitions**:
  - If "No_Beef" in `Preferences`: Exclude all beef dishes.
  - If "No_Pork" in `Preferences`: Exclude all pork dishes.
  - If "Seafood_Allergy" in `Preferences`: Exclude all seafood.
  - If "Vegetarian" in `Preferences`: Only include vegetarian dishes.
  - If "Not_Spicy" in `Preferences`: Exclude dishes marked as spicy.

## 2. Contextual Boosting (Soft Preferences)
{occasion_instructions}
- **For Kids ("Kids" tag)**:
...
  - **Exclude**: Dishes with many bones/spikes, very spicy, caffeine, raw food.
  - **Prioritize**: Fried items, sweet flavors, soft textures.
- **For Elderly ("Elderly" tag)**:
  - **Exclude**: Overly hard, tough (e.g., gristly steak), very spicy, or oily dishes.
  - **Prioritize**: Stews, steamed dishes, soups, soft-textured food.
- **For Alcohol ("Alcohol" tag)**:
  - **Prioritize**: Boldly flavored, savory dishes (e.g., fried items, skewers) and high-margin alcoholic beverages if available.
  - **Budget Conflict**: If budget is low, prioritize dishes that pair well with alcohol and suggest drinks as an optional add-on in the notes.
- **Combined Context (e.g., "Kids" AND "Elderly")**:
  - Prioritize the intersection: "Soft textures" and "Mild flavors" above all.

## 3. Dish Quantity Estimation (if Dish_Count_Target is null)
- **Shared Style**: 
  - Base Rule: Recommend `Party_Size + 1` dishes.
  - **Budget Expansion**: If the budget allows (i.e., current total is < 70% of budget), YOU SHOULD recommend more dishes (e.g., `Party_Size + 2` or `Party_Size + 3`) to provide a richer feast.
  - Structure: 1 starch, 1-2 main proteins, 1 vegetable, 1 soup/other.
- **Individual Style**: Recommend `Party_Size` complete sets.

## 4. Portion Size, Quantity & Satiety Check
**CRITICAL: Ensure recommended dishes provide adequate portions for the number of diners.**

### Quantity Calculation (MANDATORY for every dish)
Every dish MUST include a `quantity` field indicating how many portions to order:

- **Shared Style**:
  - **Main Dishes** (熱菜, 主菜, 主餐, 炒飯麵, 咖哩, etc.): `quantity = 1` (one sharing portion). If budget allows, consider ordering 2 portions of popular dishes for larger groups (>4 people).
  - **Small Dishes / Sides** (冷菜, 前菜, 配菜, 開胃菜, etc.): `quantity = ceil(Party_Size / 2)`
  - **Staples** (主食, 米飯, 麵類, etc.): `quantity = Party_Size` (one per person)
  - **Soups** (湯品, 湯類, 湯物): `quantity = 1` (one large soup to share)
  - **Desserts** (甜點, 甜品, Dolci): `quantity = ceil(Party_Size / 2)`

- **Individual Style**:
  - **All dishes**: `quantity = Party_Size` (each person gets their own portion)

### Portion Analysis
When selecting dishes, consider whether each dish's portion size is suitable for the party size:
- For **Shared Style**: Each dish should be shareable. If a dish is typically "single-serving" (e.g., 一人份), adjust the quantity accordingly
- For **Individual Style**: Each set should be one complete meal per person

### Satiety Guidelines
- **Shared Style**: The total food volume should satisfy all diners. Prioritize dishes with substantial portions.
- **Individual Style**: Each set must be a complete meal with sufficient calories.

### Special Cases
- If the restaurant is known for small portions (e.g., tapas, dim sum), recommend MORE dishes than the default formula OR increase quantities
- If the restaurant serves large portions (e.g., American steakhouse, family-style Chinese), the default `Party_Size + 1` may be sufficient with quantity = 1
- Always mention portion size considerations in your `recommendation_summary` if relevant

## 5. Pairing & Budgeting Algorithm
- **Variety Check**: Avoid more than two dishes with the same main protein (chicken, pork, beef) unless requested.
- **Cooking Style Mix**: Mix cooking methods (e.g., fried, steamed, stir-fried) for a balanced experience.
- **Budget Control**: 
  - **Target**: Aim to utilize **80-100%** of the user's budget to provide the best possible experience. Do not be overly frugal unless the user specifically asked for "cheap" options.
  - **Constraint**: The total price must NOT exceed the budget.
  - **Buffer**: A 5-10% buffer is acceptable for 'Total' budgets, but mention it in the summary. For 'Per_Person' budgets, be strict.

# Output Format
You MUST return a valid JSON object that strictly follows the schema below. Your main goal is to generate a LONG and DIVERSE list of about 20-25 recommended dishes in `menu_items`. The Python backend will handle the final selection and formatting. Do not use Markdown (e.g., ```json).

**CRITICAL REQUIREMENTS:**
1.  **Generate a large candidate pool**: The `menu_items` array should contain approximately 20-25 diverse, high-quality dish recommendations that fit the user's request.
2.  **Categorize every dish**: Every dish in `menu_items` MUST include a `category` field that correctly matches one of the categories for the detected `cuisine_type`.
3.  **Detect cuisine type**: The `cuisine_type` MUST be one of: "中式餐館", "日本料理", "美式餐廳", "義式料理", "泰式料理".
4.  **Ensure variety**: The list should cover different categories and price points suitable for the user. Do not just recommend all expensive items.

**Example Output Structure:**
```json
{{
  "cuisine_type": "中式餐館",
  "menu_items": [
    {{
      "dish_id": null,
      "dish_name": "小籠包",
      "price": 200,
      "quantity": 2,
      "reason": "鼎泰豐招牌菜品，342 則評論提到皮薄汁多",
      "category": "點心",
      "review_count": 342
    }},
    {{
      "dish_id": null,
      "dish_name": "蟹粉小籠包",
      "price": 380,
      "quantity": 1,
      "reason": "奢華版小籠包，適合想嘗鮮的顧客",
      "category": "點心",
      "review_count": 98
    }},
    {{
      "dish_id": null,
      "dish_name": "紅油抄手",
      "price": 180,
      "quantity": 2,
      "reason": "麻辣香濃，156 則評論推薦",
      "category": "冷菜",
      "review_count": 156
    }}
  ]
}}
```

**Full Schema:**
```json
{output_schema}
```

# Execution
Now, process the user's request based on the provided data.

{user_input_str}

# Menu Data
{menu_data}

# Reviews Data
{reviews_data}
"""
    return system_prompt.strip()


# ----- V1 (Deprecated) -----
from schemas.recommendation import RecommendationRequest, FullRecommendationResponse

def create_prompt_for_gemini(request: RecommendationRequest, reviews_text: str, menu_text: str, user_profile: dict = None) -> str:
    """
    DEPRECATED: Generates a structured prompt for Gemini 1.5 Flash.
    """
    
    # Extract preferences from profile
    past_preferences = ""
    if user_profile:
        history = user_profile.get("feedback_history", [])
        if history:
            past_preferences = f"User's Past Feedback History: {json.dumps(history[:3], ensure_ascii=False)}"
    
    # Get the JSON schema of the output model to guide the AI
    output_schema = json.dumps(FullRecommendationResponse.model_json_schema(), indent=2)
    
    system_role = "..." # Old prompt logic omitted for brevity
    user_context = "..."
    rag_context = "..."
    instructions = "..."
    
    return f"DEPRECATED PROMPT"
