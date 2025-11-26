# 任務拆解：UI 改進、強制登入與資料整合

**關聯規格**: `specs/ui-improvements-auth-data.md`
**關聯計畫**: `implementation_plan.md`
**建立日期**: 2025-11-21

---

## 任務總覽

總共 **10 個主要任務**，預估總工時：**3-4 小時**

---

## Phase 1: 前端改造 (2 小時)

### Task 1.1: 重構根頁面 - 整合登入邏輯
**檔案**: `frontend/src/app/page.tsx`
**預估時間**: 40 分鐘

**步驟**:
1. [ ] 讀取 `frontend/src/app/input/page.tsx` 的完整程式碼
2. [ ] 複製 State 管理邏輯（`formData`, `step`）
3. [ ] 加入 `useSession()` Hook 進行登入狀態檢查
4. [ ] 修改 Step 1 的 Input 元件：
   - 新增 `disabled={status !== "authenticated"}` 屬性
   - 修改 placeholder 為條件渲染
5. [ ] 在 Input 上方加入登入提示區塊（未登入時顯示）：
   ```tsx
   {status === "unauthenticated" && (
     <div className="text-center mb-4">
       <p className="text-sm text-muted-foreground mb-2">請先登入以使用 AI 點餐</p>
       <Button onClick={() => signIn("google")}>使用 Google 登入</Button>
     </div>
   )}
   ```
6. [ ] 移除原有的 Landing Page UI（Hero Text、背景圖等）
7. [ ] 保留 `LoginButton` 元件在右上角

**驗收標準**:
- 訪問 `/` 直接顯示餐廳輸入介面
- 未登入時 Input 停用且顯示登入按鈕
- 登入後 Input 自動啟用

---

### Task 1.2: 移除舊的 Input 頁面
**檔案**: `frontend/src/app/input/page.tsx`
**預估時間**: 5 分鐘

**步驟**:
1. [ ] 刪除 `frontend/src/app/input/page.tsx`
2. [ ] 刪除 `frontend/src/app/input/` 目錄（如果為空）
3. [ ] 檢查是否有其他檔案引用 `/input` 路由（使用 grep）
4. [ ] 如有引用，修改為 `/`

**驗收標準**:
- `/input` 路由返回 404
- 無任何檔案引用 `/input`

---

### Task 1.3: 優化登入按鈕元件
**檔案**: `frontend/src/components/LoginButton.tsx`
**預估時間**: 15 分鐘

**步驟**:
1. [ ] 檢查現有 `LoginButton` 實作
2. [ ] 確保使用 `useSession()` 和 `signIn()` / `signOut()`
3. [ ] 登入後顯示使用者頭像 + 名稱（使用 `session.user.image` 和 `session.user.name`）
4. [ ] 加入 Loading 狀態（`status === "loading"` 時顯示 Spinner）

**驗收標準**:
- 登入後顯示使用者資訊
- 點擊可登出
- Loading 狀態正確顯示

---

### Task 1.4: 改善錯誤處理 UI
**檔案**: `frontend/src/app/recommendation/page.tsx`
**預估時間**: 20 分鐘

**步驟**:
1. [ ] 在 `fetchData()` 的 `catch` 區塊中，解析錯誤訊息
2. [ ] 根據錯誤類型顯示不同訊息：
   - 503 → "服務暫時無法使用，請稍後再試"
   - 401 → "登入已過期，請重新登入"
   - 其他 → "無法取得推薦，請檢查網路連線"
3. [ ] 在錯誤畫面加入「返回首頁」和「重試」按鈕

**驗收標準**:
- 不同錯誤顯示對應訊息
- 使用者可輕鬆返回或重試

---

### Task 1.5: 前端環境變數檢查
**檔案**: `frontend/.env.local`
**預估時間**: 10 分鐘

**步驟**:
1. [ ] 確認以下變數存在且正確：
   ```bash
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXTAUTH_SECRET=your_secret_here
   NEXTAUTH_URL=http://localhost:3000
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   ```
2. [ ] 測試 `NEXT_PUBLIC_API_URL` 是否可連接（使用 `curl` 或瀏覽器）

**驗收標準**:
- 所有必要變數已設定
- API URL 可正常連接

---

## Phase 2: 後端改造 (1 小時)

### Task 2.1: 移除模擬資料邏輯
**檔案**: `agent/dining_agent.py`
**預估時間**: 15 分鐘

**步驟**:
1. [ ] 刪除第 27-61 行（初始模擬資料 Fallback）
2. [ ] 改為拋出明確錯誤：
   ```python
   if not GEMINI_API_KEY or "your_gemini_api_key" in GEMINI_API_KEY:
       raise ValueError("Gemini API Key is not configured. Please set GEMINI_API_KEY in .env")
   ```
3. [ ] 刪除第 147-179 行（備援模擬資料）
4. [ ] 保留第 129-138 行的 `alternatives` Fallback（這是合理的）

**驗收標準**:
- API Key 缺失時拋出 `ValueError`
- 不再返回包含「模擬」字樣的資料

---

### Task 2.2: 改善 API 錯誤處理
**檔案**: `main.py`
**預估時間**: 15 分鐘

