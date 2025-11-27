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
            "currency": {
                "type": "string",
                "description": "The currency code detected from the menu or location (e.g., TWD, JPY, USD, EUR). Default to TWD if uncertain.",
                "default": "TWD"
            },
            "menu_items": {
                "type": "array",
                "description": "A list of 20-25 diverse and high-quality dish recommendations. PRIORITIZE SIGNATURE DISHES.",
                "items": {
                    "type": "object",
                    "properties": {
                        "dish_name": {"type": "string", "description": "Name of the dish (User's preferred language)"},
                        "dish_name_local": {"type": "string", "description": "Name of the dish in the restaurant's local language"},
                        "price": {"type": "integer"},
                        "quantity": {"type": "integer"},
                        "reason": {"type": "string", "description": "Why recommended? Mention if it is a signature dish (招牌/必點)."},
                        "category": {"type": "string", "description": "A logical category for the dish (e.g., Main, Side, Drink, Dessert, or specific like 'Beef', 'Seafood'). Do NOT force strict cuisine types."},
                        "review_count": {"type": "integer"}
                    },
                    "required": ["dish_name", "price", "quantity", "reason", "category"]
                }
            }
        },
        "required": ["currency", "menu_items"]
    }
    output_schema = json.dumps(simplified_schema, indent=2, ensure_ascii=False)
    
    # User preferences from profile
    past_preferences = ""
    if user_profile and user_profile.get("feedback_history"):
        history = user_profile.get("feedback_history", [])
        past_preferences = f"\n- User's Past Feedback History: {json.dumps(history[:3], ensure_ascii=False)}"

    # Create the user prompt
    user_prompt = f"""
User Request:
- Restaurant: {user_input.restaurant_name} (Place ID: {user_input.place_id})
- Party Size: {user_input.party_size}
- Dining Style: {user_input.dining_style}
- Budget: {user_input.budget.amount} TWD ({user_input.budget.type}) 
  (IMPORTANT: The user's budget is in TWD. If the restaurant's local currency is different (e.g., JPY, USD), please convert this TWD amount to the local currency to correctly filter menu items. Do NOT reject items just because the raw number doesn't match if the currency is different.)
- Dietary Restrictions: {', '.join(user_input.preferences) if user_input.preferences else 'None'}
- Dish Count Target: {user_input.dish_count_target if user_input.dish_count_target else 'Auto-calculate'}
- Language: {user_input.language}
- Occasion: "{user_input.occasion or 'None'}"
{past_preferences}

Menu Data:
{menu_data[:20000]}... (truncated if too long)

Reviews Data:
{reviews_data[:15000]}... (truncated if too long)
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

## 0. Restaurant Theme Detection (HIGHEST PRIORITY)
**CRITICAL: Identify what this restaurant is famous for based on its name and menu.**

- **Analyze Restaurant Name**: If the restaurant name contains specific dish types (e.g., "牛腸鍋", "拉麵", "壽司", "火鍋", "燒肉"), this is the MAIN THEME.
- **Priority Rule**: 
  - **MUST recommend the theme dish** as the primary recommendation (e.g., if restaurant is "博多牛腸鍋", the top recommendation MUST be some variation of 牛腸鍋).
  - **DO NOT recommend multiple versions of the same theme dish** unless the party size is very large (>6 people). Choose the ONE best option that matches the party size.
  - **DO NOT recommend generic items** (like plain rice, noodles, or side dishes) as the main dish if a theme dish exists.
  - **Example**: 
    - Restaurant: "博多牛腸鍋" + Party Size: 2 → Recommend ONE motsunabe (2-3人份 or suitable for 2)
    - Restaurant: "博多牛腸鍋" + Party Size: 6 → Recommend ONE large motsunabe (4-6人份) OR TWO smaller ones if needed
    - Restaurant: "一蘭拉麵" → Top recommendation: "拉麵" (tonkotsu ramen)
    - Restaurant: "鼎泰豐" → Top recommendation: "小籠包"
- **Portion Size Matching (CRITICAL)**:
  - **Check the dish description** for portion indicators like "1-2人份", "2-3人份", "4-6人份".
  - **ONLY recommend dishes that match or slightly exceed the party size**.
  - **Example**: If party size is 2, do NOT recommend "1-2人份" AND "4-6人份" of the same dish. Choose the appropriate size.
- **Verification**: Before finalizing recommendations, ask yourself: 
  1. "Does this recommendation match what the restaurant is famous for?" 
  2. "Is the portion size appropriate for the party size?"
  3. "Am I recommending duplicate dishes?"
  If any answer is "No", adjust.

## 1. Signature Dish Detection (PRIORITY)
- **Identify Signatures**: Scan reviews and menu for terms like "Must-try", "Signature", "Best-seller", "招牌", "必點", "推薦".
- **Prioritize**: Ensure these items are included in the `menu_items` list if they fit the user's dietary restrictions.
- **Highlight**: In the `reason` field, explicitly mention if it is a signature dish.

## 2. Flexible Categorization
- **No Strict Buckets**: Do NOT force dishes into fixed categories like "Cold Dish" or "Hot Dish" unless it makes sense.
- **Logical Grouping**: Use natural categories found in the menu (e.g., "Beef Dishes", "Noodles", "Appetizers", "Desserts").
- **Goal**: The categorization should help the user understand the menu structure, not confuse them.

## 3. Currency Detection & Budget Conversion (CRITICAL)
- **Detect Local Currency**: Analyze the menu prices and restaurant location to determine the currency (e.g., "JPY" for Japan, "TWD" for Taiwan, "USD" for USA).
- **Budget Conversion**: The user's budget is ALWAYS provided in **TWD**. If the restaurant uses a different currency:
  - **Convert the TWD budget to the local currency** using approximate exchange rates:
    - 1 TWD ≈ 4.5 JPY (Japan)
    - 1 TWD ≈ 0.032 USD (USA)
    - 1 TWD ≈ 0.029 EUR (Europe)
  - **Example**: If user budget is 500 TWD and restaurant is in Japan, convert to ~2,250 JPY before filtering dishes.
- **Price Filtering**: Use the CONVERTED budget amount to filter menu items, not the raw TWD number.

## 4. Pre-processing and Filtering (Hard Bans)
- **CRITICAL: Exclude Plain Staples as Main Recommendations**: 
  - **NEVER recommend** plain white rice (白飯/米飯/ライス), plain noodles (白麵), or water as a **primary dish** or **main recommendation**.
  - **Exception**: Specialty rice/noodle dishes are OK (e.g., "Truffle Risotto", "Signature Fried Rice", "Garlic Fried Rice", "Ramen with Toppings").
  - **Reasoning**: Plain rice is assumed to be a side item that customers will order separately if needed. The AI should focus on recommending the restaurant's specialty dishes.
  - **If the restaurant ONLY serves rice bowls** (e.g., 丼飯 restaurant), then rice bowls with toppings are the main dish and should be recommended.
- **Natural Input Priority**: If the `Natural_Input` conflicts with `Preferences` buttons, `Natural_Input` takes higher priority.
- **Absolute Prohibitions**:
  - If "No_Beef" in `Preferences`: Exclude all beef dishes.
  - If "No_Pork" in `Preferences`: Exclude all pork dishes.
  - If "Seafood_Allergy" in `Preferences`: Exclude all seafood.
  - If "Vegetarian" in `Preferences`: Only include vegetarian dishes.
  - If "Not_Spicy" in `Preferences`: Exclude dishes marked as spicy.

## 5. Contextual Boosting (Soft Preferences)
{occasion_instructions}
- **For Kids ("Kids" tag)**:
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

## 6. Dish Quantity Estimation (if Dish_Count_Target is null)
- **Shared Style**: 
  - Base Rule: Recommend `Party_Size + 1` dishes.
  - **Budget Expansion**: If the budget allows (i.e., current total is < 70% of budget), YOU SHOULD recommend more dishes (e.g., `Party_Size + 2` or `Party_Size + 3`) to provide a richer feast.
  - Structure: 1 starch, 1-2 main proteins, 1 vegetable, 1 soup/other.
- **Individual Style**: Recommend `Party_Size` complete sets.

## 7. Portion Size, Quantity & Satiety Check
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

## 8. Pairing & Budgeting Algorithm
- **Variety Check**: Avoid more than two dishes with the same main protein (chicken, pork, beef) unless requested.
- **Cooking Style Mix**: Mix cooking methods (e.g., fried, steamed, stir-fried) for a balanced experience.
- **Budget Control**: 
  - **Target**: Aim to utilize **80-100%** of the user's budget (AFTER CURRENCY CONVERSION) to provide the best possible experience. Do not be overly frugal unless the user specifically asked for "cheap" options.
  - **Constraint**: The total price must NOT exceed the budget.
  - **Buffer**: A 5-10% buffer is acceptable for 'Total' budgets, but mention it in the summary. For 'Per_Person' budgets, be strict.

# Output Format
You MUST return a valid JSON object that strictly follows the schema below. Your main goal is to generate a LONG and DIVERSE list of about 20-25 recommended dishes in `menu_items`. The Python backend will handle the final selection and formatting. Do not use Markdown (e.g., ```json).

**CRITICAL REQUIREMENTS:**
1.  **Generate a large candidate pool**: The `menu_items` array should contain approximately 20-25 diverse, high-quality dish recommendations that fit the user's request.
2.  **Categorize every dish**: Every dish in `menu_items` MUST include a `category` field.
3.  **Detect Currency**: Set the `currency` field to the detected local currency (e.g., "JPY", "TWD", "USD").
4.  **Ensure variety**: The list should cover different categories and price points suitable for the user. Do not just recommend all expensive items.
5.  **Language**: 
    - `dish_name`: MUST be in the user's preferred language: **{user_input.language}**.
    - `dish_name_local`: MUST be in the restaurant's local language (e.g., Japanese for a restaurant in Japan). If the local language IS the user's language, this can be the same as `dish_name`.
    - `reason`: MUST be in the user's preferred language. Mention if it's a signature dish.

**Full Schema:**
```json
{output_schema}
```

# User Request
- Restaurant: {user_input.restaurant_name} (Place ID: {user_input.place_id})
- Party Size: {user_input.party_size}
- Dining Style: {user_input.dining_style}
- Budget: {user_input.budget.amount} TWD ({user_input.budget.type})
- Dietary Restrictions: {', '.join(user_input.preferences) if user_input.preferences else 'None'}
- Dish Count Target: {user_input.dish_count_target if user_input.dish_count_target else 'Auto-calculate'}
- Language: {user_input.language}
- Occasion: {user_input.occasion or 'None'}{past_preferences}

# Menu Data
{menu_data[:20000]}

# Reviews Data
{reviews_data[:15000]}
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
