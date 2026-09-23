# Extending an existing book

Use this mode only when the user supplies an existing book and asks to add vocabulary to it. Creating a new book for the user's collection does not imply editing other books.

1. Read the supplied book and determine its definition language from the user's statement and actual contents. If it differs from the requested language, clarify whether to translate the existing entries or produce a separate book; do not silently mix languages.
2. Validate the existing structure. If it uses the original JSONL or `content.word` envelope, normalize it to the template before merging, preserving every word, sense, and explicit course. Complete missing per-sense examples as part of the authorized conversion.
3. Keep existing order, definitions, examples, and verified phonetics unless correction or translation is needed for the request. Append new records in source order. New senses of a same-unit existing word are added to that record. Cross-unit occurrences remain separate.
4. When existing and new entries conflict, prefer the user's explicit correction; otherwise use the best supported source and explain material corrections outside JSON. Missing course membership is not permission to move a word into a nearby lesson.
5. Deduplicate by `(unit, wordHead)` and then `(pos, expanded meaning)`, preserve multiple verified pronunciations, and assign continuous IDs after merging.
6. Write the combined result to a new destination, normally `book.json` in a separate output directory. If that path is the source, choose an unused output path unless the user explicitly requested overwrite. Validate the complete combined book and state how many records or senses were added or merged.
