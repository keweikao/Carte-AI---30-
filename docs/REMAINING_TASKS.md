# OderWhat v2.0 - 剩餘開發任務清單

**最後更新**: 2025-12-03
**當前狀態**: Phase 1 部分完成，需繼續開發 Phase 1-3

---

## 📋 已完成的工作

### ✅ Phase 0: 基礎架構重構（已完成）
1. 建立新的分層式管線架構
   - `services/pipeline/providers.py` - 資料獲取層
   - `services/pipeline/intelligence.py` - AI 處理層
   - `services/pipeline/orchestrator.py` - 流程協調層
   - `schemas/pipeline.py` - 中間資料結構

2. 修正配置錯誤
   - ✅ 使用 `gemini-1.5-flash` (Vision)
   - ✅ 使用 `searchStringsArray` (Apify)
   - ✅ 使用 HTTP 直接呼叫 Serper.dev
   - ✅ 圖片 Base64 編碼

3. 新增 `DishAttributes` 結構
   - ✅ 已在 `schemas/restaurant_profile.py` 定義完整屬性
   - ✅ 已更新 `MenuItem` schema 加入 `analysis` 欄位

---

## ⚠️ 當前問題

**緊急**: Cloud Run 部署後 API 請求超時/掛起
- **Revision**: `oderwhat-staging-00031-9bk`
- **症狀**: API 請求無回應
- **可能原因**:
  - Import 錯誤（新模組導入問題）
  - 環境變數缺失
  - 非同步邏輯錯誤
- **需要做**: 查看 Cloud Run 日誌找出錯誤

**查看日誌**:
```
https://console.cloud.google.com/run/detail/asia-east1/oderwhat-staging/logs?project=gen-lang-client-0415289079
```

搜尋關鍵字: `ERROR`, `Exception`, `Pipeline`, `Aggregator`

---

## 🎯 待完成任務

### Phase 1: 完善 AI 屬性標註（最優先）

#### Task 3: 實作 `MenuIntelligence.analyze_dish_batch()`

**檔案**: `services/pipeline/intelligence.py`

**目標**: 新增 `MenuIntelligence` class，實作批次屬性分析

**實作內容**:

```python
class MenuIntelligence:
    """
    Advanced AI tagging for dish attributes
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=self.api_key)

    async def analyze_dish_batch(
        self,
        dishes: List[ParsedMenuItem],
        reviews: List[RawReview]
    ) -> List[DishAttributes]:
        """
        使用 Gemini AI 批次分析菜色屬性

        Args:
            dishes: 已解析的菜單項目列表
            reviews: 顧客評論列表

        Returns:
            List of DishAttributes (每道菜的結構化屬性)
        """
```

**System Prompt 範本**:

```python
prompt = f"""
你是一位專業的食品科學家與數據分析師。

任務：分析菜單項目並標註結構化屬性。

菜單項目：
{json.dumps([{"name": d.name, "description": d.description} for d in dishes], ensure_ascii=False)}

顧客評論摘要（參考用）：
{json.dumps([r.text[:100] for r in reviews[:10]], ensure_ascii=False)}

請為每道菜輸出以下 JSON 格式：

{{
  "dish_attributes": [
    {{
      "dish_name": "宮保雞丁",

      // 硬過濾屬性（絕對判斷，不確定則標 false）
      "is_spicy": true,
      "is_vegan": false,
      "contains_beef": false,
      "contains_pork": false,
      "contains_seafood": false,
      "allergens": ["peanuts"],

      // 軟排序屬性
      "flavors": ["spicy", "savory", "garlic_heavy"],
      "textures": ["crispy", "tender"],
      "temperature": "hot",
      "cooking_method": "stir_fried",
      "suitable_occasions": ["group_share", "alcohol_pairing"],

      // 價值屬性
      "is_signature": true,
      "sentiment_score": 0.8,
      "highlight_review": "網友大推：外皮酥脆，花生香氣十足"
    }}
  ]
}}

重要規則：
1. 成分檢測必須嚴格：無法確定的標示 false
2. 過敏原只列出明確的（堅果、海鮮、乳製品等）
3. sentiment_score 範圍 -1.0 到 1.0（根據評論情感）
4. highlight_review 只有在評論明確提及時才填入
"""
```

