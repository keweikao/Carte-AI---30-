# 實作計畫：UI 改進、強制登入與資料整合

**建立日期**: 2025-11-21
**關聯規格**: `specs/ui-improvements-auth-data.md`
**預估工時**: 3-4 小時

---

## 1. 技術架構決策

### 1.1 移除首頁 (US-1)
**目標**: 訪問 `/` 時直接顯示輸入頁面

**技術方案**:
- **方案 A (推薦)**: 在 `app/page.tsx` 中直接重定向到 `/input`
  - 優點：保持路由結構清晰，簡單快速
  - 缺點：會有短暫的重定向跳轉

- **方案 B**: 將 `app/input/page.tsx` 內容移到 `app/page.tsx`
  - 優點：無重定向，更流暢
  - 缺點：需要重構路由結構

**最終決策**: 採用**方案 B**，將輸入頁面提升為根頁面
- 理由：提供最佳使用者體驗，避免不必要的重定向
- 保留 `/input` 路由作為別名（可選）

---

### 1.2 強制 Google 登入 (US-2)
**目標**: 未登入時無法輸入餐廳名稱

**技術方案**:
- 使用 `next-auth` 的 `useSession()` Hook 檢查登入狀態
- 未登入時：
  - 餐廳名稱 Input 設為 `disabled`
  - 顯示 Google 登入按鈕（使用 `signIn("google")`）
  - 加上視覺提示（Icon + 文字說明）

**實作細節**:
```typescript
const { data: session, status } = useSession();
const isAuthenticated = status === "authenticated";

// Input 條件渲染
<Input
  disabled={!isAuthenticated}
  placeholder={isAuthenticated ? "例如：鼎泰豐..." : "請先登入 Google"}
/>
```

**登入流程**:
1. 點擊「使用 Google 登入」按鈕
2. 觸發 `signIn("google")` → 跳轉 Google OAuth
3. 回調後自動返回當前頁面
4. `useSession()` 更新，Input 自動啟用

**Session 持久化**:
- NextAuth 預設使用 JWT + `httpOnly` Cookie
- Session 會在頁面刷新後保持（無需額外處理）

---

### 1.3 整合真實資料 (US-3)
**目標**: 移除測試資料，顯示真實 API 回應

**問題分析**:
根據 `agent/dining_agent.py` 第 27-61 行，測試資料出現的條件：
```python
if not GEMINI_API_KEY or "your_gemini_api_key" in GEMINI_API_KEY:
    # 返回模擬資料
```

**解決方案**:
- **檢查環境變數**: 確認 `.env` 中 `GEMINI_API_KEY` 已正確設定
- **修改 Fallback 邏輯**:
  - 移除模擬資料 Fallback
  - 當 API Key 缺失或無效時，直接返回友善錯誤訊息
  - 不要在生產環境顯示「模擬」字樣

**實作策略**:
1. **前端**: 不需修改（已正確呼叫 API）
2. **後端**: 修改 `dining_agent.py`
   - 移除第 27-61 行的模擬資料邏輯
   - 改為拋出 `HTTPException(400, "API Key not configured")`
3. **前端錯誤處理**: 在 `recommendation/page.tsx` 中捕獲錯誤，顯示：
   ```
   "無法取得餐廳資料，請稍後再試"
   ```

**資料驗證**:
- 確認 Gemini API 回應符合 Schema（`FullRecommendationResponse`）
- 測試無資料時的 Fallback 行為

---

## 2. 檔案變更清單

### 2.1 前端變更

#### `frontend/src/app/page.tsx` (重寫)
- 移除 Landing Page 的 UI (Hero Text, Background Image)
- 複製 `frontend/src/app/input/page.tsx` 的完整邏輯
- 整合 `useSession()` 進行登入檢查
- 條件渲染：未登入時顯示登入提示 + 停用 Input

#### `frontend/src/app/input/page.tsx` (選擇性)
- **選項 1**: 刪除此檔案（因已合併到 `page.tsx`）
- **選項 2**: 保留並重定向到 `/`
- **建議**: 刪除，避免路由混淆

#### `frontend/src/components/LoginButton.tsx` (檢查)
- 確認已正確使用 `signIn()` 和 `signOut()`
- 顯示使用者頭像/名稱（登入後）

### 2.2 後端變更

#### `agent/dining_agent.py` (修改)
- 移除第 27-61 行的模擬資料邏輯
- 移除第 147-179 行的備援模擬資料
- 改為拋出明確錯誤：
  ```python
  if not GEMINI_API_KEY or "your_gemini_api_key" in GEMINI_API_KEY:
      raise ValueError("Gemini API Key is not configured. Please set GEMINI_API_KEY in .env")
  ```

