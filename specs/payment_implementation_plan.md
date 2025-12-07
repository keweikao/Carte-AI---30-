# 金流與訂閱制實作計畫

**專案**: OderWhat 訂閱制實作
**預計時間**: 2.5-4 週
**開始日期**: 2025-11-25
**目標**: 完整的訂閱制金流系統上線

---

## 📅 時程規劃

```
Week 1: 資料庫 + 後端 API 基礎
Week 2: 金流串接 + 測試
Week 3: 前端整合
Week 4: 測試 + 上線
```

---

## 階段 1：資料庫設計與遷移（2 天）

### Day 1：Schema 設計與實作

#### 任務清單

- [ ] **建立 services/subscription_service.py**
  ```python
  class SubscriptionService:
      def get_user_subscription(user_id: str) -> dict
      def create_subscription(user_id: str, plan: str, cycle: str)
      def cancel_subscription(user_id: str)
      def renew_subscription(user_id: str)
      def check_subscription_active(user_id: str) -> bool
  ```

- [ ] **建立 services/payment_service.py**
  ```python
  class PaymentService:
      def create_order(user_id: str, plan: str, amount: int) -> dict
      def get_order(order_id: str) -> dict
      def update_order_status(order_id: str, status: str)
      def record_payment(order_id: str, ecpay_data: dict)
  ```

- [ ] **建立 services/usage_service.py**
  ```python
  class UsageService:
      def check_usage_limit(user_id: str) -> dict
      def increment_usage(user_id: str)
      def reset_monthly_usage(user_id: str)
      def get_usage_stats(user_id: str) -> dict
      def log_usage(user_id: str, action: str, metadata: dict)
  ```

### Day 2：資料遷移與測試

#### 任務清單

- [ ] **建立遷移腳本 migration_add_subscription.py**
  - 為現有 users 新增 subscription 欄位
  - 為現有 users 新增 usage 欄位
  - 設定預設值（免費方案）

- [ ] **測試資料遷移**
  ```bash
  python migration_add_subscription.py --dry-run
  python migration_add_subscription.py --execute
  ```

- [ ] **建立測試資料**
  - 3 個測試用戶（免費/基礎/進階）
  - 5 個測試訂單（pending/completed/failed）

#### 驗收標準

```python
# 測試腳本：test_subscription_db.py
def test_user_has_subscription_field():
    user = db.collection('users').document('test_user').get()
    assert 'subscription' in user.to_dict()
    assert 'usage' in user.to_dict()

def test_default_subscription():
    user = db.collection('users').document('new_user').get()
    assert user.to_dict()['subscription']['plan_type'] == 'free'
    assert user.to_dict()['usage']['monthly_limit'] == 3
```

---

## 階段 2：後端 API 實作（5 天）

### Day 3：訂閱管理 API

#### 任務清單

- [ ] **建立 routers/subscription.py**
  ```python
  @router.get("/subscriptions/plans")
  async def get_plans()

  @router.get("/subscriptions/me")
  async def get_my_subscription(user_info: dict = Depends(get_current_user))

  @router.post("/subscriptions/cancel")
  async def cancel_subscription(user_info: dict = Depends(get_current_user))
  ```

- [ ] **建立 schemas/subscription.py**
  ```python
  class SubscriptionPlan(BaseModel):
      plan_id: str
      name: str
      monthly_price: int
      yearly_price: int
      features: dict

  class UserSubscription(BaseModel):
      plan_type: str
      billing_cycle: str
      status: str
      current_period_end: datetime
  ```

- [ ] **註冊路由到 main.py**
  ```python
  from routers import subscription
  app.include_router(subscription.router, tags=["subscription"])
  ```

#### 測試

```bash
# 測試取得方案列表
curl http://localhost:8000/subscriptions/plans

# 測試取得當前訂閱（需 token）
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/subscriptions/me
```

### Day 4：使用量限制 Middleware

#### 任務清單