**錯誤處理**:
- JSON 解析失敗 → 回傳預設屬性（全 false/empty）
- API 錯誤 → 記錄錯誤並回傳空列表

---

#### Task 4: 整合屬性標註到管線

**檔案**: `services/pipeline/orchestrator.py`

**修改位置**: `RestaurantPipeline.process()` 方法中的 STEP 3

**當前程式碼** (約在 line 70-80):

```python
# STEP 3: Review fusion
print(f"\n[Pipeline] STEP 3: Fusing reviews with menu...")

enhanced_menu, review_summary = await self.insight_engine.fuse_reviews(
    menu_items=menu_items,
    reviews=map_data.reviews
)
```

**需要改為**:

```python
# STEP 3: AI Attribute Tagging + Review fusion
print(f"\n[Pipeline] STEP 3: AI analysis and review fusion...")

# 3.1: 屬性標註
intelligence = MenuIntelligence()
dish_attributes = await intelligence.analyze_dish_batch(
    dishes=menu_items,
    reviews=map_data.reviews
)

# 3.2: 評論融合（保留原有邏輯，但整合屬性）
enhanced_menu, review_summary = await self.insight_engine.fuse_reviews(
    menu_items=menu_items,
    reviews=map_data.reviews
)

# 3.3: 將屬性綁定到菜單項目
for idx, item in enumerate(enhanced_menu):
    if idx < len(dish_attributes):
        item.analysis = dish_attributes[idx]
    # 生成 unique ID
    item.id = f"{map_data.place_id}_{idx}_{item.name[:10]}"
```

**注意事項**:
- Import `MenuIntelligence` from `intelligence.py`
- Import `DishAttributes` from `schemas.restaurant_profile`

---

### Phase 2: 建立即時推薦系統

#### Task 5: 建立 `UserInputV2` Schema

**檔案**: `schemas/recommendation.py`

**創建新檔案**:

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class UserInputV2(BaseModel):
    """
    使用者輸入 v2.0 - 用於智慧推薦
    """

    # 基本資訊
    occasion: Literal["date", "business", "family", "friends", "solo"] = "friends"
    group_size: int = Field(default=2, ge=1, le=20)
    budget_per_person: Optional[int] = Field(default=None, description="每人預算（台幣）")

    # 飲食限制（硬過濾）
    dietary_restrictions: List[str] = Field(
        default_factory=list,
        description="e.g., ['no_beef', 'no_pork', 'no_seafood', 'vegan', 'no_spicy']"
    )

    # 過敏原
    allergens: List[str] = Field(
        default_factory=list,
        description="e.g., ['nuts', 'shrimp', 'milk']"
    )

    # 偏好（軟排序）
    preferred_flavors: List[str] = Field(
        default_factory=list,
        description="e.g., ['spicy', 'sour', 'sweet']"
    )

    preferred_textures: List[str] = Field(
        default_factory=list,
        description="e.g., ['crispy', 'soup']"
    )

    # 其他偏好
    avoid_messy_food: bool = Field(default=False, description="約會場景避免油膩/需用手抓的菜")
    prefer_signature: bool = Field(default=True, description="優先推薦招牌菜")
```

---

#### Task 6-7: 實作 `RecommendationService`

**檔案**: `agent/recommendation.py` (新建檔案)

**完整實作範本**:

```python
"""
Runtime Recommendation Service
即時推薦邏輯（非 Agent Loop，純 Python + LLM）
"""

import os
from typing import List, Tuple
import google.generativeai as genai
import json

from schemas.recommendation import UserInputV2
from schemas.restaurant_profile import RestaurantProfile, MenuItem


