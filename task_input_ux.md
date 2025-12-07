# Input 頁面 UX 優化任務清單

## Phase 1: 準備工作
- [x] 建立規格文件 `specs/input-page-ux-improvements.md`
- [x] 建立實作計畫 `implementation_plan.md`
- [x] 建立任務清單 `task_input_ux.md`
- [ ] 讀取並分析現有 input page 程式碼

## Phase 2: 簡單修改（優先執行）

### Task 1: 標題文案修改
- [ ] 在 `frontend/src/app/input/page.tsx` 中找到標題位置
- [ ] 將「客製化你的餐點」改為「開啟你的美食探索之旅」
- [ ] 確認標題在不同螢幕尺寸下正常顯示
- [ ] 提交變更

### Task 2: 新增返回按鈕
- [ ] 檢查頁面頂部是否有 header 區域
- [ ] 如果沒有，建立 header 區域
- [ ] 新增返回按鈕（ArrowLeft icon + 「返回」文字）
- [ ] 實作 `router.back()` 功能
- [ ] 測試返回功能
- [ ] 確認響應式設計（手機版可能只顯示圖示）
- [ ] 提交變更

### Task 3: 預算金額輸入優化
- [ ] 找到數字輸入框（type="number"）
- [ ] 修改 value 邏輯：當值為 "0" 時顯示空字串
- [ ] 新增 placeholder：「例如：500」
- [ ] 調整 Slider 預設值邏輯
- [ ] 測試輸入框與 slider 雙向同步
- [ ] 測試空值處理
- [ ] 提交變更

## Phase 3: 視覺優化

### Task 4: 預算類型選擇器視覺優化
- [ ] 找到預算類型選擇器按鈕組（第 330-345 行附近）
- [ ] 匯入所需 icons：`import { User, Users } from "lucide-react"`
- [ ] 修改按鈕樣式：
  - [ ] 選中狀態：加強 border 和 shadow
  - [ ] 未選中狀態：加入 hover 效果
  - [ ] 調整 padding 和 font-size
- [ ] 為每個按鈕加入 icon（User / Users）
- [ ] 測試 hover 效果
- [ ] 測試切換功能
- [ ] 測試響應式設計
- [ ] 提交變更

## Phase 4: 飲食偏好重新設計（最複雜）

### Task 5: 定義新的飲食偏好選項
- [ ] 在 input page 頂部定義 `dietaryOptions` 常數
- [ ] 包含所有新選項（7 個）
- [ ] 每個選項包含：id, label, description, legacy
- [ ] 提交變更

### Task 6: 新增狀態管理
- [ ] 新增 `dietaryPreferences` state（string[]）
- [ ] 新增 `dietaryCustomNote` state（string）
- [ ] 移除或保留舊的 `formData.dietary_restrictions`（待決定）
- [ ] 提交變更

### Task 7: 實作新的飲食偏好 UI
- [ ] 找到現有的飲食偏好區塊
- [ ] 修改標題為「用餐風格偏好」
- [ ] 實作新的選項卡片（grid layout）
- [ ] 實作多選邏輯
- [ ] 新增自由輸入框（Textarea）
- [ ] 匯入 Textarea 元件：`import { Textarea } from "@/components/ui/textarea"`
- [ ] 設定 placeholder
- [ ] 測試多選功能
- [ ] 測試自由輸入功能
- [ ] 確認響應式設計（手機版為單欄）
- [ ] 提交變更

### Task 8: 實作資料轉換邏輯
- [ ] 在提交函數中加入轉換邏輯
- [ ] 將新選項轉換為舊格式（legacyDietary）
- [ ] 處理 `dietaryCustomNote`（暫時可以忽略，或記錄到 console）
- [ ] 測試轉換邏輯正確性
- [ ] 提交變更

## Phase 5: 整合測試

### Task 9: 功能測試
- [ ] 測試標題正確顯示
- [ ] 測試返回按鈕功能
- [ ] 測試預算類型選擇器切換
- [ ] 測試預算金額輸入（包含 placeholder、空值處理）
- [ ] 測試飲食偏好多選
- [ ] 測試飲食偏好自由輸入
- [ ] 測試表單提交（導航到 recommendation 頁面）
- [ ] 測試資料格式正確傳遞

### Task 10: 視覺與響應式測試
- [ ] 測試手機版（< 640px）
- [ ] 測試平板版（640px - 1024px）
- [ ] 測試桌面版（> 1024px）
- [ ] 測試所有 hover 效果
- [ ] 測試所有 focus 效果
- [ ] 檢查顏色對比度

### Task 11: 建置測試
- [ ] 執行 `npm run build`
- [ ] 確認無 TypeScript 錯誤
- [ ] 確認無 ESLint 警告
- [ ] 修正所有建置錯誤（如果有）

## Phase 6: 文件與收尾

### Task 12: 文件更新
- [ ] 更新相關註解
- [ ] 確認所有 ARIA 標籤正確
- [ ] 檢查是否有需要更新的文件

### Task 13: 最終檢查
- [ ] 與規格文件核對，確認所有需求都已實作
- [ ] 與實作計畫核對，確認所有步驟都已完成
- [ ] 執行完整的功能測試流程
- [ ] 準備 demo 或截圖

---

## 執行注意事項

1. **每完成一個 Task 就提交一次**，保持原子化提交
2. **按照 Phase 順序執行**，避免跳躍式開發
3. **遇到問題立即記錄**，並評估是否需要調整計畫
4. **保持與規格文件的一致性**，如有疑問回頭檢查規格
5. **優先保證功能正確**，再優化視覺效果

## 當前狀態
- 目前在：Phase 1（準備工作）
- 下一步：讀取 input page 程式碼並開始 Task 1
