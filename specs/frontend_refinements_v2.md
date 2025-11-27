# Frontend Refinements Specification (v2)

## 1. Page Title Update
**Goal**: Update the browser tab title to match the new branding.
- **File**: `frontend/src/app/layout.tsx`
- **Change**: Update `metadata.title` to "Carte AI: Dining Agent".

## 2. Preferences Page (Step 2) Enhancements
**Goal**: Contextualize the "Occasion" selection and standardize "Dietary Restrictions".
- **File**: `frontend/src/app/input/page.tsx`

### 2.1 Contextual Occasions
- **Logic**: Display different "Occasion" options based on the selected `mode` (Sharing vs. Individual).
- **Sharing Mode Occasions**:
  1.  Friends Gathering (朋友聚會)
  2.  Family Reunion (家庭聚餐)
  3.  Date Night (約會慶祝)
  4.  Business Meal (商務聚餐)
- **Individual Mode Occasions**:
  1.  Quick Meal (快速解決) - *For efficiency*
  2.  Treat Myself (犒賞自己) - *For quality*
  3.  Fitness/Fat Loss (健身減脂) - *For health*
  4.  New Adventure (全新探險) - *For discovery*

### 2.2 Dietary Restrictions
- **Logic**: Simplify the tag selection to 6 core options.
- **Options**:
  1.  No Beef (不吃牛)
  2.  No Pork (不吃豬)
  3.  No Seafood (不吃海鮮)
  4.  Vegetarian (素食)
  5.  No Spicy (不吃辣)
  6.  No Cilantro (不吃香菜)

## 3. Loading State Visual Update
**Goal**: Improve the visual feedback during the analysis phase.
- **File**: `frontend/src/components/gamified-loading-state.tsx`
- **Issue**: User reported the "circle" looks like a "forbidden" sign.
- **Solution**:
  - Replace the step icons.
  - **Completed**: `CheckCircle2` (Green, Solid)
  - **Current**: `Loader2` (Spinning, Primary Color) OR a `CircleDot` to indicate "in progress".
  - **Pending**: `Circle` (Gray, Outline)
  - Ensure the main loading animation (rotating border) is clean and doesn't look like a "stop" sign.

## 4. "Load failed" Bug Investigation
**Goal**: Identify and fix the cause of the "Load failed" error.
- **Potential Causes**:
  - API Timeout (Vercel/Cloud Run limits).
  - Empty response from Gemini.
  - JSON parsing error.
- **Action**:
  - Review `frontend/src/lib/api.ts` (need to read this).
  - Add better error handling in `frontend/src/app/recommendation/page.tsx`.
  - Ensure `dining_agent.py` returns a valid JSON even on partial failure.
