# TapPay 訂閱制實作規格

**版本**: 1.0
**日期**: 2025-11-24
**金流服務商**: TapPay
**優勢**: 無跳轉頁面、現代化 API、使用者體驗佳

---

## 📋 目錄

1. [為什麼選擇 TapPay](#為什麼選擇-tappay)
2. [TapPay vs ECPay 比較](#tappay-vs-ecpay-比較)
3. [定期定額實作原理](#定期定額實作原理)
4. [技術架構](#技術架構)
5. [API 整合](#api-整合)
6. [資料結構](#資料結構)
7. [實作流程](#實作流程)
8. [安全性考量](#安全性考量)

---

## 為什麼選擇 TapPay

### 核心優勢

1. **✅ 無跳轉付款頁面**
   - 使用者全程留在你的網站
   - 不會被導向第三方頁面
   - 品牌體驗一致

2. **✅ 支援定期定額扣款**
   - 透過 `card_key` + `card_token` 機制
   - 自行控制扣款週期和金額
   - 靈活度高

3. **✅ 現代化 API 設計**
   - RESTful API
   - 完整的 SDK（Python, Node.js, PHP）
   - 文件清晰易懂

4. **✅ 開發者友善**
   - 沙箱環境完整
   - Webhook 機制完善
   - 錯誤訊息明確

5. **✅ 手續費合理**
   - 2.8%（與 ECPay 相同）
   - 無額外設定費
   - 無月費

### 適合場景

- ✅ SaaS 訂閱服務
- ✅ 會員制網站
- ✅ 線上課程平台
- ✅ 內容訂閱平台

---

## TapPay vs ECPay 比較

| 項目 | TapPay | ECPay |
|-----|--------|-------|
| **付款體驗** | 留在網站內 ✅ | 跳轉到 ECPay ❌ |
| **定期定額** | card_token 機制 ✅ | 定期定額 API ✅ |
| **API 設計** | 現代化 RESTful ✅ | 較傳統 ⚠️ |
| **手續費** | 2.8% | 2.8% + NT$5 |
| **開發難度** | 中等 | 較高 |
| **文件品質** | 優秀 ✅ | 完整但複雜 ⚠️ |
| **沙箱環境** | 完整 ✅ | 完整 ✅ |
| **支援付款方式** | 信用卡、Apple Pay、Google Pay | 信用卡、超商、ATM、虛擬帳號 |
| **市佔率** | 中等（新創常用）| 最高（傳統電商）|

### 決策建議

**選擇 TapPay 如果**：
- 希望提供流暢的付款體驗
- 主要客群使用信用卡
- 重視品牌一致性
- 開發團隊熟悉現代 API

**選擇 ECPay 如果**：
- 需要支援超商/ATM 付款
- 客群較習慣傳統金流
- 需要最高市佔率保證

**OderWhat 建議**: 選擇 **TapPay**
- 目標客群：年輕上班族（習慣信用卡）
- 重視 UX：不想跳轉離開網站
- SaaS 訂閱模式：適合 TapPay

---

## 定期定額實作原理

### 核心機制：Card Tokenization

```
第一次付款：
  使用者輸入卡號 → TapPay JS SDK 產生 prime
  → 後端呼叫 Pay by Prime API (remember=true)
  → TapPay 返回 card_key + card_token
  → 後端儲存 token

後續扣款：
  排程觸發 → 後端呼叫 Pay by Card Token API
  → 使用儲存的 card_key + card_token
  → 自動扣款成功/失敗
```

### 關鍵參數

#### 1. Prime（首次付款）

```javascript
// 前端：使用者輸入卡號後取得 prime
TPDirect.card.getPrime((result) => {
  if (result.status !== 0) {
    alert('取得 prime 失敗：' + result.msg);
    return;
  }

  const prime = result.card.prime;
  // 將 prime 傳給後端
});
```

#### 2. Card Key + Card Token（定期扣款用）

```python
# 後端：首次付款時取得
response = tappay.pay_by_prime({
    'prime': prime,
    'partner_key': PARTNER_KEY,
    'merchant_id': MERCHANT_ID,
    'amount': 99,
    'currency': 'TWD',
    'remember': True,  # 🔑 關鍵：開啟記憶功能
    'cardholder': {
        'phone_number': user.phone,
        'name': user.name,
        'email': user.email
    }
})

if response['status'] == 0:
    # 儲存這兩個參數
    card_key = response['card_secret']['card_key']
    card_token = response['card_secret']['card_token']
```

#### 3. Pay by Card Token（定期扣款）

```python
# 後端：定期扣款時使用
response = tappay.pay_by_card_token({
    'partner_key': PARTNER_KEY,
    'merchant_id': MERCHANT_ID,
    'card_key': user.subscription.tappay_card_key,
    'card_token': user.subscription.tappay_card_token,
    'amount': 99,
    'currency': 'TWD',
    'details': 'OderWhat 基礎方案 - 2025/12',
    'cardholder': {
        'phone_number': user.phone,
        'name': user.name,
        'email': user.email
    }
})

if response['status'] == 0:
    # 扣款成功
    return True
else:
    # 扣款失敗
    error_msg = response['msg']
    return False
```

### 重要限制

⚠️ **不支援 remember 功能的支付方式**：
- Apple Pay
- Google Pay
- Samsung Pay
- LINE Pay
- 悠遊付
- 全盈支付

**只有信用卡支援定期定額扣款**

---

## 技術架構

### 系統架構圖

```
┌─────────────────────────────────────────────────┐
│            Frontend (React)                      │
│  • TapPay JS SDK                                 │
│  • 付款表單（信用卡欄位）                         │
│  • 訂閱管理頁面                                   │
└──────────────────┬──────────────────────────────┘
                   │ HTTPS
┌──────────────────▼──────────────────────────────┐
│            Backend (FastAPI)                     │
│  • /payment/tappay/create (首次付款)             │
│  • /payment/tappay/recurring (定期扣款)          │
│  • /payment/tappay/webhook (狀態通知)            │
│  • /subscriptions/* (訂閱管理)                   │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌────────▼─────────┐
│   Firestore    │   │   TapPay API     │
│  • users       │   │  • Pay by Prime  │
│  • orders      │   │  • Pay by Token  │
│  • usage_logs  │   │  • Webhook       │
└────────────────┘   └──────────────────┘
```

### 核心流程

#### 流程 1：首次訂閱付款

```
1. 前端：使用者填寫信用卡資料
2. 前端：TapPay JS SDK 產生 prime（不經過你的伺服器）
3. 前端：將 prime 傳給後端 POST /payment/tappay/create
4. 後端：呼叫 TapPay Pay by Prime API (remember=true)
5. 後端：收到 card_key + card_token
6. 後端：儲存到 Firestore users/{user_id}.subscription
7. 後端：建立訂單記錄 orders/{order_id}
8. 後端：更新使用者訂閱狀態
9. 前端：顯示付款成功
```

#### 流程 2：定期扣款（每月自動）

```
1. Cloud Scheduler 觸發 /scheduled/subscription-renewal
2. 後端：查詢明天要續約的使用者
3. 後端：呼叫 TapPay Pay by Card Token API
   - 使用儲存的 card_key + card_token
   - 金額：99 或 299（依方案）
4a. 扣款成功：
    - 更新 subscription.current_period_end (+30天)
    - 重置 usage.monthly_count = 0
    - 發送成功 Email
4b. 扣款失敗：
    - 標記 subscription.status = 'payment_failed'
    - 發送失敗 Email（請更新付款方式）
    - 提供 3 天寬限期
```

#### 流程 3：更換信用卡

```
1. 使用者在訂閱管理頁面點擊「更換信用卡」
2. 前端：顯示 TapPay 卡號輸入欄位
3. 前端：取得新的 prime
4. 前端：呼叫 POST /payment/tappay/update-card
5. 後端：呼叫 Pay by Prime (remember=true)
6. 後端：更新 card_key + card_token
7. 後端：（可選）呼叫 Pay by Card Token 扣款 NT$1 驗證
8. 後端：驗證成功後更新資料
9. 前端：顯示更新成功
```

---

## API 整合

### 1. TapPay SDK 安裝

```bash
pip install tappay-python
```

或使用 HTTP Client：

```python
# integrations/tappay.py
import requests
import hashlib
import os

class TapPayService:
    def __init__(self):
        self.partner_key = os.getenv('TAPPAY_PARTNER_KEY')
        self.merchant_id = os.getenv('TAPPAY_MERCHANT_ID')
        self.base_url = os.getenv('TAPPAY_API_URL',
            'https://sandbox.tappaysdk.com/tpc')  # 測試環境

    def pay_by_prime(self, prime: str, amount: int,
                     user_info: dict, remember: bool = True) -> dict:
        """
        首次付款 API

        Args:
            prime: 前端傳來的 prime token
            amount: 金額（新台幣）
            user_info: 使用者資訊
            remember: 是否儲存卡片資訊（定期扣款必須 True）

        Returns:
            {
                'status': 0,  # 0=成功
                'msg': '成功',
                'rec_trade_id': '...',
                'card_secret': {
                    'card_key': '...',
                    'card_token': '...'
                }
            }
        """
        url = f'{self.base_url}/payment/pay-by-prime'

        payload = {
            'partner_key': self.partner_key,
            'prime': prime,
            'amount': amount,
            'merchant_id': self.merchant_id,
            'currency': 'TWD',
            'details': f"OderWhat 訂閱 - {user_info['email']}",
            'cardholder': {
                'phone_number': user_info.get('phone', '+886900000000'),
                'name': user_info['name'],
                'email': user_info['email']
            },
            'remember': remember
        }

        response = requests.post(url, json=payload)
        return response.json()

    def pay_by_card_token(self, card_key: str, card_token: str,
                         amount: int, user_info: dict) -> dict:
        """
        定期扣款 API

        Args:
            card_key: 儲存的卡片金鑰
            card_token: 儲存的卡片 token
            amount: 金額
            user_info: 使用者資訊

        Returns:
            {
                'status': 0,  # 0=成功
                'msg': '成功',
                'rec_trade_id': '...'
            }
        """
        url = f'{self.base_url}/payment/pay-by-card-token'

        payload = {
            'partner_key': self.partner_key,
            'merchant_id': self.merchant_id,
            'card_key': card_key,
            'card_token': card_token,
            'amount': amount,
            'currency': 'TWD',
            'details': f"OderWhat 月費 - {user_info['email']}",
            'cardholder': {
                'phone_number': user_info.get('phone', '+886900000000'),
                'name': user_info['name'],
                'email': user_info['email']
            }
        }

        response = requests.post(url, json=payload)
        return response.json()

    def verify_payment(self, rec_trade_id: str) -> dict:
        """
        查詢交易狀態

        Args:
            rec_trade_id: TapPay 交易編號

        Returns:
            交易詳情
        """
        url = f'{self.base_url}/payment/record'

        payload = {
            'partner_key': self.partner_key,
            'rec_trade_id': rec_trade_id
        }

        response = requests.post(url, json=payload)
        return response.json()
```

### 2. 前端整合（React）

```tsx
// components/TapPayCardForm.tsx
import { useEffect, useState } from 'react';

export function TapPayCardForm({ onSuccess, amount }) {
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    // 載入 TapPay JS SDK
    const script = document.createElement('script');
    script.src = 'https://js.tappaysdk.com/sdk/tpdirect/v5.18.0';
    script.async = true;
    script.onload = initTapPay;
    document.body.appendChild(script);
  }, []);

  const initTapPay = () => {
    TPDirect.setupSDK(
      APP_ID,      // TapPay APP ID
      APP_KEY,     // TapPay APP KEY
      'sandbox'    // 'sandbox' or 'production'
    );

    // 設定信用卡欄位
    TPDirect.card.setup({
      fields: {
        number: { element: '#card-number' },
        expirationDate: { element: '#card-expiry' },
        ccv: { element: '#card-ccv' }
      },
      styles: {
        'input': { 'font-size': '16px' },
        ':focus': { 'color': '#3b82f6' }
      }
    });

    setIsReady(true);
  };

  const handleSubmit = async () => {
    // 取得 prime
    TPDirect.card.getPrime((result) => {
      if (result.status !== 0) {
        alert('取得 prime 失敗：' + result.msg);
        return;
      }

      const prime = result.card.prime;

      // 傳給後端
      fetch('/payment/tappay/create', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          prime: prime,
          amount: amount,
          plan_type: 'basic',
          billing_cycle: 'monthly'
        })
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          onSuccess(data);
        } else {
          alert('付款失敗：' + data.message);
        }
      });
    });
  };

  return (
    <div className="tappay-card-form">
      <h3>信用卡資訊</h3>

      <div className="form-group">
        <label>卡號</label>
        <div id="card-number"></div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>有效期限</label>
          <div id="card-expiry"></div>
        </div>
        <div className="form-group">
          <label>安全碼</label>
          <div id="card-ccv"></div>
        </div>
      </div>

      <button
        onClick={handleSubmit}
        disabled={!isReady}
        className="pay-button"
      >
        付款 NT$ {amount}
      </button>
    </div>
  );
}
```

### 3. 後端 API 實作

```python
# routers/payment_tappay.py
from fastapi import APIRouter, Depends, HTTPException
from integrations.tappay import TapPayService
from services.subscription_service import SubscriptionService
from services.payment_service import PaymentService

router = APIRouter(prefix='/payment/tappay', tags=['payment'])
tappay = TapPayService()

@router.post("/create")
async def create_payment(
    request: PaymentRequest,
    user_info: dict = Depends(get_current_user)
):
    """
    首次訂閱付款

    Request Body:
        {
            "prime": "...",
            "plan_type": "basic",
            "billing_cycle": "monthly"
        }
    """
    user_id = user_info['sub']

    # 1. 計算金額
    amount = calculate_amount(request.plan_type, request.billing_cycle)

    # 2. 呼叫 TapPay API
    result = tappay.pay_by_prime(
        prime=request.prime,
        amount=amount,
        user_info={
            'email': user_info['email'],
            'name': user_info['name'],
            'phone': user_info.get('phone')
        },
        remember=True  # 開啟定期扣款
    )

    if result['status'] != 0:
        raise HTTPException(400, f"付款失敗：{result['msg']}")

    # 3. 儲存 card_key + card_token
    card_key = result['card_secret']['card_key']
    card_token = result['card_secret']['card_token']

    # 4. 建立訂單
    order = PaymentService.create_order(
        user_id=user_id,
        plan_type=request.plan_type,
        billing_cycle=request.billing_cycle,
        amount=amount,
        payment_provider='tappay',
        rec_trade_id=result['rec_trade_id']
    )

    # 5. 更新訂閱
    SubscriptionService.create_subscription(
        user_id=user_id,
        plan=request.plan_type,
        cycle=request.billing_cycle,
        tappay_card_key=card_key,
        tappay_card_token=card_token
    )

    return {
        'status': 'success',
        'order_id': order['order_id'],
        'rec_trade_id': result['rec_trade_id']
    }


@router.post("/recurring")
async def charge_recurring():
    """
    定期扣款（由 Cloud Scheduler 觸發）

    檢查明天要續約的使用者並扣款
    """
    from datetime import datetime, timedelta

    tomorrow = datetime.now() + timedelta(days=1)

    # 查詢明天要續約的使用者
    users = db.collection('users')\
              .where('subscription.next_billing_date', '>=', tomorrow)\
              .where('subscription.next_billing_date', '<', tomorrow + timedelta(days=1))\
              .where('subscription.status', '==', 'active')\
              .stream()

    results = {
        'success': [],
        'failed': []
    }

    for user_doc in users:
        user_id = user_doc.id
        user_data = user_doc.to_dict()
        subscription = user_data['subscription']

        # 計算金額
        amount = calculate_amount(
            subscription['plan_type'],
            subscription['billing_cycle']
        )

        # 呼叫 TapPay 扣款
        result = tappay.pay_by_card_token(
            card_key=subscription['tappay_card_key'],
            card_token=subscription['tappay_card_token'],
            amount=amount,
            user_info={
                'email': user_data['email'],
                'name': user_data['name'],
                'phone': user_data.get('phone')
            }
        )

        if result['status'] == 0:
            # 扣款成功
            SubscriptionService.renew_subscription(user_id)
            results['success'].append(user_id)
        else:
            # 扣款失敗
            SubscriptionService.mark_payment_failed(user_id)
            send_payment_failed_email(user_id, result['msg'])
            results['failed'].append({
                'user_id': user_id,
                'reason': result['msg']
            })

    return results
```

---

## 資料結構

### Firestore Schema

#### users/{user_id}

```typescript
{
  // 基本資訊
  user_id: string,
  email: string,
  name: string,

  // 訂閱資訊
  subscription: {
    plan_type: 'free' | 'basic' | 'pro',
    billing_cycle: 'monthly' | 'yearly' | null,
    status: 'active' | 'expired' | 'cancelled' | 'payment_failed',

    // TapPay 專用欄位
    tappay_card_key: string | null,       // 🔑 定期扣款用
    tappay_card_token: string | null,     // 🔑 定期扣款用
    card_last_4: string | null,           // 卡號末四碼（顯示用）
    card_type: string | null,             // 卡別（Visa, Master）

    // 時間相關
    subscribed_at: timestamp | null,
    current_period_start: timestamp,
    current_period_end: timestamp,
    next_billing_date: timestamp | null,
    cancelled_at: timestamp | null
  },

  // 使用量
  usage: {
    monthly_count: number,
    monthly_limit: number,
    reset_date: timestamp
  }
}
```

#### orders/{order_id}

```typescript
{
  order_id: string,
  user_id: string,

  plan_type: 'basic' | 'pro',
  billing_cycle: 'monthly' | 'yearly',
  amount: number,
  currency: 'TWD',

  status: 'pending' | 'completed' | 'failed' | 'refunded',

  // TapPay 專用欄位
  payment_provider: 'tappay',
  tappay_rec_trade_id: string | null,   // TapPay 交易編號
  tappay_bank_transaction_id: string | null,

  created_at: timestamp,
  paid_at: timestamp | null,

  metadata: {
    user_email: string,
    ip_address: string | null
  }
}
```

---

## 實作流程

### Phase 1: TapPay 帳號申請（1 天）

1. **申請測試帳號**
   - 前往：https://portal.tappaysdk.com/register
   - 填寫公司/個人資訊
   - 取得 APP_ID 和 APP_KEY

2. **設定測試環境**
   ```bash
   # .env.development
   TAPPAY_PARTNER_KEY=partner_xxxxx
   TAPPAY_MERCHANT_ID=your_merchant_id
   TAPPAY_APP_ID=xxxxx
   TAPPAY_APP_KEY=app_xxxxx
   TAPPAY_API_URL=https://sandbox.tappaysdk.com/tpc
   ```

3. **測試信用卡**
   - 卡號：`4242 4242 4242 4242`
   - 有效期限：任意未來日期
   - CVV：任意 3 碼

### Phase 2: 後端實作（3-5 天）

- [ ] Day 1: 建立 `integrations/tappay.py`
- [ ] Day 2: 實作 `routers/payment_tappay.py`
- [ ] Day 3: 整合訂閱服務
- [ ] Day 4: 實作定期扣款排程
- [ ] Day 5: 測試與除錯

### Phase 3: 前端整合（2-3 天）

- [ ] Day 6: 載入 TapPay JS SDK
- [ ] Day 7: 建立信用卡輸入表單
- [ ] Day 8: 整合付款流程

### Phase 4: 測試與上線（2 天）

- [ ] Day 9: 完整測試
- [ ] Day 10: 正式環境部署

**總計**: 8-11 天（約 2 週）

---

## 安全性考量

### 1. PCI DSS 合規

✅ **TapPay 已處理**
- 卡號不經過你的伺服器
- 前端直接與 TapPay 溝通產生 prime
- 你只需處理 prime token

### 2. Card Token 儲存

✅ **安全建議**
```python
# 加密儲存（可選）
from cryptography.fernet import Fernet

def encrypt_token(token: str) -> str:
    f = Fernet(ENCRYPTION_KEY)
    return f.encrypt(token.encode()).decode()

def decrypt_token(encrypted: str) -> str:
    f = Fernet(ENCRYPTION_KEY)
    return f.decrypt(encrypted.encode()).decode()

# 儲存時加密
user.subscription.tappay_card_token = encrypt_token(card_token)

# 使用時解密
card_token = decrypt_token(user.subscription.tappay_card_token)
```

### 3. API 金鑰保護

✅ **環境變數**
```bash
# 絕對不要 commit 到 git
TAPPAY_PARTNER_KEY=partner_xxxxx
TAPPAY_APP_KEY=app_xxxxx
```

✅ **GCP Secret Manager**
```bash
gcloud secrets create tappay-partner-key \
  --data-file=tappay_key.txt
```

### 4. 防止重複扣款

✅ **冪等性設計**
```python
def charge_subscription(user_id: str, billing_date: date) -> dict:
    # 檢查是否已扣款
    existing_order = db.collection('orders')\
        .where('user_id', '==', user_id)\
        .where('billing_date', '==', billing_date)\
        .where('status', '==', 'completed')\
        .limit(1)\
        .get()

    if existing_order:
        return {'status': 'already_charged'}

    # 執行扣款...
```

---

## 測試案例

### 測試 1：首次訂閱付款

```python
def test_first_subscription():
    # 1. 使用者選擇基礎方案
    response = client.post('/payment/tappay/create', json={
        'prime': get_test_prime(),
        'plan_type': 'basic',
        'billing_cycle': 'monthly'
    }, headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert response.json()['status'] == 'success'

    # 2. 檢查訂閱狀態
    user = get_user('test_user')
    assert user['subscription']['plan_type'] == 'basic'
    assert user['subscription']['status'] == 'active'
    assert user['subscription']['tappay_card_key'] is not None
```

### 測試 2：定期扣款成功

```python
def test_recurring_charge_success():
    # 設定明天要續約
    set_next_billing_date('test_user', tomorrow())

    # 觸發定期扣款
    response = client.post('/payment/tappay/recurring')

    assert 'test_user' in response.json()['success']

    # 檢查訂閱已續約
    user = get_user('test_user')
    assert user['subscription']['current_period_end'] > datetime.now()
    assert user['usage']['monthly_count'] == 0  # 已重置
```

### 測試 3：扣款失敗處理

```python
def test_recurring_charge_failed():
    # 使用無效的 card_token
    user = get_user('test_user')
    user['subscription']['tappay_card_token'] = 'invalid_token'
    update_user('test_user', user)

    # 觸發扣款
    response = client.post('/payment/tappay/recurring')

    assert 'test_user' in [f['user_id'] for f in response.json()['failed']]

    # 檢查狀態已標記為失敗
    user = get_user('test_user')
    assert user['subscription']['status'] == 'payment_failed'
```

---

## 常見問題

### Q1: TapPay 手續費如何計算？

**A**: 2.8%，無額外費用
- 基礎方案 NT$99：手續費約 NT$2.77
- 進階方案 NT$299：手續費約 NT$8.37

### Q2: 定期扣款會自動進行嗎？

**A**: 不會。需要你自己實作排程（Cloud Scheduler）定期呼叫 Pay by Card Token API

### Q3: 使用者可以更換信用卡嗎？

**A**: 可以。重新呼叫 Pay by Prime (remember=true) 取得新的 card_key + card_token

### Q4: 如何處理扣款失敗？

**A**:
1. 標記 subscription.status = 'payment_failed'
2. 發送 Email 通知
3. 提供 3 天寬限期
4. 寬限期後降級為免費方案

### Q5: Apple Pay 可以用於訂閱嗎？

**A**: 不行。Apple Pay 不支援 remember 功能，無法取得 card_token

### Q6: 如何退款？

**A**: 使用 TapPay Refund API
```python
tappay.refund(rec_trade_id=order.tappay_rec_trade_id, amount=99)
```

---

## 參考資源

### 官方文件

- **TapPay 後端文件**: https://docs.tappaysdk.com/tutorial/zh/back.html
- **Pay by Prime API**: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api
- **Pay by Card Token API**: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-card-token-api
- **TapPay Portal**: https://portal.tappaysdk.com/

### SDK 與工具

- **Python SDK**: `pip install tappay-python`
- **JS SDK**: https://js.tappaysdk.com/sdk/tpdirect/v5.18.0
- **Postman Collection**: https://www.postman.com/tappay

### 測試資源

- **測試卡號**: 4242 4242 4242 4242
- **沙箱環境**: https://sandbox.tappaysdk.com
- **測試指南**: https://docs.tappaysdk.com/tutorial/zh/test.html

---

## 下一步

1. ✅ **規格確認完成**
2. [ ] 申請 TapPay 測試帳號
3. [ ] 開始後端整合
4. [ ] 前端表單開發
5. [ ] 完整測試
6. [ ] 正式上線

---

**文件版本**: 1.0
**最後更新**: 2025-11-24
**金流服務商**: TapPay
**狀態**: ✅ 規格完成，建議採用
