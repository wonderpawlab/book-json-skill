#!/usr/bin/env python3
"""Read-only structural validation for vocabulary books (Python 3.10+).

No external packages are required. This tool cannot check source coverage,
language, pronunciation accuracy, or the meaning and quality of examples.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


MAX_RECORDS = 100_000
MAX_FILE_BYTES = 30 * 1024 * 1024
MEANING_SEPARATOR = re.compile(r"[,，;；]")
PLACEHOLDER = re.compile(r"\{\{[\s\S]*?\}\}")
STAT_NAMES = (
    "records", "distinct_words", "groups", "sense_groups", "expanded_senses",
    "missing_usphone", "missing_ukphone", "missing_pos",
)


def _object(
    value: Any, path: str, required: set[str], optional: set[str], errors: list[str]
) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected an object")
        return False
    for key in sorted(required - value.keys()):
        errors.append(f"{path}.{key}: required field is missing")
    for key in sorted(value.keys() - required - optional, key=str):
        errors.append(f"{path}: unexpected field {key!r}")
    return True


def _string(
    value: Any,
    path: str,
    errors: list[str],
    *,
    nonempty: bool = False,
    trimmed: bool = False,
) -> bool:
    if not isinstance(value, str):
        errors.append(f"{path}: expected a string")
        return False
    if nonempty and not value.strip():
        errors.append(f"{path}: must contain non-whitespace text")
    if trimmed and value != value.strip():
        errors.append(f"{path}: remove leading and trailing whitespace")
    if PLACEHOLDER.search(value):
        errors.append(f"{path}: unresolved template placeholder")
    return True


def _meanings(value: str) -> list[str]:
    return [part.strip() for part in MEANING_SEPARATOR.split(value) if part.strip()]


def _phone(value: Any, path: str, errors: list[str]) -> None:
    if not _string(value, path, errors, trimmed=True) or not value:
        return
    for number, variant in enumerate(value.split(";"), 1):
        variant = variant.strip()
        if not variant:
            errors.append(f"{path}: pronunciation variant {number} is empty")
        elif variant[0] in "/[]" or variant[-1] in "/[]":
            errors.append(
                f"{path}: remove outer slash/bracket notation from pronunciation variant {number}"
            )


def _sense(
    value: Any, path: str, seen: set[tuple[str, str]], errors: list[str]
) -> None:
    if not _object(value, path, {"tranCn", "pos", "sentence_example"}, set(), errors):
        return
    meaning = value.get("tranCn")
    pos = value.get("pos")
    example = value.get("sentence_example")
    meaning_ok = _string(meaning, f"{path}.tranCn", errors, nonempty=True)
    pos_ok = _string(pos, f"{path}.pos", errors, trimmed=True)
    if pos_ok and pos.endswith("."):
        errors.append(f"{path}.pos: omit the trailing period")
    if meaning_ok:
        parts = _meanings(meaning)
        if not parts and meaning.strip():
            errors.append(f"{path}.tranCn: contains no meaning after delimiter expansion")
        if pos_ok:
            for part in parts:
                key = (pos, part)
                if key in seen:
                    errors.append(f"{path}.tranCn: duplicate expanded sense {key!r}")
                seen.add(key)
    if _string(example, f"{path}.sentence_example", errors, nonempty=True):
        if "\\n" in example:
            errors.append(f"{path}.sentence_example: contains literal backslash-n; use a newline")
        if "\r" in example:
            errors.append(f"{path}.sentence_example: use LF rather than CR/CRLF line breaks")
        lines = example.split("\n")
        if len(lines) != 2 or any(not line.strip() for line in lines):
            errors.append(f"{path}.sentence_example: expected exactly two nonempty lines")


def validate_book(data: Any) -> list[str]:
    """Return all detected structural errors without changing ``data``.

    IDs are consecutive string record numbers. Duplicate checks are exact and
    case-sensitive, with missing and empty units representing the same group.
    No target-language, headword-in-example, or dictionary heuristics are used.
    """
    errors: list[str] = []
    if not isinstance(data, list):
        return ["$: expected a nonempty array of word records"]
    if not 1 <= len(data) <= MAX_RECORDS:
        errors.append(f"$: expected 1–{MAX_RECORDS:,} records; found {len(data):,}")

    records: set[tuple[str, str]] = set()
    for index, item in enumerate(data):
        path = f"$[{index}]"
        if not _object(item, path, {"word"}, set(), errors):
            continue
        word = item.get("word")
        path += ".word"
        if not _object(word, path, {"wordHead", "wordId", "content"}, {"unit"}, errors):
            continue

        head = word.get("wordHead")
        head_ok = _string(head, f"{path}.wordHead", errors, nonempty=True, trimmed=True)
        if head_ok and not 1 <= len(head) <= 200:
            errors.append(f"{path}.wordHead: expected 1–200 characters")
        record_id = word.get("wordId")
        if _string(record_id, f"{path}.wordId", errors) and record_id != str(index + 1):
            errors.append(f"{path}.wordId: expected {str(index + 1)!r} in this array position")
        unit = word.get("unit", "")
        unit_ok = _string(unit, f"{path}.unit", errors, trimmed=True)
        if head_ok and unit_ok:
            key = (unit.strip(), head.strip())
            if key in records:
                errors.append(f"{path}: duplicate (unit, wordHead) record {key!r}")
            records.add(key)

        content = word.get("content")
        path += ".content"
        if not _object(content, path, {"usphone", "ukphone", "trans"}, set(), errors):
            continue
        _phone(content.get("usphone"), f"{path}.usphone", errors)
        _phone(content.get("ukphone"), f"{path}.ukphone", errors)
        trans = content.get("trans")
        if not isinstance(trans, list):
            errors.append(f"{path}.trans: expected a nonempty array")
            continue
        if not trans:
            errors.append(f"{path}.trans: expected at least one sense group")
        seen_senses: set[tuple[str, str]] = set()
        for sense_index, sense in enumerate(trans):
            _sense(sense, f"{path}.trans[{sense_index}]", seen_senses, errors)
    return errors


def _stats(data: Any) -> dict[str, int]:
    """Count readable records; counts for invalid books are only partial."""
    result = dict.fromkeys(STAT_NAMES, 0)
    if not isinstance(data, list):
        return result
    result["records"] = len(data)
    heads: set[str] = set()
    groups: set[str] = set()
    for item in data:
        if not isinstance(item, dict) or not isinstance(item.get("word"), dict):
            continue
        word = item["word"]
        if isinstance(word.get("wordHead"), str) and word["wordHead"].strip():
            heads.add(word["wordHead"].strip())
        if isinstance(word.get("unit"), str) and word["unit"].strip():
            groups.add(word["unit"].strip())
        content = word.get("content")
        if not isinstance(content, dict):
            continue
        for field in ("usphone", "ukphone"):
            if content.get(field) == "":
                result[f"missing_{field}"] += 1
        trans = content.get("trans")
        if not isinstance(trans, list):
            continue
        result["sense_groups"] += len(trans)
        for sense in trans:
            if not isinstance(sense, dict):
                continue
            if isinstance(sense.get("tranCn"), str):
                result["expanded_senses"] += len(_meanings(sense["tranCn"]))
            if sense.get("pos") == "":
                result["missing_pos"] += 1
    result["distinct_words"] = len(heads)
    result["groups"] = len(groups)
    return result


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def _reject_constant(value: str) -> Any:
    raise ValueError(f"non-finite JSON number {value!r} is not allowed")


def _finite_float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"non-finite JSON number {value!r} is not allowed")
    return number


def validate_path(path: str | Path) -> dict[str, Any]:
    """Read a UTF-8 file (optional BOM), validate it, and return a report.

    The report has ``path``, ``valid``, ``errors``, and ``stats`` keys. Files are
    never rewritten. Unreadable or unparseable files return zero statistics.
    """
    source = Path(path)
    result: dict[str, Any] = {
        "path": str(source), "valid": False, "errors": [], "stats": _stats(None)
    }
    try:
        # A bounded read also enforces the limit if the file grows while reading.
        with source.open("rb") as stream:
            raw = stream.read(MAX_FILE_BYTES + 1)
        if len(raw) > MAX_FILE_BYTES:
            result["errors"] = [f"$: file exceeds the {MAX_FILE_BYTES:,}-byte limit (30 MiB)"]
            return result
        data = json.loads(
            raw.decode("utf-8-sig"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
            parse_float=_finite_float,
        )
    except json.JSONDecodeError as error:
        result["errors"] = [f"$: invalid JSON at line {error.lineno}, column {error.colno}: {error.msg}"]
        return result
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        result["errors"] = [f"$: cannot read valid UTF-8 JSON: {error}"]
        return result
    result["errors"] = validate_book(data)
    result["stats"] = _stats(data)
    result["valid"] = not result["errors"]
    return result


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(1, f"{self.prog}: error: {message}\n")


def main(argv: list[str] | None = None) -> int:
    # Piped output on Windows otherwise follows the local code page. Keep both
    # reports and multilingual paths usable by UTF-8 consumers on every host.
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = _ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", metavar="BOOK", help="book JSON file(s) to validate")
    parser.add_argument("--json", action="store_true", help="print one machine-readable JSON report")
    args = parser.parse_args(argv)
    results = [validate_path(path) for path in args.paths]
    valid = all(result["valid"] for result in results)
    if args.json:
        print(json.dumps({"valid": valid, "results": results}, ensure_ascii=False, indent=2))
    else:
        for result in results:
            status = "VALID" if result["valid"] else "INVALID"
            print(f"{status}: {result['path']}")
            if result["valid"]:
                stats = result["stats"]
                print(
                    f"  {stats['records']} records; {stats['distinct_words']} distinct words; "
                    f"{stats['groups']} named groups; {stats['sense_groups']} sense groups; "
                    f"{stats['expanded_senses']} expanded senses"
                )
                print(
                    f"  Missing: US IPA {stats['missing_usphone']}; "
                    f"UK IPA {stats['missing_ukphone']}; POS {stats['missing_pos']}"
                )
            for error in result["errors"]:
                print(f"  {error}")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
