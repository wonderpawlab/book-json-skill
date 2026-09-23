# Book JSON Skill

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

將英語詞表、PDF、掃描文件或照片製作成個人詞彙書 `book.json`。使用者指定釋義語言，AI 擷取目標詞彙、補充例句與譯文，並依照專案內的範本檢查結果。

這是一個 **AI Agent Skill**，附有獨立的 Python 驗證工具。內容生成、PDF 讀取及圖片辨識由使用 Skill 的 AI 完成；單獨執行驗證程式不會擷取、翻譯或生成詞彙。

## 可以產生什麼

- 使用指定語言的釋義，例如英語、簡體中文、繁體中文、日語或韓語。
- **每個義項組**都有英文例句和對應語言的譯文。
- 可選的課程結構：`Lesson 2`、`Unit 1 / Lesson 2` 儲存在 `word.unit`；沒有課程分組的書省略此欄位。
- 連續的字串編號；同一課程內合併重複詞條，不同課程保留獨立紀錄。
- 無法查證的音標使用空字串，並在檔案外說明缺漏資訊。
- 建立新書，或將詞彙補充至使用者提供的現有書籍，輸出合併結果。

輸出格式適用於支援本專案 [書籍格式規範](skills/book-json/references/book_template.md) 的應用程式，並非所有詞彙軟體通用的交換格式。匯入應用程式支援的釋義語言可能少於本 Skill 能產生的語言。

## 安裝

下載 ZIP 並解壓縮，或使用 Git 複製此儲存庫，再依使用的工具選擇下列安裝方式。請複製 **整個** `skills/book-json` 資料夾，不能只複製 `SKILL.md`，否則會缺少範本、參考文件與驗證工具。建議使用「個人使用」位置，讓不同專案都能使用；若只想在某個專案使用，則選擇該專案的位置。

路徑中的 `alice` 與 `my-study` 僅為範例，請換成自己的使用者名稱與實際專案路徑。`%USERPROFILE%`（Windows）與 `~`（macOS）代表目前使用者的家目錄，無需替換。下列 Windows 位置適用於原生 Windows；若在 WSL 內執行工具，請使用 WSL 的 Linux 家目錄，例如 `~/.claude/skills/book-json/` 或 `~/.agents/skills/book-json/`。

### Claude Code

