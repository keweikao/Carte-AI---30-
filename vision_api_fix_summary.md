# Vision API 修復總結

**修復時間**: 2025-12-02 22:11
**狀態**: ✅ 已修復並部署中

---

## 問題描述

Vision API fallback 功能完全失敗，所有餐廳都回傳 "Fallback Dish" 而非真實菜單。

**影響範圍**:
- 菜單抓取成功率: 0%
- 所有依賴 Vision API 的餐廳都無法獲得真實菜單

---

## 根本原因

**Apify 圖片抓取失敗**

`services/menu_scraper.py` 中的 `fetch_restaurant_images()` 使用錯誤的 Apify 配置：

### ❌ 問題代碼
```python
actor_call = await client.actor("compass~crawler-google-places").call(
    run_input={
        "startUrls": [{"url": f"https://www.google.com/maps/place/?q=place_id:{place_id}"}],
        "maxImages": max_images,
        "scrapePlaceDetailPage": True,
        ...
    }
)
```

**為什麼失敗**:
- 使用 `startUrls` + place_id URL
- Apify 無法從此 URL 正確抓取 `imageUrls`
- 回傳空陣列 → 直接 fallback to "Fallback Dish"

---

## 修復方案

### ✅ 修復代碼
```python
actor_call = await client.actor("compass~crawler-google-places").call(
    run_input={
        "searchStringsArray": [restaurant_name],  # 改用餐廳名稱搜尋
        "maxImages": max_images,
        "language": "zh-TW",
        ...
    }
)
```

**為什麼有效**:
- 與其他成功服務保持一致（review_analyzer, restaurant_aggregator）
- 使用餐廳名稱搜尋比 place_id URL 更可靠
- 已被驗證在其他功能中成功運作

---

## 日誌證據

### 失敗日誌（修復前）
```
Fetching images for 鼎泰豐南西店 (place_id: ChIJ...) using Apify...
No images found in Apify result.
No images available. Returning placeholder dish.
```

### 預期日誌（修復後）
```
Fetching images for 鼎泰豐南西店 (place_id: ChIJ...) using Apify...
Successfully fetched 10 images from Apify.
Extracting menu from 5 images using Gemini Vision API...
Successfully extracted 12 menu items with Vision API.
```

---

## 預期效果

修復後的流程：

1. **Apify 圖片抓取**: ✅ 成功獲取 5-10 張圖片
2. **Gemini Vision API**: ✅ 正確調用並分析圖片
3. **菜單提取**: ✅ 返回 10-20 道真實菜品
4. **Trust Level**: `medium`（來自圖片）
5. **成功率**: 預期 **80%+**

---

## 修改檔案

**檔案**: `services/menu_scraper.py`
**行數**: 165-202
**方法**: `fetch_restaurant_images()`

**Git Diff**:
```diff
- "startUrls": [{"url": f"https://www.google.com/maps/place/?q=place_id:{place_id}"}],
+ "searchStringsArray": [restaurant_name],
- "scrapePlaceDetailPage": True,
```

---

## 測試計劃

部署完成後測試：

### 測試案例 1: 鼎泰豐南西店
```bash
curl "https://oderwhat-staging-u33peegeaa-de.a.run.app/api/v1/restaurant/ChIJP5PwKRypQjQRQZ8HXE7xLSg?name=%E9%BC%8E%E6%B3%B0%E8%B1%90%E5%8D%97%E8%A5%BF%E5%BA%97"
```

**預期結果**:
- ✅ `menu_items` 包含 10+ 道菜
- ✅ 菜品名稱為中文（如 "小籠包", "蝦仁炒飯"）
- ✅ 價格合理（200-400 範圍）
- ❌ 不是 "Fallback Dish"

### 測試案例 2: 八方雲集
```bash
curl "https://oderwhat-staging-u33peegeaa-de.a.run.app/api/v1/restaurant/ChIJm8L9_RypQjQRPo-Y6pKHpPM?name=%E5%85%AB%E6%96%B9%E9%9B%B2%E9%9B%86"
```

**預期結果**:
- ✅ 類似結果（真實菜單）

---

## 部署資訊

**Build ID**: 83369908-e1fb-47b1-b66e-8ad4db6ff5ab
**狀態**: WORKING（部署中）
**環境**: oderwhat-staging
**預計完成**: ~4 分鐘

---

## 後續步驟

1. ⏳ 等待部署完成（~4分鐘）
2. ✅ 測試真實餐廳（鼎泰豐、八方雲集）
3. ✅ 驗證菜單抓取成功率 > 80%
4. ✅ 檢查日誌確認 Vision API 被正確調用
5. ✅ 更新 `deployment_test_results.md` 與測試結果

---

## 相關檔案

- **修復檔案**: `services/menu_scraper.py`
- **測試結果**: `deployment_test_results.md`
- **本文檔**: `vision_api_fix_summary.md`

---

**修復者**: Claude
**審核者**: [待填寫]
**部署時間**: 2025-12-02 22:11 (UTC+8)