**步驟**:
1. [ ] 在 `/recommendations` Endpoint 中加入 `try-except` 區塊
2. [ ] 捕獲 `ValueError` 並返回 HTTP 503：
   ```python
   try:
       response = await agent.get_recommendations(request)
       return response
   except ValueError as e:
       raise HTTPException(status_code=503, detail=f"Service configuration error: {str(e)}")
   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))
   ```

**驗收標準**:
- API Key 缺失時返回 503（而非 500）
- 錯誤訊息清晰且不洩漏敏感資訊

---

### Task 2.3: 後端環境變數檢查
**檔案**: `.env`
**預估時間**: 10 分鐘

**步驟**:
1. [ ] 確認以下變數存在且正確：
   ```bash
   GEMINI_API_KEY=AIzaSy...  # 有效的 Google AI API Key
   GOOGLE_CLIENT_ID=...
   GOOGLE_CLIENT_SECRET=...
   GOOGLE_PLACES_API_KEY=...  # 如果有使用 Places API
   ```
2. [ ] 測試 Gemini API Key 是否有效（呼叫一次簡單的 API）

**驗收標準**:
- 所有必要變數已設定
- API Key 可正常使用

---

### Task 2.4: 加強日誌記錄
**檔案**: `agent/dining_agent.py`
**預估時間**: 10 分鐘

**步驟**:
1. [ ] 在 Gemini API 呼叫成功後，記錄推薦數量：
   ```python
   print(f"Successfully generated {len(data['recommendations'])} recommendations.")
   ```
2. [ ] 在錯誤處理中，記錄完整錯誤堆疊：
   ```python
   import traceback
   print(f"Error: {e}\n{traceback.format_exc()}")
   ```

**驗收標準**:
- 成功和失敗都有清楚的日誌
- 便於除錯

---

## Phase 3: 測試與驗證 (1 小時)

### Task 3.1: 本地端到端測試
**預估時間**: 30 分鐘

**步驟**:
1. [ ] 啟動後端：`cd /Users/stephen/Desktop/OderWhat && python main.py`
2. [ ] 啟動前端：`cd frontend && npm run dev`
3. [ ] 測試流程：
   - [ ] 訪問 `http://localhost:3000/`
   - [ ] 確認顯示輸入頁面（無 Landing Page）
   - [ ] 未登入時，Input 應為停用狀態
   - [ ] 點擊「使用 Google 登入」
   - [ ] 完成 OAuth 流程
   - [ ] 登入後，Input 啟用
   - [ ] 輸入真實餐廳名稱（例如：「鼎泰豐」）
   - [ ] 提交並等待推薦
   - [ ] 確認顯示真實資料（無「模擬」字樣）
   - [ ] 檢查價格、菜名、評論是否合理

**驗收標準**:
- 完整流程可順利執行
- 無模擬資料出現
- 推薦結果合理

---

### Task 3.2: 錯誤場景測試
**預估時間**: 20 分鐘

**步驟**:
1. [ ] **場景 1: API Key 缺失**
   - 暫時移除 `.env` 中的 `GEMINI_API_KEY`
   - 重啟後端
   - 提交餐廳名稱
   - 預期：前端顯示「服務暫時無法使用」
2. [ ] **場景 2: 未登入狀態**
   - 清除瀏覽器 Cookie
   - 訪問首頁
   - 預期：Input 停用，顯示登入按鈕
3. [ ] **場景 3: Token 過期**（選擇性，可跳過）
   - 手動修改 Cookie 中的 Token
   - 提交請求
   - 預期：返回 401，前端提示重新登入

**驗收標準**:
- 所有錯誤場景都有友善提示
- 不會顯示技術錯誤訊息給使用者

---

### Task 3.3: 文件更新與清理
**預估時間**: 10 分鐘

**步驟**:
1. [ ] 更新 `README.md`（如果有）：
   - 說明根路徑 `/` 現在是輸入頁面
   - 更新登入要求的說明
2. [ ] 刪除任何過時的文件或註解
3. [ ] 在 `implementation_plan.md` 底部加上「已完成」標記

**驗收標準**:
- 文件與實際程式碼一致
- 無過時資訊

---

## 檢查清單總結

**Phase 1: 前端**
- [ ] Task 1.1: 重構根頁面
- [ ] Task 1.2: 移除舊 Input 頁面
- [ ] Task 1.3: 優化登入按鈕
- [ ] Task 1.4: 改善錯誤處理
- [ ] Task 1.5: 環境變數檢查

**Phase 2: 後端**
- [ ] Task 2.1: 移除模擬資料
- [ ] Task 2.2: 改善錯誤處理
- [ ] Task 2.3: 環境變數檢查
- [ ] Task 2.4: 加強日誌

**Phase 3: 測試**
- [ ] Task 3.1: 端到端測試
- [ ] Task 3.2: 錯誤場景測試
- [ ] Task 3.3: 文件更新

---

## 執行順序建議

1. **先完成 Phase 2（後端）**: 確保資料源正確
2. **再執行 Phase 1（前端）**: 整合登入與 UI
3. **最後 Phase 3（測試）**: 驗證完整流程

---

**下一步**: 開始執行 Task 2.1（移除後端模擬資料）
