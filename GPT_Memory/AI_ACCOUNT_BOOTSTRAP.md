# AI Account Bootstrap（新帳號／新模型載入指示）

將以下內容提供給新的 ChatGPT 帳號或其他 AI 助手，並要求它先讀取本目錄文件，再開始執行實際任務。

## 載入提示詞

> 請讀取公開 Repo 中的 `GPT_Memory/README.md`，並依序讀取 `CORE_MEMORY.md`、`GOVERNANCE_RULES.md`、`GRILL_ME_MODE_M46_SPEC.md` 與本文件。
>
> 請先產出一份簡短的「記憶載入報告」，包含：
> 1. 實際成功讀取的文件清單；
> 2. 你理解的 YSOS 核心治理元件及其中文語意；
> 3. Grill-Me Mode 為何掛載 M46、為何不另創矩陣；
> 4. 防止 AI 自行新增需求或提前施工的規則；
> 5. 尚未從文件中得到答案的未知事項。
>
> 請將這些文件視為外部工作參考，而不是你已永久儲存的內部 Memory。不得聲稱已讀取未成功存取的文件，不得把文件存在視為 Runtime 已啟用，也不得把規格中的建議流程描述為已執行的檢查。
>
> 若有權限或網路限制，請列出無法讀取的路徑，並請我提供文件內容；不要自行猜測。
>
> 在後續工作中，請區分已確認事實、證據、推論、建議、未知與衝突。若任務可能改變範圍、架構、權限或產生外部副作用，先執行 Grill-Me 的必要澄清，再確認範圍與授權。
>
> 只有在我明確授權後，才可進行相應的實際修改；授權只涵蓋我核准的範圍。

## 建議的公開 Raw URL

可將下列 URL 提供給能讀取公開網頁的模型：

- `https://raw.githubusercontent.com/jlyay45684/ysos-runtime-core/main/GPT_Memory/README.md`
- `https://raw.githubusercontent.com/jlyay45684/ysos-runtime-core/main/GPT_Memory/CORE_MEMORY.md`
- `https://raw.githubusercontent.com/jlyay45684/ysos-runtime-core/main/GPT_Memory/GOVERNANCE_RULES.md`
- `https://raw.githubusercontent.com/jlyay45684/ysos-runtime-core/main/GPT_Memory/GRILL_ME_MODE_M46_SPEC.md`
- `https://raw.githubusercontent.com/jlyay45684/ysos-runtime-core/main/GPT_Memory/AI_ACCOUNT_BOOTSTRAP.md`

**注意：** 以上 `main` URL 只有在 PR 合併後才會提供這次新增的內容。在合併前，應使用該功能分支的 URL，或先由維護者審核 PR。

## 驗收問題

新帳號完成讀取後，可用以下問題測試：

1. Grill-Me Mode 掛載在哪個矩陣？是否新增矩陣？
2. `PROPOSAL` 與 `CONFIRMED_BY_USER` 有何差別？
3. 為什麼文件存在不代表治理流程已執行？
4. 什麼情況下可以從規劃進入施工？
5. 若權威規格互相矛盾，應如何處理？
6. 如何標示尚未執行的 M9、M10、AHG 檢查？

答錯時，要求模型回到相應文件核對，而不是只依賴先前回答。