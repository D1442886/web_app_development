# 路由設計文件 (ROUTES)：任務管理系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 任務列表與首頁 | GET | `/` | `templates/index.html` | 顯示所有任務，可接受 `?filter=` 進行過濾 |
| 建立任務 | POST | `/tasks` | — | 接收新增表單，存入 DB，然後重導向回首頁 |
| 切換任務狀態 | POST | `/tasks/<int:id>/toggle` | — | 更新該任務的 Boolean 狀態，重導向回首頁 |
| 刪除任務 | POST | `/tasks/<int:id>/delete` | — | 刪除並重導向回首頁 |

> URL 設計說明：基於 RESTful 慣例，我們使用名詞 `/tasks` 來對應新增操作。因受限於 HTML 表單僅支援 GET/POST，因此對於更新與刪除操作，我們採用 `/tasks/<id>/action` 的方式搭配 POST 方法執行。

## 2. 每個路由的詳細說明

### 2.1 `GET /` (任務列表)
- **輸入**：
  - URL Query: `filter` (其值可為 `completed`, `uncompleted`)
- **處理邏輯**：
  - 呼叫 `TaskModel.get_all(filter)` 取得相關任務的物件陣列。
- **輸出**：
  - 渲染 `index.html`。傳遞變數 `tasks` 與目前的 `current_filter` 供樣板判斷狀態標籤。
- **錯誤處理**：
  - 若找不到任務則顯示「尚無任務」的提示資訊。

### 2.2 `POST /tasks` (建立任務)
- **輸入**：
  - 表單欄位: `title` (必填)
- **處理邏輯**：
  - 驗證 `title` 是否空白。如果有效，呼叫 `TaskModel.create(title)` 寫入資料庫。
- **輸出**：
  - HTTP 302 重導向回到 `/` 首頁。
- **錯誤處理**：
  - 若 `title` 為空，可透過 Flask 的 `flash()` 功能回傳錯誤訊息 ("任務標題不能為空") 給前端顯示，並照常重導向至首頁。

### 2.3 `POST /tasks/<int:id>/toggle` (切換狀態)
- **輸入**：
  - URL 參數 (Path Parameter): `id`
- **處理邏輯**：
  - 呼叫 `TaskModel.toggle_status(id)` 進行「完成 <=> 未完成」的翻轉。
- **輸出**：
  - HTTP 302 重導向回到 `/` 首頁。
- **錯誤處理**：
  - 如果資料庫內找不到對應 `id` 的紀錄，忽略錯誤並安全重導向。

### 2.4 `POST /tasks/<int:id>/delete` (刪除任務)
- **輸入**：
  - URL 參數 (Path Parameter): `id`
- **處理邏輯**：
  - 呼叫 `TaskModel.delete(id)` 從資料庫刪除整筆資料。
- **輸出**：
  - HTTP 302 重導向回到 `/` 首頁。
- **錯誤處理**：
  - 同上，若找不到 ID 則忽略並安全重導向。

## 3. Jinja2 模板清單

在此架構中，所有的畫面會集中在首頁完成，因此僅需兩個 HTML：

| 檔案名稱 | 說明 | 繼承 |
| :--- | :--- | :--- |
| `templates/base.html` | 整個網站的基礎骨架（包含 Header、內容區與 Footer 等基礎 HTML 結構，以及引用 CSS/JS） | - |
| `templates/index.html` | 任務管理主介面（包含新增任務的表單，以及所有列出的清單與操作按鈕） | 繼承自 `base.html` |