class RecommendationService:
    """
    兩階段推薦系統：
    1. Hard Filter (Python) - 絕對條件過濾
    2. Soft Ranking (LLM) - 場景匹配與理由生成
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set")
        genai.configure(api_key=self.api_key)

    async def generate_recommendation(
        self,
        user_input: UserInputV2,
        profile: RestaurantProfile
    ) -> dict:
        """
        主要推薦流程

        Returns:
            {
                "recommended_dishes": List[MenuItem],
                "reasoning": str,
                "total_price": int,
                "warnings": List[str]
            }
        """

        # STEP 1: Hard Filter (Python)
        candidates = self._hard_filter(user_input, profile.menu_items)

        if not candidates:
            return {
                "recommended_dishes": [],
                "reasoning": "找不到符合您條件的菜色，請調整篩選條件。",
                "total_price": 0,
                "warnings": ["無符合菜色"]
            }

        # STEP 2: Soft Ranking (LLM)
        final_dishes, reasoning = await self._soft_ranking(
            user_input, candidates
        )

        # STEP 3: Calculate total
        total_price = sum(d.price or 0 for d in final_dishes)

        # STEP 4: Generate warnings
        warnings = self._generate_warnings(user_input, final_dishes, total_price)

        return {
            "recommended_dishes": final_dishes,
            "reasoning": reasoning,
            "total_price": total_price,
            "warnings": warnings
        }

    def _hard_filter(
        self,
        user_input: UserInputV2,
        all_dishes: List[MenuItem]
    ) -> List[MenuItem]:
        """
        硬過濾邏輯（Python 純運算，不使用 LLM）
        """
        candidates = []

        for dish in all_dishes:
            # 跳過沒有屬性的菜（fallback dish）
            if not dish.analysis:
                continue

            # 預算過濾（允許 10% 彈性）
            if user_input.budget_per_person:
                max_price = user_input.budget_per_person * 0.9
                if dish.price and dish.price > max_price:
                    continue

            # 飲食限制過濾
            if "no_beef" in user_input.dietary_restrictions and dish.analysis.contains_beef:
                continue
            if "no_pork" in user_input.dietary_restrictions and dish.analysis.contains_pork:
                continue
            if "no_seafood" in user_input.dietary_restrictions and dish.analysis.contains_seafood:
                continue
            if "vegan" in user_input.dietary_restrictions and not dish.analysis.is_vegan:
                continue
            if "no_spicy" in user_input.dietary_restrictions and dish.analysis.is_spicy:
                continue

            # 過敏原過濾
            if any(allergen in dish.analysis.allergens for allergen in user_input.allergens):
                continue

            # 約會場景特殊過濾
            if user_input.avoid_messy_food:
                messy_textures = ["soup", "messy", "sauce_heavy"]
                if any(t in dish.analysis.textures for t in messy_textures):
                    continue

            # 通過所有過濾
            candidates.append(dish)

        print(f"[RecommendationService] Hard filter: {len(all_dishes)} → {len(candidates)} candidates")
        return candidates

    async def _soft_ranking(
        self,
        user_input: UserInputV2,
        candidates: List[MenuItem]
    ) -> Tuple[List[MenuItem], str]:
        """
        使用 LLM 進行場景匹配與排序
        """

        # 限制候選菜數量（避免 prompt 過長）
        if len(candidates) > 30:
            # 優先保留招牌菜和高評分菜
            candidates = sorted(
                candidates,
                key=lambda d: (
                    d.analysis.is_signature if d.analysis else False,
                    d.analysis.sentiment_score if d.analysis else 0
                ),
                reverse=True
            )[:30]

        # 建立候選菜資訊（簡化版，避免過長）
        candidates_info = []
        for d in candidates:
            info = {
                "name": d.name,
                "price": d.price,
                "category": d.category,
            }
            if d.analysis:
                info["is_signature"] = d.analysis.is_signature
                info["sentiment_score"] = d.analysis.sentiment_score
                info["highlight"] = d.analysis.highlight_review or "無特別評價"
                info["flavors"] = d.analysis.flavors
                info["occasions"] = d.analysis.suitable_occasions
            candidates_info.append(info)

        # 建立 Prompt
        model = genai.GenerativeModel('gemini-1.5-flash')  # 快速模型

        prompt = f"""