#### `main.py` (錯誤處理增強)
- 在 `/recommendations` Endpoint 中捕獲 `ValueError`
- 返回 HTTP 503 (Service Unavailable) 而非 500
  ```python
  except ValueError as e:
      raise HTTPException(status_code=503, detail=str(e))
  ```

### 2.3 環境變數驗證

#### `.env` (檢查)
確認以下變數已設定：
```bash
# Backend
GEMINI_API_KEY=AIza...  # 必須是有效的 Google AI API Key
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000  # 或 Production URL
NEXTAUTH_SECRET=...
NEXTAUTH_URL=http://localhost:3000
```

---

## 3. 資料流程圖

### 3.1 登入流程
```
使用者訪問 /
  ↓
檢查 Session (useSession)
  ↓
未登入 ──→ 顯示登入按鈕 + 停用 Input
  ↓
點擊登入 ──→ signIn("google") ──→ Google OAuth
  ↓
回調 /api/auth/callback/google
  ↓
Session 建立 ──→ Input 啟用
```

### 3.2 推薦流程（修改後）
```
使用者輸入餐廳 + 提交
  ↓
前端呼叫 /recommendations (帶 Bearer Token)
  ↓
後端驗證 Token (verify_google_token)
  ↓
檢查 GEMINI_API_KEY
  ↓
有效 ──→ 呼叫 Gemini API ──→ 返回真實推薦
  ↓
無效 ──→ 拋出 503 錯誤 ──→ 前端顯示友善訊息
```

---

## 4. 測試計畫

### 4.1 功能測試

#### US-1: 首頁移除
- [ ] 訪問 `/` 時，直接顯示餐廳輸入介面（無 Landing Page）
- [ ] 頁面無重定向閃爍
- [ ] 保留原有的 Step 1 / Step 2 流程

#### US-2: 強制登入
- [ ] 未登入時，餐廳名稱 Input 為停用狀態
- [ ] 顯示「使用 Google 登入」按鈕
- [ ] 點擊登入後，跳轉 Google OAuth
- [ ] 登入成功後，自動返回頁面且 Input 啟用
- [ ] 刷新頁面後，登入狀態保持

#### US-3: 真實資料
- [ ] 確認 `.env` 中 `GEMINI_API_KEY` 已設定
- [ ] 提交餐廳名稱後，顯示真實推薦（無「模擬」字樣）
- [ ] 若 API Key 無效，顯示友善錯誤訊息（而非模擬資料）
- [ ] 檢查推薦結果是否包含真實菜名、價格、評論

### 4.2 錯誤處理測試
- [ ] API Key 缺失 → 顯示「服務暫時無法使用」
- [ ] 網路錯誤 → 顯示「請檢查網路連線」
- [ ] Token 過期 → 自動觸發重新登入

### 4.3 效能測試
- [ ] 首次載入時間 < 2 秒
- [ ] 登入流程 < 3 秒
- [ ] 推薦生成 < 5 秒（含 Gemini API 呼叫）

---

## 5. 部署檢查清單

### 5.1 部署前
- [ ] 在 Dev 環境完成所有測試
- [ ] 確認 `.env` 變數已配置到 Production 環境
- [ ] 檢查 CORS 設定（`main.py` 第 17-21 行）
- [ ] 前端 `NEXT_PUBLIC_API_URL` 指向正確的後端 URL

### 5.2 部署後驗證
- [ ] 訪問 Production URL，確認首頁已變更
- [ ] 測試 Google 登入流程（使用真實 Google 帳號）
- [ ] 提交真實餐廳名稱，驗證推薦結果
- [ ] 檢查 Console Logs（確認無模擬資料相關訊息）

---

## 6. 風險評估與緩解

### 風險 1: 移除首頁後，使用者不知道這是什麼服務
**緩解**:
- 在輸入頁面頂部加上簡短標題：「AI 點餐助手」
- 在 Input placeholder 中加上引導文字

### 風險 2: 強制登入可能降低轉換率
**緩解**:
- 登入按鈕設計要顯眼且友善
- 提供「為什麼需要登入」的簡短說明（例如：「為您提供個人化推薦」）

### 風險 3: Gemini API 失敗時完全無法使用
**緩解**:
- 實作重試機制（已存在於 `dining_agent.py` 第 104-183 行）
- 在前端顯示「稍後再試」按鈕，而非讓使用者卡住

---

## 7. 後續優化建議

- **US-2 增強**: 支援其他登入方式（Facebook、Email）
- **US-3 增強**: 實作資料 Cache 層（減少 Gemini API 呼叫）
- **UX 改進**: 登入後顯示歡迎訊息（例如：「嗨，Stephen！」）
- **Analytics**: 追蹤登入率、推薦成功率

---

**下一步**: 建立 `task.md` 拆解具體執行任務
