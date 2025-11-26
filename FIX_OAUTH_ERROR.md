# 修正 OAuth Redirect URI 錯誤

## 錯誤訊息
```
Error 400: redirect_uri_mismatch
```

## 原因
Google Cloud Console 中的 OAuth Client ID 沒有包含本機開發用的 Redirect URI。

---

## 🔧 修正步驟（圖文說明）

### 步驟 1：訪問 Google Cloud Console

點擊以下連結（會直接導向您的 OAuth Client 設定頁面）：

**直接連結**：
```
https://console.cloud.google.com/apis/credentials/oauthclient/1045148759148-u90ianu8j1vvep9nahm3862ee0nva5ps.apps.googleusercontent.com?project=1045148759148
```

或手動導航：
1. 訪問 https://console.cloud.google.com/
2. 選擇專案（Project ID: `1045148759148`）
3. 左側選單：API 和服務 → 憑證
4. 找到 OAuth 2.0 用戶端 ID
5. 點擊用戶端 ID 名稱或編輯圖示（鉛筆）

---

### 步驟 2：找到「已授權的重新導向 URI」區塊

在編輯頁面中，向下捲動找到：
```
已授權的重新導向 URI (Authorized redirect URIs)
```

---

### 步驟 3：新增本機開發用的 URI

點擊「新增 URI」按鈕，然後逐一新增以下兩個 URI：

```
http://localhost:3000/api/auth/callback/google
```

```
http://127.0.0.1:3000/api/auth/callback/google
```

**注意**：
- 必須是 `http://`（本機開發用，不是 https）
- 必須包含完整路徑 `/api/auth/callback/google`
- 不要有結尾的斜線 `/`

---

### 步驟 4：確認完整的 URI 列表

您的「已授權的重新導向 URI」應該包含：

**本機開發**：
- ✅ http://localhost:3000/api/auth/callback/google
- ✅ http://127.0.0.1:3000/api/auth/callback/google

**生產環境**（如果已有）：
- ✅ https://dining-frontend-1045148759148.asia-east1.run.app/api/auth/callback/google
- ✅ https://www.carte.tw/api/auth/callback/google

---

### 步驟 5：儲存設定

1. 確認所有 URI 都正確無誤
2. 點擊頁面底部的「儲存」按鈕
3. 等待確認訊息出現

---

### 步驟 6：等待生效

Google OAuth 設定更新後需要幾秒鐘生效：
- **建議等待**：10-30 秒
- **清除瀏覽器快取**：按 `Cmd+Shift+R` (Mac) 或 `Ctrl+Shift+R` (Windows)

---

### 步驟 7：重新測試登入

1. 回到 http://localhost:3000
2. 重新整理頁面（`Cmd+R` 或 `F5`）
3. 點擊「使用 Google 登入」
4. 這次應該可以成功！

---

## ✅ 成功標誌

登入成功後，您應該看到：
1. 右上角顯示您的 Google 頭像和名稱
2. 餐廳名稱 Input 自動啟用（不再是灰色）
3. 可以正常輸入餐廳名稱

---

## 🐛 如果還是失敗

### 檢查清單：

1. **URI 拼寫正確嗎？**
   - 確認沒有多餘的空格
   - 確認是 `http://` 不是 `https://`
   - 確認是 `/api/auth/callback/google` 不是其他路徑

2. **等待時間夠嗎？**
   - 再等 30 秒試試

3. **瀏覽器快取清除了嗎？**
   - 嘗試使用無痕模式（Incognito）

4. **專案 ID 正確嗎？**
   - 確認您在正確的 GCP 專案中

---

## 📞 需要協助

如果以上步驟都無法解決，請提供：
1. Google Console 中目前設定的所有 Redirect URIs 截圖
2. 瀏覽器中完整的錯誤訊息
3. 瀏覽器 URL 列中的完整網址

---

**完成後請告訴我結果！** 🚀
