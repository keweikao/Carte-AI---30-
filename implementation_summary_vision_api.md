# Vision API Fallback 實作摘要

**實作日期**: 2025-12-02
**狀態**: ✅ 已完成（未部署）

## 📋 實作概述

根據 `staging_test_report.md` 的分析結果，實作了完整的 Vision API fallback 機制來解決菜單抓取失敗的核心問題。

## 🎯 解決的問題

### 問題 1: 菜單抓取失敗（0% 成功率）
**Before**: `vision_api_fallback()` 只是 placeholder，回傳固定的 "Fallback Dish"
**After**: 完整實作圖片抓取 + Gemini Vision OCR 菜單提取

### 問題 2: 地址顯示 "Address placeholder"
**Before**: 硬編碼的 "Address placeholder"
**After**: 從 Apify 抓取真實餐廳地址

### 問題 3: Pydantic 序列化警告
**Before**: `ai_insight` 被設定為 dict
**After**: 正確創建 `MenuItemAnalysis` 物件

### 問題 4: Gemini API 調用錯誤
**Before**: 使用不存在的 `get_default_async_client`
**After**: 使用正確的 `GenerativeModel.generate_content_async()`

## 📝 修改的檔案

### 1. `services/menu_scraper.py`

#### 新增 imports
```python
from apify_client import ApifyClientAsync
```

#### 新增環境變數
```python
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
```

#### 新增方法: `fetch_restaurant_images()`
- 使用 Apify Google Places scraper 抓取餐廳圖片
- 參數: `place_id`, `restaurant_name`, `max_images=10`
- 回傳: `List[str]` (圖片 URLs)
- 錯誤處理: 回傳空列表

**特點**:
- 使用 Apify Actor: `compass~crawler-google-places`
- 只抓取圖片，不抓取評論（`maxReviews: 0`）
- 支援最多 10 張圖片（可調整）

#### 新增方法: `extract_menu_from_images()`
- 使用 Gemini Vision API 從圖片提取菜單
- 參數: `image_urls: List[str]`
- 回傳: `List[MenuItem]`

**流程**:
1. 限制處理前 5 張圖片（避免過高 API 成本）
2. 下載圖片（使用 httpx AsyncClient）
3. 準備 Gemini Vision prompt
4. 發送圖片 + prompt 給 Gemini 2.0 Flash
5. 解析 JSON 回應並轉換為 MenuItem 物件

**Prompt 設計重點**:
- 只提取**同時有菜名和價格**的項目
- 自動推斷分類（飯類、麵點、湯品等）
- 過濾非菜單圖片（如餐廳外觀、食物照片）
- 跳過模糊不清的文字

#### 更新方法: `vision_api_fallback()`
**Before**:
```python
async def vision_api_fallback(self, place_id: str) -> List[MenuItem]:
    print(f"Using Vision API fallback for {place_id} (placeholder)...")
    return [MenuItem(name="Fallback Dish", price=120, category="Special", source_type="estimated")]
```

**After**:
```python
async def vision_api_fallback(self, place_id: str, restaurant_name: str = "") -> List[MenuItem]:
    # Step 1: Fetch images from Apify
    image_urls = await self.fetch_restaurant_images(place_id, restaurant_name)

    if not image_urls:
        return [MenuItem(...)]  # Fallback

    # Step 2: Extract menu from images using Gemini Vision
    menu_items = await self.extract_menu_from_images(image_urls)

    if not menu_items:
        return [MenuItem(...)]  # Fallback

    return menu_items
```

#### 修復: `extract_menu_with_gemini()`
**Before**: 使用不存在的 API
```python
async with genai.get_default_async_client(api_key=GEMINI_API_KEY) as aclient:
    response = await aclient.models.generate_content(...)
```

**After**: 使用正確的 API
```python
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')
response = await model.generate_content_async(prompt)
```

---

### 2. `services/restaurant_aggregator.py`

#### 更新: `get_restaurant_data()`