- [ ] **建立 middleware/usage_limit.py**
  ```python
  async def check_usage_limit(user_id: str, request: Request):
      """
      檢查使用量並決定是否允許請求

      Returns:
          tuple: (allowed: bool, message: str | None)
      """
      # 1. 取得使用者訂閱資訊
      subscription = get_user_subscription(user_id)

      # 2. 檢查訂閱狀態
      if subscription['status'] != 'active':
          return False, "訂閱已過期"

      # 3. 檢查使用次數
      usage = get_user_usage(user_id)
      if usage['monthly_count'] >= usage['monthly_limit'] and \
         subscription['plan_type'] != 'pro':
          return False, "本月使用次數已達上限"

      return True, None
  ```

- [ ] **整合到 /recommendations 端點**
  ```python
  @app.post("/recommendations")
  async def get_recommendations(
      request: RecommendationRequest,
      user_info: dict = Depends(get_current_user)
  ):
      user_id = user_info['sub']

      # 檢查使用量
      allowed, message = await check_usage_limit(user_id, request)
      if not allowed:
          raise HTTPException(
              status_code=403,
              detail={
                  "error": "usage_limit_exceeded",
                  "message": message,
                  "current_plan": get_plan_type(user_id),
                  "upgrade_url": "/subscriptions/plans"
              }
          )

      # 遞增使用次數
      increment_usage(user_id)

      # 原本的推薦邏輯...
      response = await agent.get_recommendations(request)
      return response
  ```

#### 測試

```python
# test_usage_limit.py
def test_free_user_exceeds_limit():
    """測試免費用戶超過 3 次限制"""
    # 模擬已使用 3 次
    set_usage_count('test_user', 3)

    # 第 4 次應該被拒絕
    response = client.post('/recommendations',
                          headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 403
    assert 'usage_limit_exceeded' in response.json()['detail']['error']

def test_pro_user_unlimited():
    """測試進階用戶無限制"""
    set_plan_type('test_user', 'pro')
    set_usage_count('test_user', 999)

    # 應該允許
    response = client.post('/recommendations',
                          headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
```

### Day 5-6：ECPay 整合

#### 任務清單

- [ ] **申請 ECPay 測試帳號**
  - 前往 https://www.ecpay.com.tw/
  - 填寫測試帳號申請表
  - 取得 MerchantID 和 HashKey/HashIV

- [ ] **建立 integrations/ecpay.py**
  ```python
  class ECPayService:
      def __init__(self):
          self.merchant_id = os.getenv('ECPAY_MERCHANT_ID')
          self.hash_key = os.getenv('ECPAY_HASH_KEY')
          self.hash_iv = os.getenv('ECPAY_HASH_IV')
          self.payment_url = os.getenv('ECPAY_PAYMENT_URL')

      def create_payment_order(self, order_data: dict) -> dict:
          """建立付款訂單"""
          # 1. 準備參數
          params = {
              'MerchantID': self.merchant_id,
              'MerchantTradeNo': order_data['order_id'],
              'MerchantTradeDate': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
              'PaymentType': 'aio',
              'TotalAmount': order_data['amount'],
              'TradeDesc': f"OderWhat {order_data['plan_name']} 訂閱",
              'ItemName': order_data['plan_name'],
              'ReturnURL': f"{BASE_URL}/payment/callback/ecpay",
              'ChoosePayment': 'Credit',
              'EncryptType': 1
          }

          # 2. 計算 CheckMacValue
          params['CheckMacValue'] = self._generate_check_mac_value(params)

          # 3. 建立付款 URL
          payment_url = f"{self.payment_url}?{urlencode(params)}"

          return {
              'payment_url': payment_url,
              'order_id': order_data['order_id']
          }

      def create_recurring_payment(self, user_id: str, plan: str) -> dict:
          """建立定期定額訂閱"""
          # ECPay 定期定額 API
          pass

      def verify_callback(self, callback_data: dict) -> bool:
          """驗證 ECPay 回調的 CheckMacValue"""
          received_mac = callback_data.pop('CheckMacValue')
          calculated_mac = self._generate_check_mac_value(callback_data)
          return received_mac == calculated_mac

      def _generate_check_mac_value(self, params: dict) -> str:
          """產生檢查碼"""
          # 按照 ECPay 規則排序並串接
          sorted_params = sorted(params.items())
          param_str = '&'.join([f"{k}={v}" for k, v in sorted_params])
          param_str = f"HashKey={self.hash_key}&{param_str}&HashIV={self.hash_iv}"

          # URL encode 後計算 MD5
          param_str = urllib.parse.quote_plus(param_str)
          return hashlib.md5(param_str.encode()).hexdigest().upper()
  ```

