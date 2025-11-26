# 金流與訂閱制規格書

**版本**: 1.0
**日期**: 2025-11-24
**專案**: OderWhat AI 點餐經紀人

---

## 📋 目錄

1. [需求概述](#需求概述)
2. [會員方案設計](#會員方案設計)
3. [金流串接](#金流串接)
4. [技術架構](#技術架構)
5. [資料結構](#資料結構)
6. [API 設計](#api-設計)
7. [實作計畫](#實作計畫)
8. [安全性考量](#安全性考量)

---

## 需求概述

### 核心目標

將 OderWhat 從免費服務轉為訂閱制服務，實現：

1. **會員分級**: 免費 / 基礎 / 進階方案
2. **使用次數管控**: 根據方案限制每月推薦次數
3. **金流串接**: 信用卡 / 行動支付
4. **自動續約**: 月繳/年繳自動扣款
5. **方案升降級**: 彈性調整訂閱

### 商業模式

```
免費方案：體驗（月 3 次）
  ↓ 升級
基礎方案：輕度使用者（月 30 次 - NT$99/月）
  ↓ 升級
進階方案：重度使用者（無限次 - NT$299/月）
```

---

## 會員方案設計

### 方案對照表

| 項目 | 免費方案 | 基礎方案 | 進階方案 |
|-----|---------|---------|---------|
| **月費** | NT$ 0 | NT$ 99 | NT$ 299 |
| **年費優惠** | - | NT$ 990 (85折) | NT$ 2,990 (83折) |
| **推薦次數/月** | 3 次 | 30 次 | 無限制 |
| **一鍵換菜** | ✅ | ✅ | ✅ |
| **記憶偏好** | ❌ | ✅ | ✅ |
| **優先支援** | ❌ | ❌ | ✅ |
| **進階篩選** | ❌ | ❌ | ✅ |
| **餐廳收藏** | 5 個 | 20 個 | 無限制 |

### 方案代碼

```typescript
enum SubscriptionPlan {
  FREE = 'free',
  BASIC = 'basic',
  PRO = 'pro'
}

enum BillingCycle {
  MONTHLY = 'monthly',
  YEARLY = 'yearly'
}
```

### 定價策略

#### 月繳定價

- **基礎方案**: NT$ 99/月
  - 每次推薦成本約 NT$ 3.3
  - 對標：Netflix 基礎方案 (NT$ 270/月)

- **進階方案**: NT$ 299/月
  - 無限使用，高頻用戶划算
  - 對標：Spotify Premium (NT$ 179/月)

#### 年繳優惠

- **基礎年費**: NT$ 990 (月均 NT$ 82.5，85折)
- **進階年費**: NT$ 2,990 (月均 NT$ 249，83折)

---

## 金流串接

### 推薦金流服務商

#### 選項 1：綠界科技 ECPay（推薦）

**優點**：
- ✅ 台灣主流，支援度高
- ✅ 手續費合理（2.8% + NT$5/筆）
- ✅ 支援定期定額扣款
- ✅ 完整 API 文件（Python SDK）
- ✅ 沙箱環境測試

**支援支付方式**：
- 信用卡（一次付清、分期）
- 網路 ATM
- 超商代碼
- 定期定額（訂閱制必要）

**費用結構**：
```
信用卡：2.8% + NT$5/筆
定期定額：2.8%/月
退款手續費：NT$30/筆
```

#### 選項 2：藍新金流 NewebPay

**優點**：
- ✅ 台灣第二大
- ✅ 支援定期定額
- ✅ 手續費相近（2.75%）

#### 選項 3：Stripe（國際）

**優點**：
- ✅ 開發者友善
- ✅ Webhook 機制完善
- ✅ 訂閱管理強大

**缺點**：
- ❌ 台灣信用卡支援較少
- ❌ 手續費較高（2.9% + NT$9）
- ❌ 需要商業登記

### 推薦方案：綠界科技 ECPay

**理由**：
1. 台灣用戶最熟悉
2. 定期定額功能完整
3. 手續費合理
4. 技術文件完整

---

## 技術架構

### 系統架構圖

```
┌─────────────────────────────────────────────────┐
│                  Frontend (React)                │
│  • 方案選擇頁面                                   │
│  • 付款頁面                                       │
│  • 訂閱管理                                       │
└──────────────────┬──────────────────────────────┘
                   │ HTTPS
┌──────────────────▼──────────────────────────────┐
│              Backend (FastAPI)                   │
│  • /subscriptions (訂閱管理 API)                 │
│  • /payment/create (建立訂單)                    │
│  • /payment/callback (ECPay 回調)               │
│  • /usage/check (檢查使用次數)                   │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌────────▼─────────┐
│   Firestore    │   │   ECPay API      │
│  • users       │   │  • 付款           │
│  • orders      │   │  • 定期扣款       │
│  • usage_logs  │   │  • Webhook       │
└────────────────┘   └──────────────────┘
```

### 核心流程

#### 流程 1：訂閱購買

```
1. 使用者選擇方案 (基礎/進階, 月/年)
2. 前端呼叫 POST /payment/create
3. 後端建立訂單，寫入 Firestore (orders collection)
4. 後端呼叫 ECPay API 建立付款單
5. 返回 ECPay 付款頁面 URL
6. 前端導向 ECPay 付款頁面
7. 使用者完成付款
8. ECPay 發送 Webhook 到 /payment/callback
9. 後端驗證付款，更新使用者訂閱狀態
10. 前端顯示付款成功
```

#### 流程 2：使用次數檢查

```
1. 使用者請求推薦 (POST /recommendations)
2. 中介層 (Middleware) 呼叫 check_usage_limit()
3. 從 Firestore 讀取 users/{user_id}
4. 檢查：
   - plan_type (free/basic/pro)
   - usage_count (本月使用次數)
   - subscription_status (active/expired)
5a. 若未超過限制 → 繼續處理，usage_count++
5b. 若超過限制 → 返回 403 錯誤 + 升級提示
```

#### 流程 3：定期扣款

```
1. ECPay 每月自動扣款
2. 成功 → Webhook 通知後端
3. 後端更新：
   - subscription_renewed_at (續約時間)
   - usage_count = 0 (重置次數)
   - next_billing_date (下次扣款日)
4. 失敗 → Webhook 通知後端
5. 後端標記 subscription_status = 'payment_failed'
6. 發送 Email 通知使用者更新付款方式
```

---

## 資料結構

### Firestore Collections

#### users/{user_id}

```typescript
{
  // === 基本資訊 ===
  user_id: string,           // Google sub
  email: string,
  name: string,
  created_at: timestamp,
  last_login: timestamp,

  // === 訂閱資訊 ===
  subscription: {
    plan_type: 'free' | 'basic' | 'pro',
    billing_cycle: 'monthly' | 'yearly' | null,
    status: 'active' | 'expired' | 'cancelled' | 'payment_failed',

    // 時間相關
    subscribed_at: timestamp | null,     // 首次訂閱時間
    current_period_start: timestamp,     // 本期開始
    current_period_end: timestamp,       // 本期結束
    next_billing_date: timestamp | null, // 下次扣款日
    cancelled_at: timestamp | null,      // 取消時間

    // 金流相關
    ecpay_member_id: string | null,      // ECPay 定期定額會員 ID
    payment_method: string | null,       // 'credit_card' | 'atm'
    last_4_digits: string | null         // 信用卡末四碼
  },

  // === 使用量追蹤 ===
  usage: {
    monthly_count: number,               // 本月使用次數
    monthly_limit: number,               // 本月限制 (3/30/-1)
    reset_date: timestamp,               // 下次重置日期
    total_count: number,                 // 總使用次數
    last_used_at: timestamp | null       // 最後使用時間
  },

  // === 偏好記憶（既有） ===
  feedback_history: array,

  // === 餐廳收藏 ===
  saved_restaurants: array<{
    restaurant_id: string,
    name: string,
    saved_at: timestamp
  }>,
  saved_restaurants_limit: number       // 收藏上限 (5/20/-1)
}
```

#### orders/{order_id}

```typescript
{
  order_id: string,                     // 訂單編號（自動生成）
  user_id: string,

  // === 訂單資訊 ===
  plan_type: 'basic' | 'pro',
  billing_cycle: 'monthly' | 'yearly',
  amount: number,                       // 金額（新台幣）
  currency: 'TWD',

  // === 狀態追蹤 ===
  status: 'pending' | 'completed' | 'failed' | 'refunded',
  created_at: timestamp,
  paid_at: timestamp | null,

  // === ECPay 資訊 ===
  ecpay_merchant_trade_no: string,      // ECPay 訂單編號
  ecpay_trade_no: string | null,        // ECPay 交易編號（付款後）
  ecpay_payment_type: string | null,    // 付款方式
  ecpay_rtn_code: number | null,        // ECPay 回傳碼

  // === 附加資訊 ===
  is_recurring: boolean,                // 是否為定期扣款
  metadata: {
    user_email: string,
    user_name: string,
    ip_address: string | null
  }
}
```

#### usage_logs/{log_id}（可選，用於分析）

```typescript
{
  log_id: string,
  user_id: string,
  action: 'recommendation' | 'swap' | 'save_restaurant',
  timestamp: timestamp,

  // 使用當下的訂閱狀態
  plan_type: string,
  usage_count_before: number,
  usage_count_after: number,

  // 推薦資訊（若 action = 'recommendation'）
  restaurant_name: string | null,
  mode: 'sharing' | 'individual' | null
}
```

---

## API 設計

### 訂閱管理 API

#### 1. 取得方案列表

```http
GET /subscriptions/plans
Authorization: Bearer {google_token}
```

**Response**:
```json
{
  "plans": [
    {
      "plan_id": "free",
      "name": "免費方案",
      "monthly_price": 0,
      "yearly_price": 0,
      "features": {
        "recommendations_per_month": 3,
        "smart_swap": true,
        "taste_memory": false,
        "saved_restaurants": 5
      }
    },
    {
      "plan_id": "basic",
      "name": "基礎方案",
      "monthly_price": 99,
      "yearly_price": 990,
      "features": {
        "recommendations_per_month": 30,
        "smart_swap": true,
        "taste_memory": true,
        "saved_restaurants": 20
      }
    },
    {
      "plan_id": "pro",
      "name": "進階方案",
      "monthly_price": 299,
      "yearly_price": 2990,
      "features": {
        "recommendations_per_month": -1,
        "smart_swap": true,
        "taste_memory": true,
        "saved_restaurants": -1,
        "priority_support": true,
        "advanced_filters": true
      }
    }
  ]
}
```

#### 2. 取得當前訂閱狀態

```http
GET /subscriptions/me
Authorization: Bearer {google_token}
```

**Response**:
```json
{
  "user_id": "google_sub_123",
  "subscription": {
    "plan_type": "basic",
    "billing_cycle": "monthly",
    "status": "active",
    "current_period_end": "2025-12-24T00:00:00Z",
    "next_billing_date": "2025-12-24T00:00:00Z",
    "payment_method": "credit_card",
    "last_4_digits": "1234"
  },
  "usage": {
    "monthly_count": 15,
    "monthly_limit": 30,
    "remaining": 15,
    "reset_date": "2025-12-01T00:00:00Z"
  }
}
```

#### 3. 建立付款訂單

```http
POST /payment/create
Authorization: Bearer {google_token}
Content-Type: application/json
```

**Request Body**:
```json
{
  "plan_type": "basic",
  "billing_cycle": "monthly"
}
```

**Response**:
```json
{
  "order_id": "ORD_20251124_ABCD1234",
  "amount": 99,
  "currency": "TWD",
  "payment_url": "https://payment-stage.ecpay.com.tw/...",
  "expires_at": "2025-11-24T12:30:00Z"
}
```

#### 4. 取消訂閱

```http
POST /subscriptions/cancel
Authorization: Bearer {google_token}
```

**Response**:
```json
{
  "status": "success",
  "message": "訂閱已取消，將於 2025-12-24 到期",
  "access_until": "2025-12-24T23:59:59Z"
}
```

### 使用量檢查 API（內部）

#### 檢查使用限制（Middleware）

```python
async def check_usage_limit(user_id: str) -> dict:
    """
    檢查使用者是否可以使用推薦功能

    Returns:
        {
            "allowed": bool,
            "plan_type": str,
            "usage_count": int,
            "limit": int,
            "message": str | None
        }
    """
    user = get_user_from_firestore(user_id)

    plan_type = user['subscription']['plan_type']
    usage = user['usage']

    # 進階方案：無限制
    if plan_type == 'pro':
        return {"allowed": True, "plan_type": "pro", "limit": -1}

    # 免費/基礎方案：檢查次數
    if usage['monthly_count'] >= usage['monthly_limit']:
        return {
            "allowed": False,
            "plan_type": plan_type,
            "usage_count": usage['monthly_count'],
            "limit": usage['monthly_limit'],
            "message": "本月使用次數已達上限，請升級方案"
        }

    return {
        "allowed": True,
        "plan_type": plan_type,
        "usage_count": usage['monthly_count'],
        "limit": usage['monthly_limit']
    }
```

### ECPay Webhook API

#### 付款回調（定期定額）

```http
POST /payment/callback/ecpay
Content-Type: application/x-www-form-urlencoded
```

**Request Body** (ECPay 回傳):
```
MerchantID=MS123456&
MerchantTradeNo=ORD_20251124_ABCD1234&
RtnCode=1&
RtnMsg=付款成功&
TradeNo=2025112412345678&
TradeAmt=99&
PaymentDate=2025-11-24+12:00:00&
PaymentType=Credit_CreditCard&
SimulatePaid=0&
CheckMacValue=ABCD1234...
```

**處理邏輯**:
```python
async def handle_ecpay_callback(request: Request):
    # 1. 驗證 CheckMacValue
    if not verify_ecpay_mac(request.form):
        return {"status": "error"}

    # 2. 更新訂單狀態
    order = get_order(request.form['MerchantTradeNo'])
    order.status = 'completed'
    order.ecpay_trade_no = request.form['TradeNo']
    order.paid_at = datetime.now()

    # 3. 更新使用者訂閱
    user = get_user(order.user_id)
    user.subscription.status = 'active'
    user.subscription.current_period_start = datetime.now()
    user.subscription.current_period_end = datetime.now() + timedelta(days=30)
    user.usage.monthly_count = 0  # 重置使用次數

    # 4. 返回成功
    return {"status": "1|OK"}
```

---

## 實作計畫

### 階段 1：資料庫設計（1-2 天）

**任務**：
- [x] 設計 Firestore schema
- [ ] 建立 users collection 新欄位
- [ ] 建立 orders collection
- [ ] 建立 usage_logs collection（可選）
- [ ] 撰寫資料庫遷移腳本

**產出**：
- `services/subscription_service.py`
- `services/payment_service.py`
- `migration_add_subscription_fields.py`

### 階段 2：後端 API 實作（3-5 天）

**任務**：
- [ ] 建立訂閱管理 API
  - [ ] GET /subscriptions/plans
  - [ ] GET /subscriptions/me
  - [ ] POST /subscriptions/cancel
- [ ] 建立付款 API
  - [ ] POST /payment/create
  - [ ] POST /payment/callback/ecpay
- [ ] 實作使用量檢查 Middleware
- [ ] 整合 ECPay SDK

**產出**：
- `routers/subscription.py`
- `routers/payment.py`
- `middleware/usage_limit.py`
- `integrations/ecpay.py`

### 階段 3：金流串接測試（2-3 天）

**任務**：
- [ ] 申請 ECPay 測試帳號
- [ ] 設定沙箱環境
- [ ] 測試付款流程
  - [ ] 信用卡付款
  - [ ] 定期定額扣款
  - [ ] Webhook 接收
- [ ] 測試失敗情境
  - [ ] 付款失敗
  - [ ] 扣款失敗
  - [ ] Webhook 重送

**產出**：
- 測試報告
- 環境配置文件

### 階段 4：前端整合（3-5 天）

**任務**：
- [ ] 方案選擇頁面
- [ ] 付款頁面（導向 ECPay）
- [ ] 訂閱管理頁面
  - [ ] 檢視當前方案
  - [ ] 使用量顯示
  - [ ] 升級/取消按鈕
- [ ] 使用限制提示
  - [ ] 推薦次數剩餘提示
  - [ ] 超過限制時顯示升級選項

**產出**：
- `pages/Subscription.tsx`
- `pages/Payment.tsx`
- `components/UsageBadge.tsx`
- `components/UpgradePrompt.tsx`

### 階段 5：測試與上線（2-3 天）

**任務**：
- [ ] 完整流程測試
  - [ ] 免費用戶註冊
  - [ ] 購買基礎方案
  - [ ] 使用次數扣減
  - [ ] 升級進階方案
  - [ ] 取消訂閱
- [ ] 壓力測試
- [ ] 安全性檢查
- [ ] 正式環境部署

**總計時間**: 11-18 天（約 2.5-4 週）

---

## 安全性考量

### 1. 付款安全

- ✅ **不儲存信用卡資訊**: 由 ECPay 託管
- ✅ **HTTPS 加密**: 所有通訊使用 SSL
- ✅ **CheckMacValue 驗證**: 防止 Webhook 偽造
- ✅ **IP 白名單**: 僅接受 ECPay IP 的 Webhook

### 2. 使用量防作弊

- ✅ **後端驗證**: 所有檢查在後端進行
- ✅ **Transaction**: 使用 Firestore Transaction 避免競態條件
- ✅ **日誌記錄**: 記錄所有使用行為
- ✅ **異常偵測**: 監控短時間內大量請求

### 3. 訂閱狀態

- ✅ **自動過期**: 定期檢查訂閱是否過期
- ✅ **寬限期**: 付款失敗後提供 3 天寬限期
- ✅ **Email 通知**: 付款失敗、即將到期時通知

### 4. 資料隱私

- ✅ **GDPR 合規**: 提供資料匯出/刪除功能
- ✅ **最小權限**: 僅儲存必要資訊
- ✅ **加密傳輸**: 敏感資料加密

---

## 附錄

### A. ECPay 定期定額文件

**官方文件**: https://developers.ecpay.com.tw/?p=2856

**關鍵 API**:
- 建立定期定額訂單: `/Cashier/QueryPeriodCreditCardTradeInfo`
- 查詢訂單: `/Cashier/QueryTradeInfo/V5`
- 取消定期扣款: `/CreditDetail/DoAction`

### B. 測試帳號資訊

**ECPay 測試環境**:
- URL: https://payment-stage.ecpay.com.tw
- 測試信用卡號: 4311-9522-2222-2222
- 有效期限: 任意未來日期
- CVV: 任意 3 碼

### C. 費用試算

**基礎方案（月繳）**:
```
售價: NT$ 99
手續費: 99 × 2.8% + 5 = NT$ 7.77
淨收入: 99 - 7.77 = NT$ 91.23
```

**進階方案（年繳）**:
```
售價: NT$ 2,990
手續費: 2,990 × 2.8% + 5 = NT$ 88.72
淨收入: 2,990 - 88.72 = NT$ 2,901.28
月均淨收入: 2,901.28 / 12 = NT$ 241.77
```

---

## 下一步

1. **確認方案定價與功能** - 與團隊討論最終方案
2. **申請 ECPay 商店** - 準備營業登記文件
3. **開始階段 1 實作** - 資料庫設計與遷移
4. **前後端協調** - 確認 API 規格
5. **準備行銷素材** - 方案比較圖、FAQ

---

**文件版本**: 1.0
**最後更新**: 2025-11-24
**負責人**: Stephen
**狀態**: ✅ 規格完成，待實作
