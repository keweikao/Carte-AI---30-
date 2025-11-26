# 金流訂閱制 - 快速啟動指南

**給開發者的 TL;DR 版本**

---

## 🎯 核心概念

### 三種方案

```
免費方案：月 3 次，體驗用
基礎方案：月 30 次，NT$ 99/月（年繳 NT$ 990）
進階方案：無限次，NT$ 299/月（年繳 NT$ 2,990）
```

### 金流服務商

**推薦：綠界科技 ECPay**
- 手續費：2.8% + NT$5
- 支援定期定額扣款
- 完整 Python SDK

---

## 📁 新增檔案結構

```
OderWhat/
├── services/
│   ├── subscription_service.py      # 訂閱管理
│   ├── payment_service.py           # 付款處理
│   └── usage_service.py             # 使用量追蹤
│
├── routers/
│   ├── subscription.py              # 訂閱 API
│   └── payment.py                   # 付款 API
│
├── middleware/
│   └── usage_limit.py               # 使用量檢查
│
├── integrations/
│   └── ecpay.py                     # ECPay SDK 包裝
│
├── schemas/
│   ├── subscription.py              # 訂閱 Schema
│   └── payment.py                   # 付款 Schema
│
└── scheduled_tasks/
    └── subscription_renewal.py      # 定期扣款排程
```

---

## 🗄️ Firestore Schema 更新

### users/{user_id} 新增欄位

```javascript
{
  // 新增：訂閱資訊
  subscription: {
    plan_type: 'free' | 'basic' | 'pro',
    billing_cycle: 'monthly' | 'yearly' | null,
    status: 'active' | 'expired' | 'cancelled',
    current_period_end: timestamp,
    next_billing_date: timestamp | null,
    ecpay_member_id: string | null
  },

  // 新增：使用量追蹤
  usage: {
    monthly_count: number,
    monthly_limit: number,
    reset_date: timestamp
  }
}
```

### 新增 Collection：orders

```javascript
{
  order_id: string,
  user_id: string,
  plan_type: 'basic' | 'pro',
  billing_cycle: 'monthly' | 'yearly',
  amount: number,
  status: 'pending' | 'completed' | 'failed',
  ecpay_merchant_trade_no: string,
  created_at: timestamp
}
```

---

## 🔌 核心 API

### 1. 取得方案列表

```http
GET /subscriptions/plans
```

### 2. 取得當前訂閱

```http
GET /subscriptions/me
Authorization: Bearer {token}
```

### 3. 建立付款訂單

```http
POST /payment/create
Authorization: Bearer {token}
Content-Type: application/json

{
  "plan_type": "basic",
  "billing_cycle": "monthly"
}
```

### 4. ECPay 回調

```http
POST /payment/callback/ecpay
Content-Type: application/x-www-form-urlencoded

(ECPay 自動發送)
```

---

## 🔒 使用量檢查流程

### 整合到 /recommendations

```python
@app.post("/recommendations")
async def get_recommendations(
    request: RecommendationRequest,
    user_info: dict = Depends(get_current_user)
):
    user_id = user_info['sub']

    # 1. 檢查使用量
    allowed, message = await check_usage_limit(user_id)
    if not allowed:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "usage_limit_exceeded",
                "message": message,
                "upgrade_url": "/subscriptions/plans"
            }
        )

    # 2. 遞增使用次數
    increment_usage(user_id)

    # 3. 原本的推薦邏輯
    response = await agent.get_recommendations(request)
    return response
```

---

## 💳 ECPay 測試資訊

### 測試環境

- URL: https://payment-stage.ecpay.com.tw
- 測試卡號: `4311-9522-2222-2222`
- 有效期限: 任意未來日期
- CVV: 任意 3 碼

### 環境變數

```bash
ECPAY_MERCHANT_ID=2000132
ECPAY_HASH_KEY=5294y06JbISpM5x9
ECPAY_HASH_IV=v77hoKGq4kWxNNIS
ECPAY_PAYMENT_URL=https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5
```

---

## 📝 實作步驟

### Week 1: 後端基礎

1. **Day 1-2**: 建立 services + schema 設計
2. **Day 3**: 實作訂閱管理 API
3. **Day 4**: 實作使用量限制 middleware
4. **Day 5-7**: ECPay 整合 + 測試

### Week 2: 金流測試

1. **Day 8-10**: 完整付款流程測試
2. **Day 11-12**: 定期扣款實作
3. **Day 13-14**: 壓力測試 + 修復

### Week 3: 前端整合

1. **Day 15-16**: 方案選擇頁面
2. **Day 17-18**: 訂閱管理頁面
3. **Day 19-20**: 使用量顯示 + 提示
4. **Day 21**: 整合與調整

### Week 4: 上線

1. **Day 22-23**: 完整測試
2. **Day 24**: 正式環境部署
3. **Day 25**: 監控與調整

---

## 🚀 立即開始

### 1. 申請 ECPay 測試帳號

前往：https://www.ecpay.com.tw/
填寫測試帳號申請表

### 2. 建立第一個 Service

```bash
touch services/subscription_service.py
```

```python
# services/subscription_service.py
from google.cloud import firestore

db = firestore.Client(database="carted-data")

class SubscriptionService:
    @staticmethod
    def get_user_subscription(user_id: str) -> dict:
        """取得使用者訂閱資訊"""
        doc = db.collection('users').document(user_id).get()
        if doc.exists:
            return doc.to_dict().get('subscription', {})
        return {}

    @staticmethod
    def create_subscription(user_id: str, plan: str, cycle: str):
        """建立訂閱"""
        from datetime import datetime, timedelta

        db.collection('users').document(user_id).set({
            'subscription': {
                'plan_type': plan,
                'billing_cycle': cycle,
                'status': 'active',
                'current_period_start': datetime.now(),
                'current_period_end': datetime.now() + timedelta(days=30),
                'subscribed_at': datetime.now()
            },
            'usage': {
                'monthly_count': 0,
                'monthly_limit': 30 if plan == 'basic' else -1,
                'reset_date': datetime.now() + timedelta(days=30)
            }
        }, merge=True)
```

### 3. 測試

```python
# test_subscription.py
from services.subscription_service import SubscriptionService

# 建立測試訂閱
SubscriptionService.create_subscription(
    user_id='test_user_123',
    plan='basic',
    cycle='monthly'
)

# 檢查訂閱
subscription = SubscriptionService.get_user_subscription('test_user_123')
print(subscription)
# 輸出：{'plan_type': 'basic', 'status': 'active', ...}
```

---

## 📚 完整文件

- **詳細規格**: `payment_subscription_spec.md`
- **實作計畫**: `payment_implementation_plan.md`

---

## ❓ 常見問題

### Q: 為什麼選擇 ECPay？

A: 台灣主流、手續費合理、支援定期定額、文件完整

### Q: 如何測試付款？

A: 使用測試環境 + 測試卡號 4311-9522-2222-2222

### Q: 如何處理付款失敗？

A: Webhook 通知 → 更新狀態 → 發送 Email 通知

### Q: 定期扣款如何實作？

A: ECPay 定期定額 API + Cloud Scheduler 排程檢查

### Q: 如何防止使用量作弊？

A: 所有檢查在後端、使用 Firestore Transaction、記錄日誌

---

**開始時間**: 立即
**預計完成**: 2.5-4 週
**下一步**: 申請 ECPay 測試帳號 + 建立 subscription_service.py
