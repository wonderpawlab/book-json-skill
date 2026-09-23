# Book JSON Skill

**README 语言版本**

| 语言 | 完整文档 |
| --- | --- |
| 英语 / English | [README.md](README.md) |
| 繁体中文 / 繁體中文 | [README.zh-TW.md](README.zh-TW.md) |
| 简体中文 | [README.zh-CN.md](README.zh-CN.md) |
| 日语 / 日本語 | [README.ja.md](README.ja.md) |
| 韩语 / 한국어 | [README.ko.md](README.ko.md) |

把英语词表、PDF、扫描件或照片制作成个人词汇书 `book.json`。用户指定释义语言，AI 提取目标词汇、补充例句与译文，并按项目内的模板检查结果。

这是一个 **AI Agent Skill**，附带独立的 Python 校验工具。生成内容、读取 PDF 和识别图片由使用 Skill 的 AI 完成；单独运行校验脚本不会提取、翻译或生成词汇。

## 可以生成什么

- 使用指定语言的释义，例如英语、简体中文、繁体中文、日语或韩语。
- **每个义项组**都有英文例句和对应语言的译文。
- 可选的课程结构：`Lesson 2`、`Unit 1 / Lesson 2` 保存在 `word.unit`；没有课程的书省略该字段。
- 连续的字符串编号；同一课程内合并重复词条，不同课程保留独立记录。
- 无法核实的音标使用空字符串，并在文件外说明缺失信息。
- 创建新书，或向用户提供的现有书籍补充词汇，输出合并结果。

生成结果面向支持本项目 [书籍格式规范](skills/book-json/references/book_template.md) 的应用，不是所有词汇软件通用的格式。导入应用支持的释义语言可能少于本 Skill 可以生成的语言。

## 安装

下载 ZIP 并解压，或使用 Git 克隆本仓库，然后找到 `skills/book-json`。按你使用的工具选择下面的说明，再选择个人或项目安装。复制 **整个 `book-json` 文件夹**，保留其中的模板、参考说明和脚本。

以下是本地默认目录。`alice`、`my-study` 是示例，请替换为实际用户名和项目根目录；资源管理器中的 `%USERPROFILE%`、Finder 中的 `~` 会自动指向当前用户目录。Windows 路径适用于原生 Windows；如果在 WSL 中运行工具，应使用其 Linux 用户目录。在 Finder 中可按 `Command + Shift + .` 显示隐藏文件夹。

### Claude Code