- [ ] **建立 routers/payment.py**
  ```python
  @router.post("/payment/create")
  async def create_payment(
      request: PaymentRequest,
      user_info: dict = Depends(get_current_user)
  ):
      user_id = user_info['sub']

      # 1. 驗證方案
      if request.plan_type not in ['basic', 'pro']:
          raise HTTPException(400, "無效的方案")

      # 2. 計算金額
      amount = calculate_amount(request.plan_type, request.billing_cycle)

      # 3. 建立訂單
      order = payment_service.create_order(
          user_id=user_id,
          plan_type=request.plan_type,
          billing_cycle=request.billing_cycle,
          amount=amount
      )

      # 4. 呼叫 ECPay API
      ecpay_result = ecpay_service.create_payment_order({
          'order_id': order['order_id'],
          'amount': amount,
          'plan_name': f"{request.plan_type}方案（{request.billing_cycle}）"
      })

      return {
          'order_id': order['order_id'],
          'payment_url': ecpay_result['payment_url'],
          'amount': amount,
          'expires_at': datetime.now() + timedelta(minutes=30)
      }

  @router.post("/payment/callback/ecpay")
  async def ecpay_callback(request: Request):
      # 1. 取得回調資料
      form_data = await request.form()
      callback_data = dict(form_data)

      # 2. 驗證 CheckMacValue
      if not ecpay_service.verify_callback(callback_data):
          return Response("0|CheckMacValue Error", status_code=400)

      # 3. 處理付款結果
      order_id = callback_data['MerchantTradeNo']
      rtn_code = int(callback_data['RtnCode'])

      if rtn_code == 1:  # 付款成功
          # 更新訂單
          payment_service.update_order_status(order_id, 'completed')

          # 更新使用者訂閱
          order = payment_service.get_order(order_id)
          subscription_service.create_subscription(
              user_id=order['user_id'],
              plan=order['plan_type'],
              cycle=order['billing_cycle']
          )

          return Response("1|OK")
      else:  # 付款失敗
          payment_service.update_order_status(order_id, 'failed')
          return Response("1|OK")
  ```

### Day 7：定期扣款實作

#### 任務清單

- [ ] **建立定期扣款排程**
  ```python
  # scheduled_tasks/subscription_renewal.py
  async def check_upcoming_renewals():
      """檢查即將到期的訂閱"""
      tomorrow = datetime.now() + timedelta(days=1)

      # 查詢明天要續約的使用者
      users = db.collection('users')\
                .where('subscription.next_billing_date', '>=', tomorrow)\
                .where('subscription.next_billing_date', '<', tomorrow + timedelta(days=1))\
                .stream()

      for user_doc in users:
          user_id = user_doc.id
          subscription = user_doc.to_dict()['subscription']

          # 觸發 ECPay 定期扣款
          result = ecpay_service.charge_recurring_payment(
              ecpay_member_id=subscription['ecpay_member_id'],
              amount=calculate_amount(subscription['plan_type'], subscription['billing_cycle'])
          )

          if result['success']:
              # 續約成功
              subscription_service.renew_subscription(user_id)
          else:
              # 續約失敗
              subscription_service.mark_payment_failed(user_id)
              # 發送通知 email
              send_payment_failed_email(user_id)
  ```

- [ ] **設定排程（使用 Cloud Scheduler 或 Cron）**
  ```yaml
  # cloud_scheduler_config.yaml
  - name: subscription-renewal-check
    schedule: "0 0 * * *"  # 每天午夜
    target: /scheduled/check-renewals
    retry_config:
      retry_count: 3
      max_backoff_duration: 3600s
  ```

---

## 階段 3：前端整合（5 天）

### Day 8-9：方案選擇與付款頁面

#### 任務清單

- [ ] **建立 pages/Subscription.tsx**
  ```tsx
  export default function SubscriptionPage() {
    const [plans, setPlans] = useState([]);
    const [currentPlan, setCurrentPlan] = useState(null);

    useEffect(() => {
      // 取得方案列表
      fetch('/subscriptions/plans')
        .then(res => res.json())
        .then(data => setPlans(data.plans));

      // 取得當前訂閱
      fetch('/subscriptions/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
        .then(res => res.json())
        .then(data => setCurrentPlan(data));
    }, []);

    return (
      <div>
        <h1>選擇方案</h1>
        <PlanComparison plans={plans} currentPlan={currentPlan} />
      </div>
    );
  }
  ```