**地址處理**:
```python
# Before
address="Address placeholder"

# After
restaurant_address = "Address not available"  # Default
try:
    restaurant_address = await _fetch_restaurant_address(place_id, name)
except Exception as e:
    print(f"Could not fetch restaurant address: {e}")
    restaurant_address = "Address not available"
```

**Vision API fallback 調用**:
```python
# Before
menu_items = await scraper.vision_api_fallback(place_id)

# After
menu_items = await scraper.vision_api_fallback(place_id, name)
```

#### 新增輔助函數: `_fetch_restaurant_address()`
- 使用 Apify 抓取餐廳地址
- 獨立的 API 調用（不抓取評論或圖片）
- 錯誤處理: 回傳 "Address not available"

**實作細節**:
```python
async def _fetch_restaurant_address(place_id: str, restaurant_name: str) -> str:
    client = ApifyClientAsync(APIFY_API_TOKEN)
    actor_call = await client.actor("compass~crawler-google-places").call(
        run_input={
            "searchStringsArray": [restaurant_name],
            "maxImages": 0,
            "maxReviews": 0,
            "language": "zh-TW",
        }
    )
    # Extract address from result
    ...
```

---

### 3. `services/review_analyzer.py`

#### 新增 import
```python
from schemas.restaurant_profile import MenuItem, MenuItemAnalysis
```

#### 修復: `analyze_and_fuse_reviews()`

**Before**: 使用 dict
```python
menu_item.ai_insight = {
    "sentiment": analysis.get("sentiment", "neutral"),
    "summary": analysis.get("summary", ""),
    "mention_count": analysis.get("mention_count", 0)
}
```

**After**: 創建 Pydantic 物件
```python
menu_item.ai_insight = MenuItemAnalysis(
    sentiment=analysis.get("sentiment", "neutral"),
    summary=analysis.get("summary", ""),
    mention_count=analysis.get("mention_count", 0)
)
```

**效果**: 消除 Pydantic 序列化警告

---

## 🔄 資料流程

### Cold Start 完整流程（更新後）

```
1. API Request
   ↓
2. Cache Check (Firestore)
   ↓ (miss)
3. Menu Extraction
   ├─ Try: Serper → Jina → Gemini (text)
   │   ├─ Success → trust_level: "high"
   │   └─ Fail ↓
   └─ Fallback: Apify (images) → Gemini Vision
       ├─ Success → trust_level: "medium"
       └─ Fail → Placeholder dish
   ↓
4. Review Analysis
   ├─ Apify (fetch reviews)
   └─ Gemini (analyze & fuse)
   ↓
5. Address Fetching
   └─ Apify (fetch address)
   ↓
6. Create RestaurantProfile
   ├─ place_id
   ├─ name
   ├─ address (from Apify)
   ├─ trust_level (high/medium)
   ├─ menu_items (with ai_insight)
   └─ review_summary
   ↓
7. Save to Firestore
   ↓
8. Return to Client
```

---

## 🎨 Vision API Prompt 設計

### 關鍵策略

1. **嚴格篩選**: 只提取同時有菜名和價格的項目
2. **智能分類**: 自動推斷分類（飯類、麵點、湯品等）
3. **品質控制**:
   - 過濾非菜單圖片
   - 跳過模糊文字
   - 忽略只有標題沒有內容的區塊

### Prompt 結構

```
You are an expert at reading restaurant menus from photos.

For each menu item you can clearly see, provide:
- name: 菜品名稱
- price: 價格（整數，不清楚則 null）
- category: 分類（飯類、麵點、湯品等）
- description: 描述（可選）
- source_type: "dine_in"

IMPORTANT:
- Only extract items where BOTH name AND price are visible
- Skip section headers without items
- Skip non-menu images
- Skip blurry text

Return valid JSON array. If no items, return []
```

---

## 📊 預期效果

### 菜單抓取成功率
- **Before**: 0%
- **Target**: 80%+
- **依據**: Google Maps 圖片中通常有菜單照片

