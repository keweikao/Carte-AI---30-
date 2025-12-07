# 專案核心基礎與開發哲學 (Project Core Foundation)

本文件統整了 **Spec-Driven Development**、**MCP Code Execution** 與 **Claude Code** 的核心概念，作為本專案所有 AI 協作者與開發者的共同知識庫。

## 1. 規格驅動開發 (Spec-Driven Development)
*來源: [GitHub Spec Kit](https://github.com/github/spec-kit)*

### 核心哲學
"先寫規格，再寫程式碼。" (Write specs, not code first.)
避免直接跳入實作細節，而是先釐清「意圖 (Intent)」與「需求 (Requirements)」。

### 開發五步驟
本專案嚴格遵循以下流程：

1.  **確立原則 (Principles / Constitution)**
    - 定義專案的「憲法」，包含程式碼風格、語言規範 (如：繁體中文)、測試標準。
    - *產出*: `.cursorrules`, `project_foundation.md`

2.  **規格定義 (Specify)**
    - 描述 **要做什麼 (What)** 與 **為什麼 (Why)**。
    - **禁止** 在此階段討論技術實作 (How)。
    - 專注於使用者故事、功能邊界與限制。
    - *產出*: `specs/xxx-feature-name.md`

3.  **實作計畫 (Plan)**
    - 描述 **如何做 (How)**。
    - 選擇技術堆疊、設計資料結構、規劃模組架構。
    - 必須驗證計畫的可行性。
    - *產出*: `implementation_plan.md`

4.  **任務拆解 (Tasks)**
    - 將計畫拆解為可獨立執行的細項任務 (Checklist)。
    - 每個任務應足夠小，以便於驗證與除錯。
    - *產出*: `task.md`

5.  **執行實作 (Implement)**
    - 依據任務清單逐一撰寫程式碼。
    - 隨時回頭驗證是否符合規格與計畫。

---

## 2. MCP 程式碼執行模式 (MCP Code Execution)
*來源: [Anthropic Engineering](https://www.anthropic.com/engineering/code-execution-with-mcp)*

### 核心問題：Token 消耗與脈絡超載
- 傳統 Agent 模式：`呼叫工具 A` -> `讀取結果` -> `思考` -> `呼叫工具 B`。
- 缺點：
    1.  中間結果 (Intermediate Results) 會佔用大量 Context Window。
    2.  來回互動次數多，延遲高且昂貴。

### 解決方案：以程式碼為工具 (Code as a Tool)
- **原則**：不要手動扮演「膠水」，而是撰寫「膠水程式碼 (Glue Code)」。
- **實踐**：
    - 當需要處理大量資料或連續步驟時，**編寫一個 Python/Shell Script** 來一次完成。
    - 讓 Script 在執行環境中處理資料，只回傳最終摘要給 AI。
    - *範例*：
        - ❌ 壞的模式：列出目錄 -> 讀取檔案 A -> 讀取檔案 B -> 讀取檔案 C -> 自己在腦中比對。
        - ✅ 好的模式：寫一個 Python script，遍歷目錄，讀取所有檔案，找出差異，並 print 出差異摘要。

### 效益
- **Token 節省**：可達 98% 以上 (根據 Anthropic 案例)。
- **準確度**：程式碼邏輯比 LLM 的模擬推理更可靠。

---

## 3. Agentic Workflow & Claude Code
*來源: [Claude Code Docs](https://code.claude.com/docs)*

### 核心精神
- **Unix 哲學**：工具應可組合 (Composable)。
- **工程師思維**：AI 不只是聊天機器人，而是能「採取行動」的工程師。
- **主動性 (Proactiveness)**：
    - 遇到錯誤時，主動分析 Log、嘗試修復，而非直接報錯停機 (除非陷入死胡同)。
    - 善用 Terminal 指令來探索環境。

### 最佳實踐
- **保持 Context 清潔**：善用 `grep`, `find`, `ls` 等指令先探索，再精準讀取檔案。
- **原子化提交**：完成一個小任務後即進行驗證與 Commit，避免累積過多變更導致除錯困難。

---

*本文件為專案之基石，任何開發決策均應回溯至此。*