- [ ] **建立 components/PlanCard.tsx**
  - 方案名稱、價格
  - 功能列表（打勾/打叉）
  - 選擇按鈕（月繳/年繳）
  - 「當前方案」標示

- [ ] **建立 components/PaymentFlow.tsx**
  ```tsx
  const handlePayment = async (planType, billingCycle) => {
    // 1. 建立訂單
    const response = await fetch('/payment/create', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ plan_type: planType, billing_cycle: billingCycle })
    });

    const { payment_url } = await response.json();

    // 2. 導向 ECPay 付款頁面
    window.location.href = payment_url;
  };
  ```

### Day 10：訂閱管理與使用量顯示

#### 任務清單

- [ ] **建立 components/UsageBadge.tsx**
  ```tsx
  export function UsageBadge({ usage }) {
    const { monthly_count, monthly_limit } = usage;
    const percentage = (monthly_count / monthly_limit) * 100;

    return (
      <div className="usage-badge">
        <div className="progress-bar" style={{ width: `${percentage}%` }} />
        <span>{monthly_count} / {monthly_limit} 次</span>
      </div>
    );
  }
  ```

- [ ] **建立 components/UpgradePrompt.tsx**
  - 當使用次數達 80% 時顯示
  - 當超過限制時顯示（modal）

- [ ] **建立 pages/SubscriptionManagement.tsx**
  ```tsx
  export default function SubscriptionManagement() {
    return (
      <div>
        <h2>訂閱管理</h2>

        {/* 當前方案 */}
        <CurrentPlanCard subscription={subscription} />

        {/* 使用量統計 */}
        <UsageStats usage={usage} />

        {/* 付款資訊 */}
        <PaymentInfo payment={subscription.payment_method} />

        {/* 操作按鈕 */}
        <ActionButtons>
          <button onClick={handleUpgrade}>升級方案</button>
          <button onClick={handleCancel}>取消訂閱</button>
        </ActionButtons>
      </div>
    );
  }
  ```

### Day 11-12：整合與調整

#### 任務清單

- [ ] **整合到導航列**
  - 新增「訂閱管理」連結
  - 顯示使用量 badge

- [ ] **整合到推薦流程**
  - 推薦前檢查使用量
  - 推薦後顯示剩餘次數

- [ ] **錯誤處理**
  - 付款失敗提示
  - 訂閱過期提示
  - 使用量超限提示

---

## 階段 4：測試與上線（3 天）

### Day 13：完整流程測試

#### 測試清單

- [ ] **免費用戶流程**
  1. 註冊新帳號
  2. 使用 3 次推薦
  3. 第 4 次應顯示升級提示
  4. 點擊升級，導向方案頁面

- [ ] **購買基礎方案流程**
  1. 選擇基礎方案（月繳）
  2. 導向 ECPay 付款頁面
  3. 使用測試信用卡完成付款
  4. 返回網站，檢查訂閱狀態
  5. 使用量應重置為 0/30

- [ ] **使用次數扣減**
  1. 執行推薦
  2. 檢查 Firestore usage.monthly_count 是否 +1
  3. 前端顯示的剩餘次數是否正確

- [ ] **升級方案流程**
  1. 從基礎升級到進階
  2. 付款成功後檢查方案是否更新
  3. 使用量限制應變為「無限制」

- [ ] **取消訂閱流程**
  1. 點擊「取消訂閱」
  2. 確認 modal
  3. 取消後應保留使用權限至期末
  4. 檢查 subscription.cancelled_at 是否記錄

### Day 14：壓力測試與修復

#### 測試場景

- [ ] **並發請求測試**
  ```python
  # 使用 locust 進行壓力測試
  from locust import HttpUser, task

  class SubscriptionUser(HttpUser):
      @task
      def get_recommendations(self):
          self.client.post("/recommendations",
                          json={...},
                          headers={'Authorization': f'Bearer {token}'})
  ```

- [ ] **邊界條件測試**
  - 恰好達到使用限制
  - 訂閱剛好到期
  - 付款失敗情境
  - Webhook 重複發送