### Trust Level 分布
- **high** (Serper + Jina): 官方網站菜單
- **medium** (Vision API): Google Maps 圖片 OCR ✨ 新增
- **low**: 無法取得菜單（極少數）

### API 成本
- **圖片抓取**: Apify（按使用量計費）
- **Vision API**: Gemini 2.0 Flash（經濟型）
  - 限制最多 5 張圖片/次
  - 避免過高成本

---

## ⚠️ 已知限制

1. **圖片品質依賴**:
   - 如果 Google Maps 沒有清晰的菜單照片，仍會失敗
   - 解決方案: 回傳 "Fallback Dish"

2. **OCR 準確度**:
   - 手寫菜單可能辨識困難
   - 特殊字體或排版可能影響準確度

3. **成本考量**:
   - 每次 cold start 都會調用 Vision API
   - 目前限制 5 張圖片來控制成本

4. **重複 Apify 調用**:
   - 目前地址、評論、圖片是分開調用的
   - 優化空間: 合併為單次調用

---

## 🔧 後續優化建議

### 短期（本週）

1. **合併 Apify 調用**
   - 一次調用同時取得：圖片、評論、地址
   - 減少 API 調用次數和等待時間

2. **增加日誌**
   - 記錄每個步驟的成功/失敗
   - 追蹤 Vision API 的準確度

3. **錯誤處理增強**
   - 更細緻的異常處理
   - 區分不同失敗原因

### 中期（下週）

4. **A/B 測試**
   - 比較 Vision API vs Serper+Jina 的成功率
   - 評估不同 prompt 的效果

5. **快取優化**
   - Vision API 結果可快取
   - 避免重複處理相同圖片

6. **品質評分**
   - 對提取的菜單項目評分
   - 過濾低可信度項目

### 長期（未來）

7. **多模型比較**
   - 嘗試其他 Vision models
   - 選擇最佳性價比方案

8. **人工驗證流程**
   - 對 trust_level: "medium" 的資料
   - 建立人工審核機制

---

## ✅ 測試檢查清單

在部署前需要測試：

- [ ] `fetch_restaurant_images()` 成功抓取圖片
- [ ] `extract_menu_from_images()` 正確提取菜單
- [ ] `vision_api_fallback()` 完整流程運作
- [ ] `_fetch_restaurant_address()` 取得地址
- [ ] `ai_insight` 正確創建為物件（無 Pydantic 警告）
- [ ] Cold Start 完整流程端到端測試
- [ ] 錯誤情境處理（無圖片、無菜單等）
- [ ] API 成本在可接受範圍內

---

## 📦 Commit 記錄

實作分為以下 commits（未推送）：

1. `feat: implement Vision API fallback with Apify image fetching`
2. `feat: add Gemini Vision OCR for menu extraction`
3. `fix: update restaurant_aggregator to fetch real address`
4. `fix: correct ai_insight type to MenuItemAnalysis object`
5. `fix: use correct Gemini API for all text generation`

---

## 🚀 部署建議

**部署時機**: 在本地完成以下測試後再部署
1. 單元測試通過
2. 整合測試通過
3. 成本評估完成

**部署步驟**:
```bash
# 1. 提交所有變更
git add services/menu_scraper.py services/restaurant_aggregator.py services/review_analyzer.py
git commit -m "feat: implement complete Vision API fallback system"

# 2. 部署到 staging
gcloud builds submit --config=cloudbuild.yaml --project=gen-lang-client-0415289079

# 3. 測試新餐廳（觸發 cold start）
curl "https://oderwhat-staging-u33peegeaa-de.a.run.app/api/v1/restaurant/{place_id}?name={name}"

# 4. 檢查日誌
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=oderwhat-staging"
```

---

**實作完成時間**: 約 1 小時
**預計測試時間**: 30 分鐘
**預計部署時間**: 5 分鐘

**總結**: 所有核心問題已修復，等待測試和部署。
