# OderWhat 現況規格書（As-Built Specification）

**版本**: 2.0 (Current Implementation)
**日期**: 2025-11-24
**狀態**: ✅ MVP 已上線運作

---

## 📋 目錄

1. [專案概述](#專案概述)
2. [技術架構](#技術架構)
3. [已實作功能](#已實作功能)
4. [API 規格](#api-規格)
5. [資料結構](#資料結構)
6. [前端實作](#前端實作)
7. [後端實作](#後端實作)
8. [部署架構](#部署架構)
9. [Token 優化系統](#token-優化系統)
10. [待開發功能](#待開發功能)

---

## 專案概述

### 核心價值

**解決消費者在陌生餐廳的點餐決策癱瘓**，透過 AI 分析 Google 評論與網路資訊，提供結構化的最佳點餐建議。

### 目標用戶

- 👥 多人聚餐需要分食建議
- 🍽️ 個人用餐想快速決定
- 🎯 第一次去餐廳不知道點什麼
- 💰 想在預算內吃到最好的組合

### 產品定位

**AI 點餐經紀人** - 你的私人點餐顧問

---

## 技術架構

### Tech Stack

```
前端：Next.js 14 + TypeScript + Tailwind CSS
後端：FastAPI + Python 3.11
AI：Google Gemini Flash (gemini-flash-latest)
資料庫：Firestore (GCP)
認證：NextAuth.js + Google OAuth
部署：Google Cloud Run
金流：TapPay（規劃中）
```

### 系統架構圖

```
┌─────────────────────────────────────────────────┐
│        Frontend (Next.js 14)                     │
│  • Landing Page (/)                              │
│  • Input Form (/input)                           │
│  • Recommendation Result (/recommendation)       │
│  • Google OAuth Login                            │
└──────────────────┬──────────────────────────────┘
                   │ HTTPS + Bearer Token
┌──────────────────▼──────────────────────────────┐
│        Backend API (FastAPI)                     │
│  • POST /recommendations                         │
│  • POST /feedback                                │
│  • GET /health                                   │
│  • Google Token Verification                     │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌────────▼─────────┐
│   Firestore    │   │   External APIs  │
│  • users       │   │  • Google Places │
│  • restaurants │   │  • Google Search │
│                │   │  • Gemini API    │
└────────────────┘   └──────────────────┘
```

### 資料流程

```
1. 使用者登入（Google OAuth）
   ↓
2. 輸入餐廳資訊 + 條件
   ↓
3. 後端檢查 Firestore 快取
   ↓ (Cache Miss)
4. 並行抓取：
   • Google Places API → 評論
   • Google Search API → 菜單資訊
   ↓
5. 儲存到 Firestore (30天TTL)
   ↓
6. 建構 Prompt + RAG
   ↓
7. 呼叫 Gemini API
   ↓
8. 解析 JSON 回應
   ↓
9. 前端渲染推薦結果
   ↓
10. 使用者可一鍵換菜（前端）
    ↓
11. 使用者提交反饋（儲存到 Firestore）
```

---

## 已實作功能

### ✅ 核心功能（MVP）

#### 1. 使用者認證
- ✅ Google OAuth 登入
- ✅ NextAuth.js 整合
- ✅ Bearer Token 驗證
- ✅ 使用者 session 管理

#### 2. 輸入表單
- ✅ 兩階段表單（餐廳 → 條件）
- ✅ 餐廳名稱輸入
- ✅ 用餐模式選擇（分食 / 個人）
- ✅ 人數選擇（動態調整）
- ✅ 預算輸入（人均 / 總預算）
- ✅ 飲食限制文字輸入
- ✅ 流暢的 UX 動畫（Framer Motion）

#### 3. AI 推薦生成
- ✅ Google Places API 整合
- ✅ Google Search API 整合
- ✅ Firestore 快取機制（30天）
- ✅ Gemini Flash API 整合
- ✅ Structured JSON Output
- ✅ RAG（Retrieval-Augmented Generation）
- ✅ 使用者偏好記憶（Firestore）

#### 4. 推薦結果展示
- ✅ 推薦卡片顯示
- ✅ 菜色名稱 + 價格 + 推薦理由
- ✅ 總價顯示
- ✅ 一鍵換菜功能（前端切換 alternatives）
- ✅ 招牌菜標示
- ✅ 點餐專用卡（Waiter Card）

#### 5. 反饋系統
- ✅ 評分機制（1-5星）
- ✅ 文字評論
- ✅ 選擇實際點的菜色
- ✅ 儲存到 Firestore users.feedback_history

#### 6. Token 優化系統（新增）
- ✅ API 快取系統（api_cache_minimal.py）
- ✅ Token 優化器（token_optimizer_minimal.py）
- ✅ 檔案參考機制（90%+ token 節省）
- ✅ 自動快取管理
- ✅ 統計追蹤

---

## API 規格

### 基礎資訊

- **Base URL**: `https://api.carte.tw` (Production)
- **Base URL**: `http://localhost:8000` (Development)
- **認證方式**: Bearer Token (Google ID Token)
- **Content-Type**: `application/json`

### API Endpoints

#### 1. POST /recommendations

**描述**: 生成餐廳推薦

**Headers**:
```http
Authorization: Bearer {google_id_token}
Content-Type: application/json
```

**Request Body**:
```json
{
  "restaurant_name": "鼎泰豐",
  "mode": "sharing",
  "people": 4,
  "budget": "500",
  "dietary_restrictions": "不吃牛、不吃辣"
}
```

**Request Schema**:
```python
class RecommendationRequest(BaseModel):
    restaurant_name: str              # 餐廳名稱
    mode: Literal["sharing", "individual"]  # 用餐模式
    people: int                       # 人數 (> 0)
    budget: str                       # 預算描述
    dietary_restrictions: Optional[str]     # 飲食限制
    user_id: Optional[str]            # 使用者 ID（自動注入）
```

**Response** (200 OK):
```json
{
  "recommendation_id": "550e8400-e29b-41d4-a716-446655440000",
  "restaurant_name": "鼎泰豐",
  "total_estimated_price": 2000,
  "currency": "TWD",
  "summary": "為 4 位共享用餐者推薦的經典組合，包含招牌小籠包...",
  "recommendations": [
    {
      "id": "dish_001",
      "name": "小籠包",
      "price": 220,
      "reason": "45則評論提到「皮薄餡多」，招牌必點",
      "type": "Appetizer",
      "is_signature": true,
      "alternatives": [
        {
          "id": "dish_002",
          "name": "蝦仁炒飯",
          "price": 250,
          "reason": "粒粒分明，適合分食",
          "type": "Main",
          "is_signature": false,
          "alternatives": []
        }
      ]
    }
  ],
  "user_info": {
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

**Error Responses**:

- **401 Unauthorized**: Token 無效或過期
```json
{
  "detail": "Invalid or expired token"
}
```

- **503 Service Unavailable**: Gemini API 設定錯誤
```json
{
  "detail": "服務設定錯誤：Gemini API Key is not configured"
}
```

- **502 Bad Gateway**: Gemini API 呼叫失敗
```json
{
  "detail": "推薦生成失敗：Gemini API error"
}
```

#### 2. POST /feedback

**描述**: 提交使用者反饋

**Headers**:
```http
Authorization: Bearer {google_id_token}
Content-Type: application/json
```

**Request Body**:
```json
{
  "recommendation_id": "550e8400-e29b-41d4-a716-446655440000",
  "rating": 5,
  "selected_items": ["小籠包", "蝦仁炒飯"],
  "comment": "推薦很準確，都很好吃！"
}
```

**Request Schema**:
```python
class FeedbackRequest(BaseModel):
    recommendation_id: str          # 推薦 ID
    rating: int                     # 評分 1-5
    selected_items: List[str]       # 實際點的菜色
    comment: Optional[str]          # 文字評論
```

**Response** (200 OK):
```json
{
  "status": "success",
  "message": "Feedback received"
}
```

#### 3. GET /health

**描述**: 健康檢查

**Response** (200 OK):
```json
{
  "status": "ok"
}
```

---

## 資料結構

### Firestore Collections

#### users/{user_id}

```typescript
{
  // Google OAuth 資訊
  user_id: string,           // Google sub
  email: string,
  name: string,
  picture: string | null,
  created_at: timestamp,
  last_login: timestamp,

  // 反饋歷史（味覺記憶）
  feedback_history: [
    {
      recommendation_id: string,
      rating: number,
      selected_items: string[],
      comment: string,
      timestamp: timestamp,
      restaurant_name: string
    }
  ],

  // Token 優化統計（可選）
  optimization_stats: {
    total_saved_tokens: number,
    last_updated: timestamp
  }
}
```

**索引**:
- `email` (單一欄位)
- `created_at` (單一欄位)

#### restaurants/{restaurant_id}

```typescript
{
  // 餐廳基本資訊
  name: string,              // 餐廳名稱

  // Google Places 資料
  reviews_data: {
    rating: number,
    user_ratings_total: number,
    reviews: [
      {
        author_name: string,
        rating: number,
        text: string,
        time: number
      }
    ]
  },

  // 菜單資訊（Google Search）
  menu_text: string,         // 從搜尋結果提取的菜單文字

  // 快取管理
  updated_at: timestamp,     // 最後更新時間
  cache_expires_at: timestamp  // 快取過期時間（30天後）
}
```

**索引**:
- `name` (單一欄位)
- `updated_at` (單一欄位)

**Document ID**: MD5(restaurant_name.lower().strip())

---

## 前端實作

### 技術棧

```
Framework: Next.js 14 (App Router)
Language: TypeScript
Styling: Tailwind CSS + shadcn/ui
Animation: Framer Motion
Auth: NextAuth.js
State Management: React Hooks (useState, useEffect)
HTTP Client: Fetch API
```

### 頁面結構

```
src/
├── app/
│   ├── page.tsx                    # Landing Page（首頁）
│   ├── input/
│   │   └── page.tsx                # 輸入表單頁面
│   └── recommendation/
│       └── page.tsx                # 推薦結果頁面
│
├── components/
│   ├── ui/                         # shadcn/ui 元件
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   ├── AuthProvider.tsx            # NextAuth Provider
│   └── LoginButton.tsx             # Google 登入按鈕
│
└── lib/
    └── auth.ts                     # NextAuth 設定
```

### 核心頁面

#### 1. Landing Page (/)

**功能**:
- ✅ 產品介紹
- ✅ Google 登入按鈕
- ✅ 特色說明
- ✅ CTA（Call to Action）

**流程**:
```
未登入 → 顯示登入按鈕
已登入 → 自動導向 /input
```

#### 2. Input Form (/input)

**功能**:
- ✅ 兩階段表單設計
  - Step 1: 餐廳名稱
  - Step 2: 用餐條件
- ✅ 動態表單驗證
- ✅ 流暢的過場動畫
- ✅ 預算計算（人均/總預算切換）

**表單欄位**:
```typescript
{
  restaurant_name: string,        // 必填
  mode: "sharing" | "individual", // 預設 "sharing"
  people: number,                 // 預設 2，範圍 1-20
  budget: string,                 // 金額或描述
  dietary_restrictions: string    // 可選
}
```

**驗證規則**:
- 餐廳名稱不可為空
- 人數必須 > 0
- 預算為可選，但建議填寫

#### 3. Recommendation Result (/recommendation)

**功能**:
- ✅ Loading 狀態（呼叫 API 時）
- ✅ 推薦卡片展示
- ✅ 一鍵換菜（alternatives 切換）
- ✅ 點餐專用卡（Waiter Card）
- ✅ 反饋表單

**卡片設計**:
```tsx
<RecommendationCard>
  <DishName>小籠包</DishName>
  <Price>NT$ 220</Price>
  <Reason>45則評論提到「皮薄餡多」</Reason>
  {is_signature && <Badge>招牌</Badge>}
  {alternatives.length > 0 && <SwapButton />}
</RecommendationCard>
```

**一鍵換菜邏輯**:
```typescript
const handleSwap = (dishId: string) => {
  const dish = recommendations.find(d => d.id === dishId);
  if (dish?.alternatives?.length > 0) {
    const newDish = dish.alternatives[0];
    // 替換當前菜色（純前端操作，不呼叫 API）
    setRecommendations(prev =>
      prev.map(d => d.id === dishId ? newDish : d)
    );
  }
};
```

---

## 後端實作

### 技術棧

```
Framework: FastAPI 0.104+
Language: Python 3.11
ASGI Server: Uvicorn
Database: Firestore
Auth: Google OAuth (Token Verification)
AI: Google Gemini Flash
APIs: Google Places API, Custom Search JSON API
```

### 專案結構

```
OderWhat/
├── main.py                         # FastAPI 應用程式入口
├── agent/
│   ├── dining_agent.py             # 核心 Agent 邏輯
│   ├── data_fetcher.py             # 資料抓取（Places, Search）
│   └── prompt_builder.py           # Prompt 建構器
├── schemas/
│   ├── recommendation.py           # Pydantic Schemas
│   └── feedback.py
├── services/
│   ├── firestore_service.py        # Firestore 操作
│   ├── subscription_service.py     # 訂閱服務（待開發）
│   └── payment_service.py          # 付款服務（待開發）
├── auth/
│   └── google_auth.py              # Google Token 驗證
├── middleware/
│   └── usage_limit.py              # 使用量限制（待開發）
├── integrations/
│   └── tappay.py                   # TapPay 整合（待開發）
└── api_cache_minimal.py            # API 快取系統
└── token_optimizer_minimal.py      # Token 優化器
```

### 核心模組

#### 1. main.py - FastAPI 應用

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas.recommendation import RecommendationRequest, FullRecommendationResponse
from schemas.feedback import FeedbackRequest
from agent.dining_agent import DiningAgent
from auth.google_auth import verify_google_token
from services.firestore_service import update_user_profile

app = FastAPI(title="AI Dining Agent API", version="1.0")

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://dining-frontend-*.run.app",
        "https://www.carte.tw"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Google Auth Dependency
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return verify_google_token(token)

# Initialize Agent
agent = DiningAgent()

@app.post("/recommendations", response_model=FullRecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest,
    user_info: dict = Depends(get_current_user)
):
    # 注入 user_id
    request.user_id = user_info.get("sub")

    # 生成推薦
    response = await agent.get_recommendations(request)

    # 注入 user_info
    response.user_info = {
        "email": user_info.get("email"),
        "name": user_info.get("name")
    }

    return response

@app.post("/feedback")
async def submit_feedback(
    feedback: FeedbackRequest,
    user_info: dict = Depends(get_current_user)
):
    user_id = user_info.get("sub")
    update_user_profile(user_id, feedback.dict())
    return {"status": "success", "message": "Feedback received"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

#### 2. agent/dining_agent.py - 核心推薦邏輯

```python
import asyncio
import uuid
import google.generativeai as genai
from schemas.recommendation import RecommendationRequest, FullRecommendationResponse
from agent.data_fetcher import fetch_place_details, fetch_menu_from_search
from agent.prompt_builder import create_prompt_for_gemini
from services.firestore_service import get_cached_data, save_restaurant_data, get_user_profile

class DiningAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-flash-latest')

    async def get_recommendations(self, request: RecommendationRequest) -> FullRecommendationResponse:
        # 1. 檢查快取
        cached_data = get_cached_data(request.restaurant_name)

        if cached_data:
            reviews_data = cached_data.get("reviews_data", {})
            menu_text = cached_data.get("menu_text", "")
        else:
            # 2. 並行抓取資料
            reviews_task = fetch_place_details(request.restaurant_name)
            menu_task = fetch_menu_from_search(request.restaurant_name)
            reviews_data, menu_text = await asyncio.gather(reviews_task, menu_task)

            # 3. 儲存快取
            save_restaurant_data(request.restaurant_name, reviews_data, menu_text)

        # 4. 取得使用者偏好
        user_profile = {}
        if request.user_id:
            user_profile = get_user_profile(request.user_id)

        # 5. 建構 Prompt
        prompt = create_prompt_for_gemini(request, reviews_data, menu_text, user_profile)

        # 6. 呼叫 Gemini（含重試）
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                response = await asyncio.to_thread(
                    self.model.generate_content,
                    prompt,
                    generation_config={"response_mime_type": "application/json"}
                )

                data = json.loads(response.text.strip())
                data["recommendation_id"] = str(uuid.uuid4())

                # 7. 確保每個 item 都有 alternatives
                for item in data.get("recommendations", []):
                    if not item.get("alternatives"):
                        item["alternatives"] = []

                return FullRecommendationResponse(**data)

            except Exception as e:
                if attempt < max_retries:
                    await asyncio.sleep(1)
                    continue
                raise RuntimeError(f"Gemini API 失敗: {str(e)}")
```

#### 3. services/firestore_service.py - 資料庫操作

```python
from google.cloud import firestore
import hashlib
import datetime

db = firestore.Client(database="carted-data")

COLLECTION_NAME = "restaurants"
CACHE_DURATION_DAYS = 30

def _get_doc_id(restaurant_name: str) -> str:
    """產生一致的 document ID"""
    return hashlib.md5(restaurant_name.lower().strip().encode()).hexdigest()

def get_cached_data(restaurant_name: str) -> dict:
    """取得快取資料（若存在且未過期）"""
    doc_id = _get_doc_id(restaurant_name)
    doc_ref = db.collection(COLLECTION_NAME).document(doc_id)

    try:
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            updated_at = data.get("updated_at")

            if updated_at:
                now = datetime.datetime.now(datetime.timezone.utc)
                if (now - updated_at).days < CACHE_DURATION_DAYS:
                    return data
    except Exception as e:
        print(f"Firestore 讀取錯誤: {e}")

    return None

def save_restaurant_data(restaurant_name: str, reviews_data: dict, menu_text: str):
    """儲存餐廳資料到 Firestore"""
    doc_id = _get_doc_id(restaurant_name)
    doc_ref = db.collection(COLLECTION_NAME).document(doc_id)

    data = {
        "name": restaurant_name,
        "reviews_data": reviews_data,
        "menu_text": menu_text,
        "updated_at": datetime.datetime.now(datetime.timezone.utc)
    }

    try:
        doc_ref.set(data)
    except Exception as e:
        print(f"Firestore 寫入錯誤: {e}")

def get_user_profile(user_id: str) -> dict:
    """取得使用者檔案（偏好記憶）"""
    try:
        doc = db.collection("users").document(user_id).get()
        if doc.exists:
            return doc.to_dict()
    except Exception as e:
        print(f"取得使用者檔案錯誤: {e}")

    return {}

def update_user_profile(user_id: str, feedback_data: dict):
    """更新使用者檔案（反饋記錄）"""
    doc_ref = db.collection("users").document(user_id)

    try:
        doc_ref.set({
            "feedback_history": firestore.ArrayUnion([feedback_data]),
            "last_updated": datetime.datetime.now(datetime.timezone.utc)
        }, merge=True)
    except Exception as e:
        print(f"更新使用者檔案錯誤: {e}")
```

---

## 部署架構

### Google Cloud Platform

**服務使用**:
- ✅ **Cloud Run** - 後端 API 部署
- ✅ **Cloud Run** - 前端部署
- ✅ **Firestore** - NoSQL 資料庫
- ✅ **Cloud Build** - CI/CD
- ✅ **Secret Manager** - 環境變數管理

### 環境變數

#### 後端 (.env)

```bash
# Google API
GEMINI_API_KEY=AIza...
GOOGLE_PLACES_API_KEY=AIza...
GOOGLE_SEARCH_API_KEY=AIza...
GOOGLE_SEARCH_ENGINE_ID=...

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json

# NextAuth（前端需要）
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
NEXTAUTH_SECRET=...
NEXTAUTH_URL=https://www.carte.tw

# TapPay（待開發）
TAPPAY_PARTNER_KEY=...
TAPPAY_MERCHANT_ID=...
TAPPAY_APP_ID=...
TAPPAY_APP_KEY=...
```

### 部署指令

#### 後端部署

```bash
gcloud run deploy oderwhat-api \
  --source . \
  --region asia-east1 \
  --allow-unauthenticated \
  --set-env-vars="GEMINI_API_KEY=$GEMINI_API_KEY,..."
```

#### 前端部署

```bash
cd frontend
npm run build
gcloud run deploy oderwhat-frontend \
  --source . \
  --region asia-east1 \
  --allow-unauthenticated
```

---

## Token 優化系統

### 已實作模組

#### 1. api_cache_minimal.py - API 快取

**功能**:
- ✅ 自動快取 API 結果
- ✅ TTL 機制（預設 1 小時）
- ✅ MD5 雜湊鍵
- ✅ 統計追蹤（命中率）

**使用方式**:
```python
from api_cache_minimal import APICache

cache = APICache(cache_dir="temp/api_cache", default_ttl_hours=1)

# 快取 API 呼叫
result = cache.get_or_call(
    cache_key="鼎泰豐",
    api_function=search_restaurant,
    ttl_hours=1
)

# 檢視統計
stats = cache.get_stats()
# {'hits': 3, 'misses': 1, 'hit_rate': '75.0%'}
```

#### 2. token_optimizer_minimal.py - Token 優化

**功能**:
- ✅ 大型資料（>1000字元）存為檔案
- ✅ 返回檔案參考（節省 90%+ token）
- ✅ 自動管理快取目錄
- ✅ Token 節省統計

**使用方式**:
```python
from token_optimizer_minimal import TokenOptimizer

optimizer = TokenOptimizer(threshold=1000, cache_dir="temp/cache")

# 優化大型資料
result = optimizer.optimize(large_data, source="restaurant_search")

# 若 large_data > 1000 字元
# 返回：{"file": "temp/cache/data.txt", "preview": "...", "saved_tokens": 1000}

# 若 large_data < 1000 字元
# 返回：原始 large_data
```

### 乘數效應

```
策略 1（API 快取）+ 策略 2（Token 優化）= 乘數效應

第一次查詢：
  API 呼叫 → 存快取 → Token 優化
  節省：90% token

第二次查詢：
  使用快取（無 API）→ Token 優化
  節省：100% API + 90% token + 99% 時間
```

### 效益

```
實測數據（3 次查詢）：
  • Token 節省：8,370 tokens
  • API 節省：2 次呼叫
  • 快取命中率：66.7%
  • 成本節省：~$0.25
```

**詳細文件**: `TOKEN_OPTIMIZATION.md`, `quick_start_for_ai.md`

---

## 待開發功能

### 🔜 Phase 2: 訂閱制金流

**優先級**: 高
**預計時間**: 2-3 週

#### 功能清單

- [ ] **會員方案系統**
  - [ ] 免費方案（月 3 次）
  - [ ] 基礎方案（月 30 次，NT$99）
  - [ ] 進階方案（無限次，NT$299）

- [ ] **TapPay 金流整合**
  - [ ] 首次付款（Pay by Prime）
  - [ ] 定期扣款（Pay by Card Token）
  - [ ] 更換信用卡
  - [ ] 退款機制

- [ ] **使用量管控**
  - [ ] Middleware 檢查使用次數
  - [ ] 超限時顯示升級提示
  - [ ] 月初自動重置計數

- [ ] **訂閱管理頁面**
  - [ ] 檢視當前方案
  - [ ] 使用量顯示
  - [ ] 升級/降級/取消

**規格文件**:
- `specs/tappay_subscription_spec.md` - TapPay 完整規格
- `specs/payment_subscription_spec.md` - ECPay 版本（備案）

---

### 🔜 Phase 3: 進階功能

**優先級**: 中
**預計時間**: 4-6 週

- [ ] **餐廳收藏**
  - [ ] 收藏喜歡的餐廳
  - [ ] 快速重新推薦

- [ ] **歷史記錄**
  - [ ] 查看過往推薦
  - [ ] 再次生成

- [ ] **社群分享**
  - [ ] 分享推薦結果
  - [ ] 生成美觀的分享圖

- [ ] **多語言支援**
  - [ ] 英文介面
  - [ ] 日文介面

- [ ] **進階篩選**
  - [ ] 依菜系篩選
  - [ ] 依價位範圍
  - [ ] 排除特定食材

---

## 附錄

### A. 相關文件索引

**核心規格**:
- `specs/specification.md` - 原始 MVP 規格
- `specs/current_implementation_spec.md` - 本文件（現況規格）

**Token 優化**:
- `TOKEN_OPTIMIZATION.md` - Token 優化系統說明
- `quick_start_for_ai.md` - AI 開發者指南（含優化規則）

**訂閱制規劃**:
- `specs/tappay_subscription_spec.md` - TapPay 金流規格
- `specs/payment_implementation_plan.md` - ECPay 實作計畫
- `specs/payment_quick_start.md` - ECPay 快速啟動

**部署相關**:
- `docs/deployment_guide.md` - 部署指南
- `LOCAL_SETUP.md` - 本地開發設定

### B. 環境設定

**本地開發**:
```bash
# 後端
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# 前端
cd frontend
npm install
npm run dev
```

**測試**:
```bash
# 後端測試
pytest

# Token 優化測試
python test_strategy_1_2_combined.py
python test_minimal.py
```

### C. 常見問題

**Q: 為什麼選擇 Gemini Flash 而不是 GPT-4？**
A: Gemini Flash 速度快、成本低、支援 structured output，適合 MVP

**Q: 快取為什麼是 30 天？**
A: 平衡資料新鮮度與 API 成本，餐廳資訊通常變動不大

**Q: 為什麼使用 Firestore 而不是 PostgreSQL？**
A: Firestore 無伺服器、自動擴展、與 GCP 整合良好

**Q: 一鍵換菜為什麼在前端？**
A: 避免重複呼叫 API，節省成本，回應速度快

**Q: Token 優化會影響功能嗎？**
A: 不會。LLM 會自動讀取檔案參考，使用者無感

---

**文件版本**: 2.0
**最後更新**: 2025-11-24
**狀態**: ✅ 反映實際實作
**下一步**: Phase 2 - 訂閱制金流開發