你是專業的餐廳經理。客人資訊如下：

- 用餐場景：{user_input.occasion}
- 人數：{user_input.group_size} 人
- 預算（每人）：{user_input.budget_per_person or '不限'}
- 偏好口味：{', '.join(user_input.preferred_flavors) or '無特別偏好'}

候選菜單（已過濾不符合條件的菜色）：
{json.dumps(candidates_info, ensure_ascii=False, indent=2)}

請完成以下任務：

1. 從候選菜中挑選 3-5 道最適合的組合
2. 確保：
   - 場景匹配（例如約會避開大蒜重、油膩菜）
   - 口味平衡（有主食、蔬菜、肉類）
   - 價格合理（總價不超過預算）
   - 優先選擇招牌菜（is_signature: true）

3. 回傳 JSON 格式：
{{
  "selected_dish_names": ["菜名1", "菜名2", "菜名3"],
  "reasoning": "推薦理由說明（2-3 句話，引用 highlight 內容）"
}}
"""

        try:
            response = await model.generate_content_async(prompt)
            result_text = response.text

            # 清理 JSON
            if result_text.startswith("```json"):
                result_text = result_text[len("```json"):].strip()
            if result_text.endswith("```"):
                result_text = result_text[:-len("```")].strip()

            result = json.loads(result_text)

            # 根據 LLM 回傳的名稱找出實際的 MenuItem
            selected_names = set(result.get("selected_dish_names", []))
            final_dishes = [d for d in candidates if d.name in selected_names]
            reasoning = result.get("reasoning", "AI 推薦組合")

            print(f"[RecommendationService] LLM selected {len(final_dishes)} dishes")
            return final_dishes, reasoning

        except Exception as e:
            print(f"[RecommendationService] LLM ranking error: {e}")
            # Fallback: 回傳前 3 個招牌菜
            fallback = sorted(
                candidates,
                key=lambda d: d.analysis.is_signature if d.analysis else False,
                reverse=True
            )[:3]
            return fallback, "系統自動推薦（招牌菜優先）"

    def _generate_warnings(
        self,
        user_input: UserInputV2,
        dishes: List[MenuItem],
        total_price: int
    ) -> List[str]:
        """
        生成警告訊息
        """
        warnings = []

        # 預算警告
        if user_input.budget_per_person:
            expected_total = user_input.budget_per_person * user_input.group_size
            if total_price > expected_total * 1.1:
                warnings.append(f"總價 ${total_price} 超出預算約 {int((total_price / expected_total - 1) * 100)}%")

        # 菜色數量警告
        if len(dishes) < 2:
            warnings.append("菜色較少，建議再加點")

        if len(dishes) < user_input.group_size:
            warnings.append(f"{user_input.group_size} 人用餐建議至少 {user_input.group_size} 道菜")

        return warnings
```

---

#### Task 8: 建立推薦 API 端點

**檔案**: `api/v1/recommend.py` (新建檔案)

```python
from fastapi import APIRouter, HTTPException, BackgroundTasks
from schemas.recommendation import UserInputV2
from schemas.restaurant_profile import RestaurantProfile
from services import firestore_service
from agent.recommendation import RecommendationService
from services.pipeline import RestaurantPipeline

router = APIRouter()

@router.post("/recommend/{place_id}")
async def get_recommendation(
    place_id: str,
    user_input: UserInputV2,
    background_tasks: BackgroundTasks
):
    """
    智慧推薦端點

    Flow:
    1. 檢查 Firestore 是否有 Profile
    2. 若無 → 觸發 Background Pipeline → 回傳 202 Accepted
    3. 若有 → 執行推薦 → 回傳 200 OK
    """

    # 查詢 Profile
    profile = firestore_service.get_restaurant_profile(place_id)

    if not profile:
        # Cold Start: 觸發 Pipeline
        print(f"[RecommendAPI] Cold start for {place_id}, triggering pipeline")

        # 需要餐廳名稱來啟動 pipeline（從哪裡取得？）
        # 選項 1: 要求 client 提供 name
        # 選項 2: 使用 Google Places API 查詢

        # 這裡先回傳 202（實際上應該要 SSE 或 WebSocket）
        background_tasks.add_task(_run_pipeline_async, place_id, "restaurant_name_here")

        return {
            "status": "processing",
            "message": "正在處理餐廳資料，請稍後重試",
            "estimated_time": "30-60 seconds"
        }, 202

    # Warm Start: 執行推薦
    service = RecommendationService()
    result = await service.generate_recommendation(user_input, profile)

    return result

async def _run_pipeline_async(place_id: str, name: str):
    """背景任務：執行 Pipeline"""
    try:
        pipeline = RestaurantPipeline()
        profile = await pipeline.process(name)

        if profile:
            # 確保使用正確的 place_id
            profile.place_id = place_id
            firestore_service.save_restaurant_profile(profile)
            print(f"[Background] Pipeline completed for {place_id}")
        else:
            print(f"[Background] Pipeline failed for {place_id}")
    except Exception as e:
        print(f"[Background] Pipeline error: {e}")
```

**整合到 main.py**:

```python
# 在 main.py 中加入
from api.v1.recommend import router as recommend_router

app.include_router(recommend_router, prefix="/api/v1")
```

---

### Phase 3: 測試與優化

#### Task 11-13: 測試計劃

**建立測試檔案**: `tests/test_recommendation.py`

```python
import pytest
from schemas.recommendation import UserInputV2
from schemas.restaurant_profile import MenuItem, DishAttributes
from agent.recommendation import RecommendationService

def test_hard_filter_no_beef():
    """測試無牛肉過濾"""
    service = RecommendationService()

    dishes = [
        MenuItem(
            name="牛肉麵",
            price=150,
            analysis=DishAttributes(contains_beef=True)
        ),
        MenuItem(
            name="雞肉飯",
            price=80,
            analysis=DishAttributes(contains_beef=False)
        )
    ]

    user_input = UserInputV2(dietary_restrictions=["no_beef"])

    result = service._hard_filter(user_input, dishes)

    assert len(result) == 1
    assert result[0].name == "雞肉飯"

# 更多測試...
```

---

## 🚀 部署流程

**重新部署**:

```bash
gcloud builds submit --config=cloudbuild.yaml --project=gen-lang-client-0415289079
```

**測試 API**:

```bash
# 測試推薦端點
curl -X POST "https://oderwhat-staging-u33peegeaa-de.a.run.app/api/v1/recommend/ChIJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "occasion": "date",
    "group_size": 2,
    "budget_per_person": 500,
    "dietary_restrictions": ["no_spicy"],
    "avoid_messy_food": true
  }'
```

---

## 📝 注意事項

1. **環境變數確認**:
   - `GEMINI_API_KEY` 必須設定
   - `APIFY_API_TOKEN` 必須設定
   - `SERPER_API_KEY` 必須設定

2. **效能目標**:
   - 推薦 API 回應時間 < 5 秒
   - Hard Filter 應在 < 100ms
   - LLM Ranking 應在 < 3 秒

3. **錯誤處理**:
   - 所有 async 函式都要有 try-except
   - JSON 解析失敗要有 fallback
   - LLM 失敗要回傳預設推薦

---

## 💡 給下一個 LLM 的提示

當您繼續開發時：

1. 先閱讀 `specs/architecture_v2_pipeline.md` 了解整體架構
2. 查看 `schemas/restaurant_profile.py` 了解資料結構
3. 按照 Task 3 → Task 4 → Task 5-7 → Task 8 的順序實作
4. 每完成一個 Task 就測試一次
5. 遇到問題先查看 Cloud Run 日誌

**祝開發順利！** 🎉
