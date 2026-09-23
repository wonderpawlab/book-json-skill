# Book JSON Skill

**README versions / 文档版本**

| Language / 语言 | README |
| --- | --- |
| English / 英语 | [README.md](README.md) |
| 繁體中文 / 繁体中文 | [README.zh-TW.md](README.zh-TW.md) |
| 简体中文 | [README.zh-CN.md](README.zh-CN.md) |
| 日本語 / 日语 | [README.ja.md](README.ja.md) |
| 한국어 / 韩语 | [README.ko.md](README.ko.md) |

Turn English word lists, PDFs, scans, and photos into a personal vocabulary `book.json`. Tell the AI which language to use for definitions; it extracts the intended vocabulary, supplies examples with translations, and checks the result against the included template.

This is an **AI agent skill**, with a standalone Python validator. Generation and image/PDF reading use the agent's capabilities. Running the validator alone does not extract, translate, or generate vocabulary.

## What it produces

- Definitions in the language you request, such as English, Simplified Chinese, Traditional Chinese, Japanese, or Korean.
- An English example and its translation for **every sense group**.
- Optional courses: `Lesson 2` or `Unit 1 / Lesson 2` stays in `word.unit`; books without courses omit that field.
- Continuous string IDs, merged duplicates within the same course, and separate records across courses.
- Empty strings for unverified pronunciations, with missing information reported outside the file.
- A new book, or a combined book when you supply an existing one to extend.

The format is intended for consumers of the included [book contract](skills/book-json/references/book_template.md). It is not a universal vocabulary interchange format. A consuming app may support fewer definition languages than this skill can generate.

## Install

Download and extract the ZIP, or clone this repository, then locate `skills/book-json`. Follow the section for your tool and choose one installation scope. Copy the **whole `book-json` folder**, including its assets, references, and scripts.

The paths below use default local settings. `alice` and `my-study` are examples; substitute your actual username and project root. `%USERPROFILE%` in File Explorer and `~` in Finder resolve to your current home directory. Windows paths refer to native Windows; when running a tool inside WSL, use its Linux home instead. In Finder, `Command + Shift + .` shows hidden folders.

### Claude Code

