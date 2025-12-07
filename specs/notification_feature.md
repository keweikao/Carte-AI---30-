# Web Push Notification Feature Specification

## 1. 目標
當使用者在等待推薦結果時離開瀏覽器（切換分頁或最小化），若推薦生成完成，系統應發送瀏覽器通知，提醒使用者查看結果。

## 2. 使用者流程 (User Flow)
1.  使用者進入 `/waiting` 頁面。
2.  頁面顯示「開啟通知」按鈕（或自動詢問）。
3.  使用者點擊允許。
4.  使用者切換到其他視窗工作。
5.  後端完成推薦生成。
6.  使用者收到系統通知：「您的 [餐廳名稱] 菜單分析已完成！點擊查看」。
7.  使用者點擊通知，瀏覽器自動切換回 `/recommendation` 頁面。

## 3. 技術架構

### 3.1 前端 (Frontend)
- **Service Worker**: 需要註冊一個 Service Worker (`public/sw.js`) 來處理背景推播。
- **Notification API**: 使用 `Notification.requestPermission()` 請求權限。
- **Push API**: 使用 `pushManager.subscribe()` 取得 `PushSubscription`。

### 3.2 後端 (Backend)
- **儲存訂閱**: 需要一個新的 Firestore collection `push_subscriptions` 或在 `recommendation_jobs` 中儲存 subscription info。
- **發送推播**: 使用 `pywebpush` library 發送通知。
- **VAPID Keys**: 需要生成 VAPID 公私鑰對來驗證推播服務。

## 4. 實作細節

### 4.1 VAPID Key 生成
```bash
# 生成 VAPID keys
openssl ecparam -name prime256v1 -genkey -noout -out vapid_private.pem
openssl ec -in vapid_private.pem -pubout -out vapid_public.pem
```

### 4.2 前端 Service Worker (`public/sw.js`)
```javascript
self.addEventListener('push', function(event) {
  const data = event.data.json();
  const options = {
    body: data.body,
    icon: '/icons/icon-192x192.png',
    badge: '/icons/badge-72x72.png',
    data: {
      url: data.url
    }
  };

  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  event.waitUntil(
    clients.openWindow(event.notification.data.url)
  );
});
```

### 4.3 前端組件 (`NotificationButton.tsx`)
```typescript
const subscribeUser = async () => {
    const registration = await navigator.serviceWorker.ready;
    const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY!)
    });

    // Send subscription to backend
    await fetch('/api/notifications/subscribe', {
        method: 'POST',
        body: JSON.stringify({
            subscription,
            jobId: currentJobId
        })
    });
};
```

### 4.4 後端 API (`services/notification_service.py`)
```python
from pywebpush import webpush, WebPushException

def send_notification(subscription_info, message, url):
    try:
        webpush(
            subscription_info=subscription_info,
            data=json.dumps({"title": "Carte AI", "body": message, "url": url}),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": "mailto:admin@carte.ai"}
        )
    except WebPushException as ex:
        print("Web Push failed: {}", ex)
```

## 5. 實作計畫

### Phase 1: 基礎建設
- [ ] 生成 VAPID Keys 並設定環境變數。
- [ ] 建立 `public/sw.js`。
- [ ] 在 `layout.tsx` 或 `_app.tsx` 註冊 Service Worker。

### Phase 2: 前端整合
- [ ] 在 `TransparencyStream` 或 `WaitingPage` 加入「開啟通知」按鈕。
- [ ] 實作訂閱邏輯並傳送給後端。

### Phase 3: 後端整合
- [ ] 更新 `POST /v2/recommendations` 流程，接收 subscription。
- [ ] 在推薦生成完成時 (Job Completed)，觸發推播發送。