- [ ] **安全性測試**
  - 嘗試偽造 Webhook
  - 嘗試修改使用次數
  - 嘗試跳過付款直接升級

### Day 15：正式環境部署

#### 部署清單

- [ ] **環境變數設定**
  ```bash
  # .env.production
  ECPAY_MERCHANT_ID=正式商店代號
  ECPAY_HASH_KEY=正式HashKey
  ECPAY_HASH_IV=正式HashIV
  ECPAY_PAYMENT_URL=https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5
  ```

- [ ] **Firestore 規則更新**
  ```javascript
  // 確保 users.usage 只能由後端更新
  match /users/{userId} {
    allow read: if request.auth.uid == userId;
    allow update: if request.auth.uid == userId
                  && !request.resource.data.diff(resource.data).affectedKeys()
                      .hasAny(['usage', 'subscription']);
  }
  ```

- [ ] **部署後端**
  ```bash
  gcloud run deploy oderwhat-api \
    --source . \
    --region asia-east1 \
    --allow-unauthenticated \
    --set-env-vars="$(cat .env.production)"
  ```

- [ ] **部署前端**
  ```bash
  npm run build
  firebase deploy --only hosting
  ```

- [ ] **設定 Cloud Scheduler**
  ```bash
  gcloud scheduler jobs create http subscription-renewal \
    --schedule="0 0 * * *" \
    --uri="https://api.carte.tw/scheduled/check-renewals" \
    --http-method=POST \
    --oidc-service-account-email=scheduler@project.iam.gserviceaccount.com
  ```

---

## 驗收標準

### 功能驗收

- [ ] 所有方案正確顯示
- [ ] 付款流程完整無誤
- [ ] 使用量正確扣減
- [ ] 訂閱狀態即時更新
- [ ] 定期扣款自動執行
- [ ] Email 通知正常發送

### 性能驗收

- [ ] API 回應時間 < 500ms
- [ ] 並發 100 使用者無錯誤
- [ ] Webhook 處理成功率 > 99%

### 安全驗證

- [ ] CheckMacValue 驗證通過
- [ ] 使用量無法手動修改
- [ ] 付款資訊不外洩
- [ ] HTTPS 全程加密

---

## 風險管理

### 技術風險

| 風險 | 機率 | 影響 | 應對 |
|-----|------|------|------|
| ECPay API 變更 | 低 | 高 | 訂閱官方更新通知 |
| Webhook 遺失 | 中 | 高 | 實作重試機制 + 手動對帳 |
| 並發競態條件 | 中 | 中 | 使用 Firestore Transaction |
| 定期扣款失敗 | 高 | 中 | 提供寬限期 + Email 通知 |

### 商業風險

| 風險 | 機率 | 影響 | 應對 |
|-----|------|------|------|
| 定價不當 | 中 | 高 | 提供早鳥優惠，收集反饋 |
| 使用者流失 | 中 | 高 | 提供免費方案過渡期 |
| 競爭對手出現 | 低 | 中 | 強化差異化功能 |

---

## 成功指標

### 第 1 個月

- [ ] 付費轉換率 > 5%
- [ ] 月活躍用戶 > 100
- [ ] 付款成功率 > 95%
- [ ] 客服工單 < 10 件

### 第 3 個月

- [ ] 付費用戶 > 50
- [ ] 月營收 > NT$ 5,000
- [ ] 留存率 > 60%
- [ ] NPS > 50

---

## 下一步行動

### 立即執行（Week 1）

1. [ ] 確認方案定價與功能（與團隊討論）
2. [ ] 申請 ECPay 商店帳號
3. [ ] 開始 Day 1 任務：建立 subscription_service.py

### 中期規劃（Month 2-3）

1. [ ] 新增年繳優惠活動
2. [ ] 實作推薦碼功能
3. [ ] 新增企業方案（B2B）

### 長期願景（Month 6+）

1. [ ] 國際化（支援 Stripe）
2. [ ] 動態定價（依使用量計費）
3. [ ] API 服務（開放給餐廳）

---

**計畫版本**: 1.0
**最後更新**: 2025-11-24
**負責人**: Stephen
**狀態**: ✅ 規劃完成，準備執行
