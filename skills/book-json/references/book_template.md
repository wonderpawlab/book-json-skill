# book.json contract

This standalone specification defines the output of [book.template.json](../assets/book.template.json). It retains the original English-vocabulary JSON format and makes the chosen definition language explicit.

## Input and language

The user supplies English vocabulary and a definition language. Vocabulary may come from text, a PDF, scans, or photos. Obtain the language before writing definitions; distinguish Simplified Chinese (`zh-Hans`) from Traditional Chinese (`zh-Hant`). Common requests also include English (`en`), Japanese (`ja`), and Korean (`ko`). These are examples, not a closed language list.

Keep English headwords, English example lines, English POS labels, and IPA notation. Translate definitions and the example's second line into the chosen language. For English definitions, the second line is a natural English paraphrase explaining the same sentence. Do not mix languages within a book or add a `language` field. Tell the user the language outside the JSON so they can select it when importing. A consumer's supported languages may be narrower than the JSON format; the skill does not change an app's language settings or grading rules.

## Exact structure

The top level is a nonempty JSON array. Each item has exactly one field, `word`. UTF-8, two-space indentation, and no BOM are the generation defaults; the validator also accepts UTF-8 BOM. Limits for the originating importer are 1–100,000 records and 30 MiB of UTF-8 data.

| Path | Type | Rule |
| --- | --- | --- |
| `[].word.wordHead` | string | English word or intact phrase; trimmed, 1–200 characters. Preserve meaningful case, accents, hyphens, apostrophes, parentheses, and variants. |
| `[].word.wordId` | string | Exactly `"1"` through `"N"` in final array order. This is a record number, not a database ID. |
| `[].word.unit` | string, optional | Exact source course name or full path. Omit when no grouping exists. Empty string is accepted for compatibility. |
| `[].word.content.usphone` | string | Verified US IPA without outer `/ /` or `[ ]`; otherwise `""`. |
| `[].word.content.ukphone` | string | Verified UK IPA without outer `/ /` or `[ ]`; otherwise `""`. |
| `[].word.content.trans` | array | At least one sense group. |
| `trans[].tranCn` | string | Nonempty definition in the selected language, despite the legacy field name. |
| `trans[].pos` | string | English POS abbreviation without a trailing period; unknown is `""`. |
| `trans[].sentence_example` | string | Exactly two nonempty lines: English example, then its translation in the selected language. |

No other fields or outer wrappers are allowed. All leaf values are strings; no `null`, numeric IDs, comments, trailing commas, code fences, placeholders, or truncated arrays.

Use [book.schema.json](../assets/book.schema.json) for editor/JSON Schema checks. It covers local structure; the Python validator additionally checks sequential IDs, duplicate records, duplicate expanded senses, file size, and placeholders.

## Senses, POS, and examples

Use source-specified senses rather than expanding to every dictionary meaning. When a source only lists a word, infer a common, reliable sense at the user's level. If the ambiguity would materially change the intended entry, ask instead of guessing.

Typical POS labels: `n`, `v`, `adj`, `adv`, `pron`, `prep`, `conj`, `art`, `det`, `num`, `exclam`, `n pl`, `phr v`, `prep phr`. This is not a closed enum. Preserve reliable source distinctions such as `vt`/`vi`; split different POS/senses when they require different examples.

The original importer splits `tranCn` on ASCII/full-width commas and semicolons: `,，;；`. Synonymous glosses that fit one example may be joined with `；`. Avoid these delimiters inside an explanation that must remain a single sense. This matters for English and other languages too: write a concise definition without incidental commas. Parentheses do not protect commas from splitting. Separate genuinely different meanings into separate `trans` objects.

Each example must demonstrate the target word, an ordinary inflection, or the complete phrase with a normal grammatical variation. Match the actual POS and sense: `cold` meaning low temperature and `a cold` meaning an illness need different examples. A generic sentence about spelling or learning the word does not demonstrate its meaning.

Prefer a suitable complete source example. If none exists, write one rather than leaving an empty field. Use natural, concrete sentences suited to the learner, usually 5–15 English words; short greetings and other complete expressions are fine. Translate the whole example faithfully, without labels or numbering. For JSON text, encode the line break as `\n`; after parsing it must be a real newline, not literal backslash-plus-n.

Phonetics may come from explicitly labelled source IPA or a dictionary actually checked during the task. Do not copy a single unlabelled pronunciation into both accents. Leave unverifiable fields empty and mention missing values outside the JSON. For distinct verified pronunciations of the same spelling, combine them with `; ` in the relevant phone field and explain any sense-to-pronunciation ambiguity outside the file.

## Units, order, and duplicates

`unit` is **optional for every book**. Do not invent Unit 1, distribute words into arbitrary courses, or derive “days” from a title. A book may contain both grouped and ungrouped records.

- `Lesson 2` → `"unit": "Lesson 2"`.
- Nested headings → `"unit": "Unit 1 / Lesson 2"`.
- No explicit course → omit `unit`.
- Never introduce a separate `lesson` field.

Preserve source reading order and course names. Compare trimmed spelling exactly and case-sensitively; do not lemmatize words during deduplication. Missing `unit` and `""` are the same ungrouped value.

Within one `(unit, wordHead)` record, merge all senses in first-appearance order, remove exact duplicate `(pos, expanded meaning)` pairs, and choose the best fitting example. Across units, keep separate records even for the same spelling. Assign IDs only after merging. Keep every source word and intended sense accounted for, except documented duplicate merges or verified corrections.

The originating Flutter application shares word spellings internally and saves senses by group, but schedules a word only in its first valid group. Preserving cross-unit records does not itself provide separate per-course mastery.

## Final review

Check structure with the validator. Separately verify source coverage and reading order, optional courses, the selected language/script, POS/meaning alignment, grammar, target-word usage, translated examples, and phonetic provenance.

Final JSON has no book title or definition-language metadata. Supply these in the delivery note or import UI. The template is a scaffold, not a finished book; its placeholders must never appear in a delivered file.