Copy the complete `book-json` folder into one of the destinations below. [Claude Code skill documentation](https://code.claude.com/docs/en/skills).

#### Windows

| Scope | Destination folder | Full path example |
| --- | --- | --- |
| Personal (recommended) | `%USERPROFILE%\.claude\skills\book-json\` | `C:\Users\alice\.claude\skills\book-json\` |
| One project | `.claude\skills\book-json\` inside the project root | `C:\Projects\my-study\.claude\skills\book-json\` |

Press `Win + E`, then `Ctrl + L`, and paste `%USERPROFILE%` into File Explorer. Create the `.claude` folder and its `skills` subfolder if missing. If they already exist, open `%USERPROFILE%\.claude\skills` directly from the address bar. Copy the repository's `skills\book-json` folder into that `skills` folder.

The installed file should be `%USERPROFILE%\.claude\skills\book-json\SKILL.md`. For a project installation, create `.claude\skills` in your actual project root and copy `book-json` there.

#### macOS

| Scope | Destination folder | Full path example |
| --- | --- | --- |
| Personal (recommended) | `~/.claude/skills/book-json/` | `/Users/alice/.claude/skills/book-json/` |
| One project | `.claude/skills/book-json/` inside the project root | `/Users/alice/Projects/my-study/.claude/skills/book-json/` |

In Finder, press `Command + Shift + G` and enter `~/.claude/skills/`. If the folder does not exist, use Terminal to create and open it:

```sh
mkdir -p "$HOME/.claude/skills"
open "$HOME/.claude/skills"
```

Copy the repository's `skills/book-json` folder into that `skills` folder. Check for `~/.claude/skills/book-json/SKILL.md`. For a project installation, create `.claude/skills` in your actual project root and copy `book-json` there.

**Invoke:** `/book-json` in Claude Code.

### Codex

Copy the complete `book-json` folder into one of the destinations below. [Codex local skill documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

#### Windows

| Scope | Destination folder | Full path example |
| --- | --- | --- |
| Personal (recommended) | `%USERPROFILE%\.agents\skills\book-json\` | `C:\Users\alice\.agents\skills\book-json\` |
| One project | `.agents\skills\book-json\` inside the project root | `C:\Projects\my-study\.agents\skills\book-json\` |

Press `Win + E`, then `Ctrl + L`, and paste `%USERPROFILE%` into File Explorer. Create the `.agents` folder and its `skills` subfolder if missing. If they already exist, open `%USERPROFILE%\.agents\skills` directly from the address bar. Copy the repository's `skills\book-json` folder into that `skills` folder.

The installed file should be `%USERPROFILE%\.agents\skills\book-json\SKILL.md`. For a project installation, create `.agents\skills` in your actual project root and copy `book-json` there.

#### macOS

| Scope | Destination folder | Full path example |
| --- | --- | --- |
| Personal (recommended) | `~/.agents/skills/book-json/` | `/Users/alice/.agents/skills/book-json/` |
| One project | `.agents/skills/book-json/` inside the project root | `/Users/alice/Projects/my-study/.agents/skills/book-json/` |

In Finder, press `Command + Shift + G` and enter `~/.agents/skills/`. If the folder does not exist, use Terminal to create and open it:

```sh
mkdir -p "$HOME/.agents/skills"
open "$HOME/.agents/skills"
```

Copy the repository's `skills/book-json` folder into that `skills` folder. Check for `~/.agents/skills/book-json/SKILL.md`. For a project installation, create `.agents/skills` in your actual project root and copy `book-json` there.

**Invoke:** `$book-json` in Codex CLI/IDE; in a graphical host, select the installed skill.

### Other tools

- **Native `SKILL.md` support:** copy the complete `book-json` folder to the skill directory documented by that tool, then enable or invoke it through that tool's interface. The directory and invocation syntax are tool-specific.
- **No native skill installation:** give a file-capable AI the `SKILL.md` file, its referenced `assets/` and `references/`, and `scripts/`, together with your vocabulary sources. Ask it to follow the skill and generate `book.json`. This is manual use of the instructions; it does not register `/book-json` or `$book-json` as a command.

A manual request can be:

```text
Read skills/book-json/SKILL.md and the resources it references, then follow its workflow.
Definition language: Japanese.
Words: apple, borrow, look after.
Create book.json and report whether automated validation was run.
```

### Confirm installation and requirements

For a native installation, the final structure must be `…/skills/book-json/SKILL.md`, without an extra nested `book-json` folder. Copying only `SKILL.md` leaves out required resources. If the skill is missing from the tool's selector, check the path and reopen the session; for a project installation, open that project.

- The agent must be able to read the supplied files and write output. Photos and scanned PDFs require vision or OCR; text PDFs require document-reading tools. This repository does not bundle an OCR engine.
- Python **3.10+** is needed for automated validation; the validator has **no third-party dependencies**. Without Python execution, the agent can review manually and must say automated validation was not run.
- No project-specific API key is needed. Model access and host tools follow your agent's own setup.

## Use

Invoke `/book-json` in Claude Code, `$book-json` in Codex CLI/IDE, or use the selection/manual workflow described for your tool above. Provide **both the definition language and the words/source files**. The skill asks for either when missing. “Chinese” alone needs a choice of Simplified or Traditional.

The examples below use Codex's `$book-json` prefix. In Claude Code, change the first line to `/book-json`; for other tools, use their invocation method or omit the prefix for manual use.

### Pasted words

```text
$book-json
Definition language: Japanese.
Words: apple, borrow, look after.
Level: A2.
Generate book.json. These words have no unit or lesson grouping.
```

### PDF or photos

Attach the source files, then send:

```text
$book-json
Definition language: Simplified Chinese.
Use the vocabulary lists on pages 4–8 of the attached PDF and both attached photos.
Keep the printed Unit/Lesson headings. Include bilingual examples and create book.json.
```

Page range, level, course names, and output directory are optional. The skill checks reading order and source coverage; unreadable entries need a clearer crop or page before a complete book can be delivered. For ordinary prose without a vocabulary list, specify which words to collect.

### Extend an existing book

```text
$book-json
Definition language: Korean.
Extend the attached existing book.json with the vocabulary in this photo.
Save the combined result as book.extended.json.
```

Existing correct entries are retained. Same-course duplicate spellings are merged without losing senses. Different courses remain separate. The skill asks how to proceed if the existing book uses another language; it writes to a new path unless you request an overwrite.

## Output format

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
            "tranCn": "りんご",
            "pos": "n",
            "sentence_example": "I eat an apple after lunch.\n昼食後にりんごを一つ食べます。"
          }
        ]
      }
    }
  }
]
```

`tranCn` is the historical field name for **any selected definition language**. Do not rename it or add `language` metadata. The example is exactly two lines after JSON parsing. For English definitions, the second line is an English paraphrase of the example.

`unit` is optional in every book. A source Lesson is stored in `unit`, not a separate `lesson` field. Source senses and POS are preserved; missing examples are authored. IPA is included only when verified. See the [complete contract](skills/book-json/references/book_template.md) for punctuation-based sense splitting and course deduplication.

Examples: [English](examples/book.en.json), [繁體中文](examples/book.zh-Hant.json), [简体中文](examples/book.zh-Hans.json), [日本語](examples/book.ja.json), [한국어](examples/book.ko.json), and [optional Lesson/Unit grouping](examples/book.lessons.json).

## Validate

From the repository root:

```sh
python skills/book-json/scripts/validate_book.py examples/book.ja.json
python skills/book-json/scripts/validate_book.py /path/to/book.json --json
```

Use your Python 3 launcher (for example `python3`) if needed. Multiple file paths are accepted. Exit code `0` means every file passed; `1` means validation failed. `--json` produces a machine-readable report. The validator reads files without modifying them.

Checks include strict fields/types, required examples, sequential IDs, duplicate entries/senses, placeholders, pronunciation delimiters, UTF-8 JSON, and the import limits of **100,000 records / 30 MiB**. The [JSON Schema](skills/book-json/assets/book.schema.json) also supports editor checks.

Structural validation cannot prove OCR accuracy, source coverage, the chosen language, translation quality, or whether an example demonstrates the right sense. The skill requires the agent to review those separately.

## Project layout

```text
skills/book-json/
  SKILL.md                         Agent workflow and triggers
  agents/openai.yaml               Display metadata
  assets/book.template.json        Generation scaffold
  assets/book.schema.json          JSON Schema
  references/book_template.md      Complete format contract
  references/source-extraction.md  PDF/photo reading workflow
  references/extending-books.md    Existing-book merge rules
  scripts/validate_book.py         Read-only standard-library validator
examples/                         Original sample books
tests/                            Automated validation tests
.github/workflows/validate.yml    Linux/Windows CI
```

## Development and publishing

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

Development dependencies are only for tests and metadata/schema checks. Runtime validation remains dependency-free. CI runs the tests and validates the sample books.

Use **this directory as the repository root** when publishing to GitHub. It is self-contained: no Flutter project, original vocabulary corpus, local machine paths, or external project files are required. Keep the skill folder intact when distributing it; update the contract, schema, validator, examples, and tests together when changing the format. Keep the five README versions in sync.

`inputs/` and `outputs/` are ignored for local work. Uploaded documents are processed by the chosen AI host and any tools it uses; the validator itself makes no network requests. Do not commit private source documents.

## License

[MIT](LICENSE). The included examples are original samples. This license covers the project, not third-party books, photos, or other materials supplied by users.
