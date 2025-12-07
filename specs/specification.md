# AI 點餐經紀人 MVP 規格書 (v1.1 - 無 OCR 版)

**版本：** 1.1
**核心價值：** 解決消費者在陌生餐廳的點餐決策癱瘓，透過 AI 分析 Google 評論與網路食記，提供結構化的最佳點餐建議。

---

## 1\. 功能需求規格 (Functional Requirements)

### 1.1 輸入層 (Input Layer)

| 欄位 | 類型 | 邏輯/備註 |
| :--- | :--- | :--- |
| **餐廳資訊** | Text / Map Link | 串接 Google Places Autocomplete 確保找對店。 |
| **用餐模式** | **Radio Button** | **選項 A：大家分食 (Sharing)**<br>**選項 B：個人套餐 (Individual)**<br>*(此選項將決定後端 AI Agent 的核心邏輯)* |
| **人數** | Number | 用於計算總預算與推薦份量。 |
| **人均預算** | Number | 軟性限制 (Soft Constraint)，總價允許 10-15% 誤差。 |
| **禁忌/偏好** | Tags / Text | 例如：不吃牛、不吃辣、要喝酒、有長輩。 |

### 1.2 核心處理層 (AI Logic & RAG)

#### A. 資料源 (Data Source)

*   **主要 API:** Google Places API (New Version)。
*   **輔助 API:** Google Search (Custom Search JSON API)。
*   **資料獲取策略 (RAG - Retrieval-Augmented Generation):**
    1.  **Reviews:** 透過 Places API 抓取 `sort_by: new` (最新) 與 `sort_by: relevant` (最相關) 各 15 則，共 30 則評論文字。
    2.  **Menu Info:** 透過 Google Search 搜尋關鍵字「[餐廳名稱] 菜單」或「[餐廳名稱] 食記」，抓取 1-2 個最相關的網頁純文字內容。
    3.  **價格估算:** 優先從獲取的文字中，透過關鍵字 (如 `$`、`元`) 和正規表示式 (Regex) 進行價格估算。若無法估算，則標記 `price_estimated: true` 並可能使用預設值。

#### B. 生成邏輯 (Prompt Engineering Strategy)

AI Agent 必須嚴格遵守以下結構化邏輯：

*   **邏輯分支 1：分食模式 (Sharing Mode)**
    *   **規則：** 總份量約為 `人數 x 1.2` (飽足係數)。
    *   **結構強制：** 推薦組合中必須包含 [開胃菜/涼菜] + [主食/澱粉] + [肉類主菜] + [蔬菜] + [飲料/湯]。
    *   **防呆：** 禁止推薦超過 50% 的同類型食物 (例如全是炸物)。

*   **邏輯分支 2：獨享模式 (Individual Mode)**
    *   **規則：** 確保每人一份完整的 Set。
    *   **結構強制：** 輸出結構為 `(主餐 + 附餐/飲料)` 的組合，重複 `人數` 次。
    *   **公平性：** 各套餐的估算價格差異不可超過 20%。

### 1.3 輸出與互動層 (Output & UI)

#### A. 推薦結果

*   **分組顯示：** 依照菜色類別 (`category_name`) 進行分組，方便閱讀。
*   **推薦理由 (Social Proof)：** 必須從評論中摘要關鍵字或句子。
    *   *範例:* "45 則評論提到『皮超脆』"

#### B. 一鍵換菜 (Smart Swap)

*   **後端邏輯：** 後端在生成 JSON 時，針對每一個推薦位 (Slot)，必須預先生成 **1-2 個備選菜色 (`alternatives`)**。
*   **前端行為：** 用戶點擊「換一道」時，直接由前端替換為備選菜色，**無需重新呼叫 API**。

#### C. 點餐專用卡 (Waiter Card)

*   **UI 設計：** 高對比背景 (白底黑字)，超大字體。
*   **內容：** 僅顯示最終確認的「菜名」與「數量」。

---

## 2\. 資料結構 (JSON Response Schema)

後端回傳給前端的 JSON 必須嚴格遵守此格式，以支援「一鍵換菜」功能。

```json
{
  "restaurant_name": "String",
  "mode": "sharing | individual",
  "total_estimated_price": "Number",
  "currency": "TWD",
  "recommendation_groups": [
    {
      "category": "String (e.g., Appetizer)",
      "category_name": "String (e.g., 開胃前菜)",
      "selected_item": {
        "id": "String",
        "name": "String",
        "quantity": "Number",
        "price": "Number",
        "price_estimated": "Boolean",
        "reason": "String"
      },
      "alternatives": [
        {
          "id": "String",
          "name": "String",
          "quantity": "Number",
          "price": "Number",
          "price_estimated": "Boolean",
          "reason": "String"
        }
      ]
    }
  ]
}
```

---

## 3\. MVP 邊界與限制 (Out of Scope)

1.  **❌ 視覺辨識 (Vision OCR):** 不處理菜單圖片。
2.  **❌ 即時訂位:** 不串接訂位系統。
3.  **❌ 真實庫存檢查:** 無法知道當天是否售完。
4.  **❌ 使用者帳號系統:** 無需登入即可使用。