Claude Code 使用 `.claude/skills` 目錄。安裝後可輸入 `/book-json` 呼叫本 Skill。目錄與呼叫方式依據 [Claude Code 官方 Skills 文件](https://code.claude.com/docs/en/skills)。

#### Windows

| 使用範圍 | 目標位置 | 完整路徑範例 |
| --- | --- | --- |
| 個人使用（建議） | `%USERPROFILE%\.claude\skills\book-json\` | `C:\Users\alice\.claude\skills\book-json\` |
| 單一專案 | `<專案根目錄>\.claude\skills\book-json\` | `C:\Projects\my-study\.claude\skills\book-json\` |

快速找到個人安裝位置：

1. 按 **Win + E** 開啟檔案總管，再按 **Ctrl + L** 選取網址列。
2. 貼上 `%USERPROFILE%`，按 Enter，進入目前使用者的資料夾。
3. 在此建立缺少的 `.claude` 資料夾，再於其中建立 `skills` 資料夾。如果目錄已存在，可直接在網址列貼上 `%USERPROFILE%\.claude\skills` 開啟。
4. 將解壓縮專案中的 **整個** `skills\book-json` 資料夾複製到這個 `skills` 目錄內。
5. 確認最終檔案位置為 `%USERPROFILE%\.claude\skills\book-json\SKILL.md`。

若採單一專案安裝，請在實際專案根目錄內建立 `.claude\skills`，再放入完整的 `book-json` 資料夾。例如，最終檔案位置為 `C:\Projects\my-study\.claude\skills\book-json\SKILL.md`。

#### macOS

| 使用範圍 | 目標位置 | 完整路徑範例 |
| --- | --- | --- |
| 個人使用（建議） | `~/.claude/skills/book-json/` | `/Users/alice/.claude/skills/book-json/` |
| 單一專案 | `<專案根目錄>/.claude/skills/book-json/` | `/Users/alice/Projects/my-study/.claude/skills/book-json/` |

快速找到個人安裝位置：

1. 開啟 **Finder**，按 **Command + Shift + G**，貼上 `~/.claude/skills/`，按 Return。
2. 如果目錄尚未建立，開啟「終端機」，依序執行以下兩行，建立並開啟目錄：

   ```sh
   mkdir -p "$HOME/.claude/skills"
   open "$HOME/.claude/skills"
   ```

3. 將解壓縮專案中的 **整個** `skills/book-json` 資料夾複製到這個 `skills` 目錄內。
4. 確認最終檔案位置為 `~/.claude/skills/book-json/SKILL.md`。需要顯示隱藏資料夾時，在 Finder 按 **Command + Shift + .**。

若採單一專案安裝，請在實際專案根目錄內建立 `.claude/skills`，再放入完整的 `book-json` 資料夾。例如，最終檔案位置為 `/Users/alice/Projects/my-study/.claude/skills/book-json/SKILL.md`。

### Codex

Codex 使用 `.agents/skills` 目錄。在 Codex CLI/IDE 中可輸入 `$book-json` 呼叫本 Skill。目錄與呼叫方式依據 [Codex 官方本機 Skill 文件](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)。

#### Windows

| 使用範圍 | 目標位置 | 完整路徑範例 |
| --- | --- | --- |
| 個人使用（建議） | `%USERPROFILE%\.agents\skills\book-json\` | `C:\Users\alice\.agents\skills\book-json\` |
| 單一專案 | `<專案根目錄>\.agents\skills\book-json\` | `C:\Projects\my-study\.agents\skills\book-json\` |

快速找到個人安裝位置：

1. 按 **Win + E** 開啟檔案總管，再按 **Ctrl + L** 選取網址列。
2. 貼上 `%USERPROFILE%`，按 Enter，進入目前使用者的資料夾。
3. 在此建立缺少的 `.agents` 資料夾，再於其中建立 `skills` 資料夾。如果目錄已存在，可直接在網址列貼上 `%USERPROFILE%\.agents\skills` 開啟。
4. 將解壓縮專案中的 **整個** `skills\book-json` 資料夾複製到這個 `skills` 目錄內。
5. 確認最終檔案位置為 `%USERPROFILE%\.agents\skills\book-json\SKILL.md`。

若採單一專案安裝，請在實際專案根目錄內建立 `.agents\skills`，再放入完整的 `book-json` 資料夾。例如，最終檔案位置為 `C:\Projects\my-study\.agents\skills\book-json\SKILL.md`。

#### macOS

| 使用範圍 | 目標位置 | 完整路徑範例 |
| --- | --- | --- |
| 個人使用（建議） | `~/.agents/skills/book-json/` | `/Users/alice/.agents/skills/book-json/` |
| 單一專案 | `<專案根目錄>/.agents/skills/book-json/` | `/Users/alice/Projects/my-study/.agents/skills/book-json/` |

快速找到個人安裝位置：

1. 開啟 **Finder**，按 **Command + Shift + G**，貼上 `~/.agents/skills/`，按 Return。
2. 如果目錄尚未建立，開啟「終端機」，依序執行以下兩行，建立並開啟目錄：

   ```sh
   mkdir -p "$HOME/.agents/skills"
   open "$HOME/.agents/skills"
   ```

3. 將解壓縮專案中的 **整個** `skills/book-json` 資料夾複製到這個 `skills` 目錄內。
4. 確認最終檔案位置為 `~/.agents/skills/book-json/SKILL.md`。需要顯示隱藏資料夾時，在 Finder 按 **Command + Shift + .**。

若採單一專案安裝，請在實際專案根目錄內建立 `.agents/skills`，再放入完整的 `book-json` 資料夾。例如，最終檔案位置為 `/Users/alice/Projects/my-study/.agents/skills/book-json/SKILL.md`。

### 其他工具

- **原生支援 `SKILL.md` 的 AI Agent：**依該工具的文件，將完整的 `skills/book-json` 資料夾放入其指定的 Skill 目錄，再使用該工具的選取或呼叫方式。不同工具的安裝位置與指令可能不同，不能假設都支援 `/book-json` 或 `$book-json`。
- **沒有原生 Skill 安裝入口的 AI 工具：**若工具能讀取檔案，可提供 `SKILL.md`、`assets/`、`references/`、`scripts/` 與詞彙來源資料，請 AI 依照 Skill 規範手動執行。這種方式不會自動註冊 Skill 指令；PDF、照片辨識與檔案輸出仍取決於該工具的能力。若無法執行 Python，必須如實說明未執行自動驗證。

### 共用執行需求

- AI 能讀取提供的檔案並儲存結果。照片與掃描版 PDF 需要視覺辨識或 OCR，文字版 PDF 需要文件讀取工具；本專案不內建 OCR 引擎。
- 自動驗證需要 **Python 3.10+**，驗證程式**不依賴第三方套件**。沒有 Python 時，AI 可以手動檢查，但必須說明未執行自動驗證。
- 專案不需要專用 API 金鑰。模型與工具使用 AI Agent 本身的設定。

## 使用

以下三個範例預設使用 Codex 的 `$book-json`；使用 Claude Code 時，請將第一行改為 `/book-json`；其他工具則依其支援的方式呼叫，或提供 Skill 檔案請 AI 手動執行。請同時提供 **釋義語言和單字／來源檔案**。缺少任何一項時，Skill 會詢問；只寫「中文」時，會確認使用簡體或繁體。

### 直接提供單字

```text
$book-json
釋義語言：繁體中文。
單字：apple, borrow, look after。
難度：A2。
產生 book.json。這些單字沒有 Unit 或 Lesson 分組。
```

### PDF 或照片

附上來源檔案，然後傳送：

```text
$book-json
釋義語言：繁體中文。
使用附件 PDF 第 4–8 頁的詞彙表，以及兩張照片中的詞彙。
保留資料中的 Unit/Lesson 標題，補充雙語例句，產生 book.json。
```

頁碼範圍、難度、課程名稱與輸出目錄皆為選填。Skill 會核對閱讀順序與擷取完整性；看不清楚的詞條需要補充清晰的局部圖片或頁面後，才能交付完整書籍。一般文章沒有明確詞表時，請指定要收集的詞彙範圍。

### 擴充現有書籍

```text
$book-json
釋義語言：繁體中文。
將照片中的詞彙補充至附件中現有的 book.json。
將合併結果儲存為 book.extended.json。
```

保留現有正確內容；同一課程內相同拼寫的詞條合併義項，不同課程分別保留。原書語言與目標語言不一致時，會詢問處理方式。除非使用者要求覆寫，否則寫入新檔案。

## 輸出格式

```json
[
  {
    "word": {
      "wordHead": "apple",
      "wordId": "1",
      "content": {
        "usphone": "",
        "ukphone": "",
        "trans": [
          {
            "tranCn": "蘋果",
            "pos": "n",
            "sentence_example": "I eat an apple after lunch.\n我午餐後吃一顆蘋果。"
          }
        ]
      }
    }
  }
]
```

`tranCn` 是歷史欄位名稱，表示**使用者所選語言的釋義**。請勿改名，也不要新增 `language` 中繼資料。例句欄位在 JSON 解析後必須恰好是兩行；釋義語言為英語時，第二行是同一句話的英文改寫。

**每本書都可以省略 `unit`**。資料中的 Lesson 統一儲存到 `unit`，不新增 `lesson` 欄位。保留來源中的義項與詞性，缺少例句時由 AI 撰寫；音標僅在查證後填入。釋義標點拆分、課程去重等規則，請參閱 [完整格式規範](skills/book-json/references/book_template.md)。

範例：[English](examples/book.en.json)、[繁體中文](examples/book.zh-Hant.json)、[简体中文](examples/book.zh-Hans.json)、[日本語](examples/book.ja.json)、[한국어](examples/book.ko.json)，以及 [可選的 Lesson/Unit 分組](examples/book.lessons.json)。

## 驗證

在專案根目錄執行：

```sh
python skills/book-json/scripts/validate_book.py examples/book.ja.json
python skills/book-json/scripts/validate_book.py /path/to/book.json --json
```

依環境需要，將 `python` 換成 `python3` 等啟動指令。可同時傳入多個檔案路徑。結束代碼 `0` 表示全部通過，`1` 表示驗證失敗。`--json` 會輸出機器可讀的報告。驗證程式僅讀取檔案，不修改內容。

檢查範圍包括嚴格的欄位與型別、必填例句、連續編號、重複詞條及義項、預留文字、音標外圍符號、UTF-8 JSON，以及匯入上限 **100,000 筆紀錄／30 MiB**。[JSON Schema](skills/book-json/assets/book.schema.json) 也可用於編輯器檢查。

結構驗證無法判斷 OCR 是否正確、來源是否完整、是否使用目標語言、翻譯品質，或例句是否符合義項；Skill 要求 AI 另外逐項核對這些內容。

## 專案結構

```text
skills/book-json/
  SKILL.md                         AI 工作流程與觸發條件
  agents/openai.yaml               顯示用中繼資料
  assets/book.template.json        生成範本
  assets/book.schema.json          JSON Schema
  references/book_template.md      完整格式規範
  references/source-extraction.md  PDF／照片讀取流程
  references/extending-books.md    擴充現有書籍的合併規則
  scripts/validate_book.py         使用標準函式庫的唯讀驗證程式
examples/                         原創範例書籍
tests/                            自動化驗證測試
.github/workflows/validate.yml    Linux／Windows CI
```

## 開發與發布

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

開發相依套件僅用於測試及中繼資料／Schema 檢查，執行驗證程式無需安裝這些套件。CI 會執行測試並驗證範例檔案。

發布至 GitHub 時，以**此資料夾作為獨立儲存庫的根目錄**。專案不依賴 Flutter 專案、原始詞庫、本機路徑或外部專案檔案。散布時請保留完整 Skill 資料夾；修改格式時，同步更新規範、Schema、驗證程式、範例及測試，並保持五種語言的 README 一致。

`inputs/`、`outputs/` 已加入忽略清單，供本機使用。上傳的資料由所選的 AI 產品及其工具處理；驗證程式本身不會發送網路請求。請勿將私人來源文件提交至儲存庫。

## 授權條款

[MIT](LICENSE)。專案中的範例為原創內容。授權條款適用於本專案，不涵蓋使用者提供的第三方書籍、照片等資料。