将完整的 `book-json` 文件夹复制到下列一个位置。目录依据：[Claude Code 官方 Skill 文档](https://code.claude.com/docs/en/skills)。

#### Windows

| 使用范围 | 目标文件夹 | 完整路径示例 |
| --- | --- | --- |
| 个人使用（推荐） | `%USERPROFILE%\.claude\skills\book-json\` | `C:\Users\alice\.claude\skills\book-json\` |
| 单个项目 | 项目根目录下的 `.claude\skills\book-json\` | `C:\Projects\my-study\.claude\skills\book-json\` |

按 `Win + E` 打开资源管理器，再按 `Ctrl + L`，在地址栏粘贴 `%USERPROFILE%`。在其中创建缺少的 `.claude` 文件夹及其下的 `skills` 文件夹。如果已经存在，直接在地址栏打开 `%USERPROFILE%\.claude\skills`。将本仓库的 `skills\book-json` 整个文件夹复制到这个 `skills` 目录。

最终应能找到 `%USERPROFILE%\.claude\skills\book-json\SKILL.md`。如果只用于单个项目，在实际项目根目录创建 `.claude\skills`，再把 `book-json` 复制进去。

#### macOS

| 使用范围 | 目标文件夹 | 完整路径示例 |
| --- | --- | --- |
| 个人使用（推荐） | `~/.claude/skills/book-json/` | `/Users/alice/.claude/skills/book-json/` |
| 单个项目 | 项目根目录下的 `.claude/skills/book-json/` | `/Users/alice/Projects/my-study/.claude/skills/book-json/` |

打开 Finder（访达），按 `Command + Shift + G`，输入 `~/.claude/skills/`。如果目录不存在，在“终端”中执行以下两行来创建并打开：

```sh
mkdir -p "$HOME/.claude/skills"
open "$HOME/.claude/skills"
```

将本仓库的 `skills/book-json` 整个文件夹复制到这个 `skills` 目录，并确认 `~/.claude/skills/book-json/SKILL.md` 存在。单个项目安装时，在实际项目根目录创建 `.claude/skills`，再把 `book-json` 复制进去。

**调用方式：**在 Claude Code 中输入 `/book-json`。

### Codex

将完整的 `book-json` 文件夹复制到下列一个位置。目录依据：[Codex 官方本地 Skill 文档](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)。

#### Windows

| 使用范围 | 目标文件夹 | 完整路径示例 |
| --- | --- | --- |
| 个人使用（推荐） | `%USERPROFILE%\.agents\skills\book-json\` | `C:\Users\alice\.agents\skills\book-json\` |
| 单个项目 | 项目根目录下的 `.agents\skills\book-json\` | `C:\Projects\my-study\.agents\skills\book-json\` |

按 `Win + E` 打开资源管理器，再按 `Ctrl + L`，在地址栏粘贴 `%USERPROFILE%`。在其中创建缺少的 `.agents` 文件夹及其下的 `skills` 文件夹。如果已经存在，直接在地址栏打开 `%USERPROFILE%\.agents\skills`。将本仓库的 `skills\book-json` 整个文件夹复制到这个 `skills` 目录。

最终应能找到 `%USERPROFILE%\.agents\skills\book-json\SKILL.md`。如果只用于单个项目，在实际项目根目录创建 `.agents\skills`，再把 `book-json` 复制进去。

#### macOS

| 使用范围 | 目标文件夹 | 完整路径示例 |
| --- | --- | --- |
| 个人使用（推荐） | `~/.agents/skills/book-json/` | `/Users/alice/.agents/skills/book-json/` |
| 单个项目 | 项目根目录下的 `.agents/skills/book-json/` | `/Users/alice/Projects/my-study/.agents/skills/book-json/` |

打开 Finder（访达），按 `Command + Shift + G`，输入 `~/.agents/skills/`。如果目录不存在，在“终端”中执行以下两行来创建并打开：

```sh
mkdir -p "$HOME/.agents/skills"
open "$HOME/.agents/skills"
```

将本仓库的 `skills/book-json` 整个文件夹复制到这个 `skills` 目录，并确认 `~/.agents/skills/book-json/SKILL.md` 存在。单个项目安装时，在实际项目根目录创建 `.agents/skills`，再把 `book-json` 复制进去。

**调用方式：**在 Codex CLI/IDE 中输入 `$book-json`；图形界面中也可以选择已安装的 Skill。

### 其他工具

- **原生支持 `SKILL.md`：**按该工具文档，将整个 `book-json` 文件夹复制到它规定的 Skill 目录，再通过它自己的界面启用或调用。不同工具的目录和调用语法可能不同。
- **没有原生 Skill 安装入口：**向支持读取文件的 AI 提供 `SKILL.md`、其中引用的 `assets/`、`references/` 和 `scripts/`，以及你的词汇资料，要求它按 Skill 生成 `book.json`。这属于手动使用指令，不会注册 `/book-json` 或 `$book-json` 命令。

手动使用时可以这样提问：

```text
请读取 skills/book-json/SKILL.md 及其引用的资源，按其中的流程执行。
释义语言：日语。
单词：apple, borrow, look after。
生成 book.json，并说明是否执行了自动校验。
```

### 确认安装与运行条件

原生安装后的最终结构必须是 `…/skills/book-json/SKILL.md`，避免多嵌套一层 `book-json`。不要只复制 `SKILL.md`，否则会缺少配套资源。如果工具的 Skill 列表中没有出现，检查路径后重新打开会话；项目安装时应打开对应项目。

- AI 能读取提供的文件并保存结果。照片和扫描版 PDF 需要视觉识别或 OCR，文字版 PDF 需要文档读取工具；本项目不内置 OCR 引擎。
- 自动校验需要 **Python 3.10+**，校验器**不依赖第三方库**。无法执行 Python 时，AI 可以人工检查，但必须说明未执行自动校验。
- 项目不需要专用 API Key。模型和工具使用 AI Agent 本身的配置。

## 使用

Claude Code 使用 `/book-json`，Codex CLI/IDE 使用 `$book-json`，其他工具按上面的原生安装或手动使用方式执行。需要同时提供 **释义语言和单词／来源文件**。缺少任何一项时，Skill 会询问；只写“中文”时会确认简体或繁体。

下面的示例使用 Codex 的 `$book-json` 前缀。在 Claude Code 中把第一行改为 `/book-json`；其他工具使用其自身的调用方式，手动使用时省略该前缀。

### 直接提供单词

```text
$book-json
释义语言：日语。
单词：apple, borrow, look after。
难度：A2。
生成 book.json。这些单词没有 Unit 或 Lesson 分组。
```

### PDF 或照片

上传来源文件，然后发送：

```text
$book-json
释义语言：简体中文。
使用附件 PDF 第 4–8 页的词汇表，以及两张照片中的词汇。
保留资料中的 Unit/Lesson 标题，补充双语例句，生成 book.json。
```

页码范围、难度、课程名称和输出目录均为可选项。Skill 会核对阅读顺序和提取完整性；看不清的词条需要补充清晰截图或页面后，才能交付完整书籍。普通文章没有明确词表时，请指定需要收集的词汇范围。

### 扩充已有书籍

```text
$book-json
释义语言：韩语。
把照片里的词汇补充到附件中已有的 book.json。
将合并结果保存为 book.extended.json。
```

保留现有正确内容；同一课程内的相同拼写合并义项，不同课程分别保留。原书语言与目标语言不一致时会询问处理方式。除非用户要求覆盖，否则写入新文件。

## 输出格式

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
            "tranCn": "苹果",
            "pos": "n",
            "sentence_example": "I eat an apple after lunch.\n我午饭后吃一个苹果。"
          }
        ]
      }
    }
  }
]
```

`tranCn` 是历史字段名，表示**用户所选语言的释义**。不要改名，也不要增加 `language` 元数据。例句字段在 JSON 解析后必须恰好是两行；释义语言为英语时，第二行是同一句话的英文改写。

**每本书都可以没有 `unit`**。资料中的 Lesson 统一保存到 `unit`，不增加 `lesson` 字段。保留来源中的义项和词性，缺少例句时由 AI 编写；音标只有核实后才填写。释义标点拆分、课程去重等规则见 [完整格式规范](skills/book-json/references/book_template.md)。

示例：[English](examples/book.en.json)、[繁體中文](examples/book.zh-Hant.json)、[简体中文](examples/book.zh-Hans.json)、[日本語](examples/book.ja.json)、[한국어](examples/book.ko.json)，以及 [可选 Lesson/Unit 分组](examples/book.lessons.json)。

## 校验

在项目根目录运行：

```sh
python skills/book-json/scripts/validate_book.py examples/book.ja.json
python skills/book-json/scripts/validate_book.py /path/to/book.json --json
```

按环境需要将 `python` 换成 `python3` 等启动命令。支持同时传入多个文件路径。退出码 `0` 表示全部通过，`1` 表示校验失败。`--json` 输出机器可读报告。校验器只读文件，不修改内容。

检查范围包括严格字段和类型、必填例句、连续编号、重复词条及义项、占位符、音标外围符号、UTF-8 JSON，以及导入上限 **100,000 条记录／30 MiB**。[JSON Schema](skills/book-json/assets/book.schema.json) 可用于编辑器检查。

结构校验无法判断 OCR 是否正确、来源是否完整、是否使用目标语言、翻译质量或例句是否符合义项；Skill 要求 AI 另外逐项核对这些内容。

## 项目结构

```text
skills/book-json/
  SKILL.md                         AI 工作流程与触发条件
  agents/openai.yaml               展示元数据
  assets/book.template.json        生成模板
  assets/book.schema.json          JSON Schema
  references/book_template.md      完整格式规范
  references/source-extraction.md  PDF／照片读取流程
  references/extending-books.md    扩充现有书籍的合并规则
  scripts/validate_book.py         基于标准库的只读校验器
examples/                         原创示例书籍
tests/                            自动化校验测试
.github/workflows/validate.yml    Linux／Windows CI
```

## 开发与发布

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

开发依赖仅用于测试及元数据／Schema 检查，运行校验器无需安装这些依赖。CI 会运行测试并校验示例文件。

发布 GitHub 时，以**当前文件夹作为独立仓库根目录**。项目不依赖 Flutter 工程、原始词库、本机路径或外部项目文件。分发时保留完整 Skill 文件夹；修改格式时同步更新规范、Schema、校验器、示例和测试，并保持五种语言的 README 一致。

`inputs/`、`outputs/` 已加入忽略列表，供本地使用。上传资料由选用的 AI 产品及其工具处理；校验器本身不发送网络请求。不要把私人来源文件提交到仓库。

## 许可证

[MIT](LICENSE)。项目中的示例为原创样例。许可证适用于本项目，不涵盖用户提供的第三方书籍、照片等资料。
