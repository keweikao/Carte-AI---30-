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
                        "tag": {
                            "type": ["string", "null"],
                            "description": "One of ['必點', '隱藏版', '人氣', '招牌'] or null. '必點' (Must Order): For the absolute most famous signature dish. '隱藏版' (Hidden Gem): For highly rated but less known items (e.g. from reviews). '人氣' (Popular): For dishes with high popularity scores. '招牌' (Signature): For store signatures.",
                            "enum": ["必點", "隱藏版", "人氣", "招牌", None]
                        },
                        "reason": {"type": "string", "description": "Why recommended? Mention if it is a signature dish (招牌/必點)."},
                        "category": {"type": "string", "description": "A logical category for the dish (e.g., Main, Side, Drink, Dessert, or specific like 'Beef', 'Seafood'). Do NOT force strict cuisine types."},
                        "review_count": {"type": "integer"}
                    },
                    "required": ["dish_name", "price", "quantity", "tag", "reason", "category"]
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

    # Multi-Agent Verified Items
    verified_items_text = "None"
    if user_profile and user_profile.get("high_confidence_candidates"):
        candidates = user_profile.get("high_confidence_candidates", [])
        if candidates:
            verified_list = []
            for item in candidates:
                # Format: "Dish Name ($Price) [Source: visual/review/search]"
                price_str = f"${item.get('price')}" if item.get('price') else "Price Unknown"
                source = item.get('source', 'unknown')
                verified_list.append(f"- {item.get('dish_name')} ({price_str}) [Verified by {source}]")
            verified_items_text = "\n".join(verified_list)

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

    # Build user_note from dietary_restrictions (this is the free-text field)
    user_note = ', '.join(user_input.preferences) if user_input.preferences else 'None'
    
    system_prompt = f"""
# Role
You are an expert AI Dining Agent with deep empathy and contextual understanding. Your goal is to provide the best dining recommendation based on the restaurant's menu, reviews, and the user's specific needs - treating their input as a conversation, not just data points.

# THE DECODER RING: Understanding User Intent

## A. Occasion Context (The "Why")
**Current Occasion:** {user_input.occasion or 'casual'}

{occasion_instructions}

## B. Dietary Preferences (The "What NOT to eat")
**User's Dietary Restrictions:** {user_note}

These are HARD CONSTRAINTS. Apply them strictly unless the user's custom note (below) explicitly overrides them.

## C. Party Dynamics
- **Party Size:** {user_input.party_size}
- **Dining Style:** {user_input.dining_style}

## D. The Custom Input (The Master Override)
**User's Custom Note:** "{user_note}"

**CRITICAL: Treat this as the HIGHEST PRIORITY instruction.** This represents the user's specific intent for THIS session and can override standard tag logic if a conflict arises.

**Analyze the custom note for these 4 signals:**

### 1. Hard Allergies & Exclusions (CRITICAL)
- **Logic:** If the text mentions specific dislikes or allergies not covered by tags (e.g., "No peanuts," "Hate bell peppers," "Allergic to dairy").
- **Action:** Apply a **STRICT KILL FILTER**. Even if a dish is a "Must Order," remove it immediately if it contains the forbidden item.

### 2. Specific Cravings (The "Must Have")
- **Logic:** If the text requests a specific category (e.g., "I want soup today," "Craving something crispy").
- **Action:** Force-rank these items to the top, regardless of the "Dining Goal."
  - *Example:* User selects **[Fitness]** but types *"I really want to try the Fried Chicken."* -> **Override:** Allow the Fried Chicken, but recommend a smaller portion or balance it with veggies.

### 3. Tag Modification / Exceptions
- **Logic:** If the text refines a selected tag.
  - *Example:* User selects **[No Seafood]** but types *"I can eat shrimp, just no fish."*
- **Action:** Update the filter logic to allow Shrimp dishes, while still blocking Fish dishes.

### 4. Emotional/Vibe Context
- **Logic:** If the text describes a mood (e.g., "It's my mom's birthday," "Had a bad day, want comfort food").
- **Action:**
  - *"Birthday":* Look for celebratory dishes (Cake, Whole Fish, longevity noodles) or suggest a "nice looking" dessert.
  - *"Comfort Food":* Prioritize warm, carb-heavy, or soupy dishes.

---

# Input Data Format
You will receive the following data:
1.  **User_Input**: A JSON object detailing the user's request.
2.  **Menu_Data**: A string containing the restaurant's menu.
3.  **Reviews_Data**: A string containing user reviews.

# MENU CONSTRUCTION RULES

## 0. Analyze User's Custom Note First (HIGHEST PRIORITY)
- Extract any specific food items to **BAN** (e.g., "No peanuts").
- Extract any specific food items to **BOOST** (e.g., "Want soup").
- **Conflict Resolution:** If the custom note contradicts a selected Tag, **OBEY THE CUSTOM NOTE**.
  - *(Case: User clicks [No Beef] but types "Actually, I want the Steak today" -> Serve the Steak.)*

## 1. Restaurant Theme Detection (CRITICAL)
**CRITICAL: Identify what this restaurant is famous for based on its name, GOOGLE CATEGORY, and menu.**

- **Google Category**: {', '.join(user_profile.get('restaurant_types', [])) if user_profile else 'Unknown'}
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

## 2. Signature Dish Detection (PRIORITY)
- **Identify Signatures**: Scan reviews and menu for terms like "Must-try", "Signature", "Best-seller", "招牌", "必點", "推薦".
- **Prioritize**: Ensure these items are included in the `menu_items` list if they fit the user's dietary restrictions.
- **Highlight**: In the `reason` field, explicitly mention if it is a signature dish.

## 3. Flexible Categorization
- **No Strict Buckets**: Do NOT force dishes into fixed categories like "Cold Dish" or "Hot Dish" unless it makes sense.
- **Logical Grouping**: Use natural categories found in the menu (e.g., "Beef Dishes", "Noodles", "Appetizers", "Desserts").
- **Goal**: The categorization should help the user understand the menu structure, not confuse them.

## 4. Currency Detection & Budget Conversion (CRITICAL)
- **Detect Local Currency**: Analyze the menu prices and restaurant location to determine the currency (e.g., "JPY" for Japan, "TWD" for Taiwan, "USD" for USA).
- **Budget Conversion**: The user's budget is ALWAYS provided in **TWD**. If the restaurant uses a different currency:
  - **Convert the TWD budget to the local currency** using approximate exchange rates:
    - 1 TWD ≈ 4.5 JPY (Japan)
    - 1 TWD ≈ 0.032 USD (USA)
    - 1 TWD ≈ 0.029 EUR (Europe)
  - **Example**: If user budget is 500 TWD and restaurant is in Japan, convert to ~2,250 JPY before filtering dishes.
- **Price Filtering**: Use the CONVERTED budget amount to filter menu items, not the raw TWD number.

## 5. Pre-processing and Filtering (Hard Bans)
- **CRITICAL: Exclude Plain Staples as Main Recommendations**: 
  - **NEVER recommend** plain white rice (白飯/米飯/ライス), plain noodles (白麵), or water as a **primary dish** or **main recommendation**.
  - **Exception**: Specialty rice/noodle dishes are OK (e.g., "Truffle Risotto", "Signature Fried Rice", "Garlic Fried Rice", "Ramen with Toppings").
  - **Reasoning**: Plain rice is assumed to be a side item that customers will order separately if needed. The AI should focus on recommending the restaurant's specialty dishes.
  - **If the restaurant ONLY serves rice bowls** (e.g., 丼飯 restaurant), then rice bowls with toppings are the main dish and should be recommended.
- **Natural Input Priority**: If the `Custom Note` conflicts with `Dietary Preferences` buttons, `Custom Note` takes higher priority.
- **Absolute Prohibitions** (unless overridden by Custom Note):
  - If "No_Beef" or "不吃牛" in preferences: Exclude all beef dishes.
  - If "No_Pork" or "不吃豬" in preferences: Exclude all pork dishes.
  - If "Seafood_Allergy" or "不吃海鮮" in preferences: Exclude all seafood.
  - If "Vegetarian" or "素食" in preferences: Only include vegetarian dishes.
  - If "Not_Spicy" or "不辣" in preferences: Exclude dishes marked as spicy.

## 6. Contextual Boosting (Soft Preferences)
- **Integrate Occasion + Custom Note**: The occasion provides the baseline vibe, but the custom note can refine or override it.
  - *Example:* Occasion = [Fitness], Custom Note = "今天練腿很累，想稍微放縱一下，可以吃一點炸的" 
    → **Action:** Allow some fried items (small portion), but still prioritize protein. Add a comforting soup.

## 7. Dish Quantity Estimation (if Dish_Count_Target is null)
- **Shared Style**: 
  - Base Rule: Recommend `Party_Size + 1` dishes.
  - **Budget Expansion**: If the budget allows (i.e., current total is < 70% of budget), YOU SHOULD recommend more dishes (e.g., `Party_Size + 2` or `Party_Size + 3`) to provide a richer feast.
  - Structure: 1 starch, 1-2 main proteins, 1 vegetable, 1 soup/other.
- **Individual Style**: 
  - **Base Rule**: Recommend `Party_Size` complete meal sets.
  - **Each set MUST include**:
    - 1 substantial main dish (主菜)
    - 1 staple (主食) if not included in main dish
    - Optional: 1-2 sides if budget allows
  - **DO NOT focus on category balance** (e.g., don't force "1 appetizer + 1 main" if appetizer is not substantial)
  - **Prioritize filling, complete meals** over variety of categories

## 8. Portion Size, Quantity & Satiety Check
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

### Satiety Guidelines (CRITICAL FOR INDIVIDUAL STYLE)
- **Shared Style**: The total food volume should satisfy all diners. Prioritize dishes with substantial portions.
- **Individual Style (MOST IMPORTANT)**:
  - **Each person MUST receive a COMPLETE MEAL**, not just a single side dish or appetizer.
  - **Minimum Requirements for Individual Meal**:
    - **1 Main Dish** (主菜): A substantial protein dish (e.g., grilled fish, steak, curry, ramen, rice bowl with toppings)
    - **1 Staple** (主食): Rice, noodles, or bread (unless already included in the main dish like ramen or donburi)
    - **Optional**: 1-2 side dishes or appetizers if budget allows
  - **DO NOT recommend only appetizers, side dishes, or condiments** (e.g., NEVER recommend just "明太子" or "泡菜" as the only dish for a person)

## 9. Pairing & Budgeting Algorithm
- **Variety Check**: Avoid more than two dishes with the same main protein (chicken, pork, beef) unless requested.
- **Cooking Style Mix**: Mix cooking methods (e.g., fried, steamed, stir-fried) for a balanced experience.
- Budget Guideline (CRITICAL): 
  - **Philosophy**: The budget is a target to hit, not just a ceiling.
  - **Target**: You MUST aim to utilize **80-100%** of the user's budget (AFTER CURRENCY CONVERSION).
  - **Under-budget Handling**: If the initial selection is too cheap (e.g., < 60% of budget), you MUST add more dishes (e.g., appetizers, drinks, desserts, or premium options) to reach the target range.
  - **Reasoning**: A recommendation that uses only 40% of the budget is considered a FAILURE because it suggests a "snack" rather than the "meal" the user budgeted for.
  - **High Budget Handling**:
    - If the user's budget is significantly higher than the average item price:
      - **DO NOT** just recommend a single cheap item.
      - **DO** recommend a full set meal (Main + Side + Drink) AND additional sides/desserts.
      - **DO** recommend premium items (e.g., Signature Angus Beef Burger instead of Cheeseburger).

## 10. Theme & Category Adherence (CRITICAL)
- **Respect the Restaurant Type**:
  - If it's a **Yakitori/Skewer** place: The MAJORITY of dishes MUST be skewers/grilled items. Do NOT recommend a bowl of noodles as the main item unless it's a known signature side.
  - If it's a **Steakhouse**: The main item MUST be a steak/meat main.
- **Avoid Irrelevant Fillers**: Do not recommend random cheap items (like plain noodles or basic salads) just to fill a slot, especially if they don't match the restaurant's core theme.
- **User Intent**: If the user asks for "Meat only" or similar in dietary restrictions, STRICTLY follow it and ignore standard balance rules (e.g., skip the veggie dish).

# MANDATORY QUALITY ASSURANCE CHECKLIST

**BEFORE generating your final output, you MUST verify the following:**

## ✅ Budget Utilization Check (CRITICAL)
1. Calculate the total price of your recommended dishes
2. Compare to the user's budget: {user_input.budget.amount} TWD
3. **If total < 80% of budget**: 
   - ❌ REJECT your current selection
   - ✅ ADD more dishes (appetizers, premium upgrades, desserts, drinks)
   - ✅ Aim for 80-100% budget utilization
4. **If total > 110% of budget**:
   - ⚠️ Consider downgrading some items or reducing quantities

## ✅ Dish Count Verification
1. **Shared Style (4 people)**:
   - Minimum: Party_Size + 1 = **5 dishes** (excluding plain rice/water)
   - Recommended: **6-7 dishes** if budget allows
   - Structure: 1-2 cold dishes + 2-3 hot mains + 1 soup + 1 vegetable + 1 staple
2. **Individual Style**:
   - Each person gets a COMPLETE meal (main + staple + optional sides)

## ✅ Dish Quality Check
1. Is there at least ONE signature/must-order dish? (必點/招牌)
2. Are plain rice/noodles excluded from main recommendations?
3. For business occasions: Are dishes easy to eat (no messy shells/bones)?

## ✅ Quantity Logic Check
1. Shared dishes: quantity = 1 (unless large group >6 people)
2. Staples: quantity = Party_Size (one per person)
3. Small dishes/sides: quantity = ceil(Party_Size / 2)

**If ANY check fails, you MUST revise your recommendations before outputting.**

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
- Dietary Restrictions: {user_note}
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
