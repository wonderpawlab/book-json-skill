# PDF and photo extraction

Use the host's available file-reading, vision, rendering, and OCR tools. These capabilities are supplied by the agent environment, not this repository. Plain word-list generation does not require OCR. Do not claim to have read an image if only its filename or OCR text was available.

## PDFs

For a text PDF, extract the text and check the page layout where columns, tables, or heading relationships affect meaning. For a scanned or mixed PDF, inspect the page images and use OCR if available. Text extraction returning an empty page is not evidence that the page contains no vocabulary.

Respect requested pages or sections. Otherwise select explicit vocabulary lists, unit word lists, and vocabulary appendices. Do not turn ordinary prose or example sentences into exhaustive word lists. If the user instead explicitly asks for vocabulary selected from prose, use that stated scope.

Read multi-column lists in the document's intended order. Align each headword with its own POS, definition, pronunciation, and course heading. Check continued tables across pages before deciding that an entry is complete.

## Photos and screenshots

Inspect orientation, cropped borders, glare, blur, and handwriting. Use visible page numbers or the user's ordering to arrange multiple images. If order or heading ownership changes the result and cannot be resolved, ask.

Check commonly confused characters (such as `l/I/1` and `rn/m`), apostrophes, accents, IPA symbols, and line-break hyphens against the image. Keep true hyphens and intact phrases. Correct only OCR errors that the source resolves.

When one word is unreadable, identify the image/page and location and request a clearer crop or transcription. Preserve verified work as a draft. Do not invent a likely-looking word, silently omit it, or label partial work as the completed book.

## Coverage and provenance

Maintain temporary extraction notes separate from `book.json`: input page/image, source word, course, senses, and unresolved items. Resolve overlapping photos through the same-unit duplicate rule rather than deleting cross-course repetitions.

For long sources, work in manageable page batches and save verified records as temporary working data. Reconcile the complete coverage inventory, merge duplicates, and assign IDs across the whole book at the end. Response length or context limits are not reasons to drop later pages. If the final book would exceed the documented import limits, explain the limit and agree on a split into separate books.

If the host cannot read a needed attachment, say which input is unavailable and request readable source material or pasted text. Do not upload local documents to an external OCR service without the user's authorization.

Source examples, AI-authored examples, and dictionary-sourced phonetics must be described truthfully in the delivery note. Never include image filenames, page notes, confidence scores, or the extraction ledger in the strict book schema.
