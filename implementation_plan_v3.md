# Recommendation UX v3 - Backend Implementation Plan

> **文件類型**: Implementation Plan (How)
> **對應規格**: `specs/recommendation_ux_improvement_v3.md`
> **狀態**: 進行中

---

## 🎯 總體目標

本計畫旨在說明如何修改後端系統，以支援「推薦頁面 UX 改進 v3.0」規格中定義的「菜品槽位 (DishSlot)」與「候選菜品池 (Alternatives)」功能。

---

## 🛠️ 核心實作項目

### 1. 更新 API 回應結構

**目標**: 修改 `POST /v2/recommendations` 端點，使其回傳符合 `DishSlotResponse` 的新資料結構。

- **檔案**: `main.py`, `schemas/recommendation.py`

**修改內容**:
1.  在 `schemas/recommendation.py` 中定義新的 Pydantic 模型：
    ```python
    class MenuItem(BaseModel):
        # ... (現有欄位保持不變)
        category: str # 確保 category 欄位存在

    class DishSlotResponse(BaseModel):
        category: str
        display: MenuItem
        alternatives: List[MenuItem]

    class RecommendationResponseV2(BaseModel):
        # ... (現有欄位)
        items: List[DishSlotResponse] # 將 List[MenuItem] 改為 List[DishSlotResponse]
        category_summary: Dict[str, int] # 新增欄位
    ```
2.  在 `main.py` 中的 `/v2/recommendations` 端點，調整回傳前的資料處理，以符合 `RecommendationResponseV2` 的新結構。

---

### 2. 實作候選池生成邏輯

**目標**: 在 `DiningAgent` 中，為每個主要推薦菜品（`display`）生成一個備選菜品池（`alternatives`）。

- **檔案**: `agent/dining_agent.py`, `agent/prompt_builder.py`

**實作策略**:
1.  **擴大單次 LLM 請求數量**: 修改 `prompt_builder.py`，讓 Prompt 要求 LLM 一次生成一個更長的菜單列表（例如，20-30 道），並確保包含豐富的類別。
2.  **菜品分組與篩選**: 在 `dining_agent.py` 的 `get_recommendations_v2` 方法中：
    a.  接收到 LLM 回傳的長列表後，根據 `category` 欄位進行分組。
    b.  對每個類別，選擇一道最優菜品作為 `display`（例如，基於推薦理由、評分等）。
    c.  從同類別的其餘菜品中，選擇 2-3 道作為 `alternatives`。
    d.  **應用約束**: 篩選 `alternatives` 時，需嚴格遵守 `v3.md` 中定義的品質門檻（例如，與 `display` 菜品的價格差異不超過 100%，評分 > 3.5 星等）。
3.  **快取完整候選單**: 將 LLM 首次返回的完整菜單列表（20-30道）與 `recommendation_id` 一同存入快取（例如 Redis 或 Firestore），以供後續的動態候選 API 使用。

---

### 3. 新增動態候選 API

**目標**: 建立新端點 `GET /v2/recommendations/alternatives`，供前端在特定類別的備選池用完時呼叫，動態獲取更多候選菜品。

- **檔案**: `main.py`, `services/firestore_service.py` (或其他快取服務)

**實作細節**:
1.  **定義 API**: 在 `main.py` 中新增端點。
    ```python
    @app.get("/v2/recommendations/alternatives", response_model=List[MenuItem])
    async def get_alternatives(
        recommendation_id: str,
        category: str,
        exclude: List[str] = Query(...) # 已顯示或換掉的菜品名稱
    ):
        # ... 實作邏輯 ...
    ```
2.  **定義 Schema**: 在 `schemas/recommendation.py` 中可能需要為請求定義模型。
3.  **實作邏輯**:
    a.  根據 `recommendation_id` 從快取中讀取完整的候選菜單。
    b.  篩選出指定 `category` 的菜品。
    c.  排除掉 `exclude` 列表中的菜品。
    d.  回傳剩餘的菜品作為新的候選池。
    e.  如果快取中沒有資料，應拋出 `404 Not Found` 錯誤。

---

## 🧪 測試策略

1.  **單元測試**: 針對 `DiningAgent` 中新的候選池生成邏輯撰寫單元測試。
2.  **API 整合測試**:
    -   更新 `test_tracking_api_mock.py` 或建立 `test_ux_v3_api.py`。
    -   驗證 `POST /v2/recommendations` 回應是否包含 `items`, `display`, `alternatives`, `category_summary` 等欄位。
    -   驗證 `GET /v2/recommendations/alternatives` 是否能根據參數正確回傳篩選後的候選菜品。
    -   確保所有端點在邊界條件下（如快取未命中、無更多候選等）能正常運作。

---

## 📅 執行步驟

1.  **Schema 定義**: 完成 `schemas/recommendation.py` 的模型更新。
2.  **候選池邏輯**: 在 `agent/` 中實作候選池生成與快取邏輯。
3.  **API 修改**: 更新 `main.py` 中的 `POST /v2/recommendations` 端點。
4.  **新增 API**: 在 `main.py` 中建立 `GET /v2/recommendations/alternatives` 端點。
5.  **測試**: 撰寫並執行所有相關測試。
