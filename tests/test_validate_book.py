"""Exercise the public validator contract without translation or OCR services."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "book-json" / "scripts" / "validate_book.py"
SPEC = importlib.util.spec_from_file_location("book_json_validator", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


def sense(definition="苹果", pos="n", example="I eat an apple every morning.\n我每天早晨吃一个苹果。"):
    return {"tranCn": definition, "pos": pos, "sentence_example": example}


def record(head="apple", word_id="1", unit=None, senses=None):
    word = {
        "wordHead": head,
        "wordId": word_id,
        "content": {"usphone": "", "ukphone": "", "trans": senses or [sense()]},
    }
    if unit is not None:
        word["unit"] = unit
    return {"word": word}


class ValidateBookTests(unittest.TestCase):
    def assert_valid(self, book):
        self.assertEqual([], validator.validate_book(book))

    def assert_invalid(self, book):
        errors = validator.validate_book(book)
        self.assertIsInstance(errors, list)
        self.assertTrue(errors)
        self.assertTrue(all(isinstance(error, str) and error for error in errors))

    def test_valid_ungrouped_book(self):
        self.assert_valid([record(), record("pear", "2", senses=[sense("梨")])])

    def test_definitions_are_not_restricted_to_chinese(self):
        cases = [
            ("苹果", "我每天早晨吃一个苹果。"),
            ("蘋果", "我每天早晨吃一個蘋果。"),
            ("リンゴ", "私は毎朝リンゴを一つ食べます。"),
            ("사과", "나는 매일 아침 사과를 하나 먹습니다."),
            ("a round fruit", "Every morning I have an apple to eat."),
            ("manzana", "Como una manzana todas las mañanas."),
        ]
        for definition, translation in cases:
            with self.subTest(definition=definition):
                self.assert_valid([record(senses=[sense(definition, example="I eat an apple every morning.\n" + translation)])])

    def test_explicit_lessons_and_mixed_grouping(self):
        self.assert_valid([
            record("apple", "1", "Unit 1 / Lesson 2"),
            record("apple", "2", "Unit 1 / Lesson 3"),
            record("apple", "3"),
        ])

    def test_empty_unit_is_valid(self):
        self.assert_valid([record(unit="")])

    def test_same_word_same_unit_is_duplicate(self):
        self.assert_invalid([record(unit="Lesson 1"), record(word_id="2", unit="Lesson 1")])

    def test_missing_and_empty_unit_are_same_group(self):
        self.assert_invalid([record(), record(word_id="2", unit="")])

    def test_meaningful_case_is_preserved(self):
        self.assert_valid([record("Polish"), record("polish", "2")])

    def test_phrases_and_accents_are_preserved(self):
        for head in ["look after", "café", "mother-in-law", "colour (color)", "don't"]:
            with self.subTest(head=head):
                self.assert_valid([record(head)])

    def test_nonempty_top_level_array_is_required(self):
        for value in [None, {}, "book", 1, True, []]:
            with self.subTest(value=value):
                self.assert_invalid(value)

    def test_required_keys_at_every_object_level(self):
        paths = [
            ((), "word"),
            (("word",), "wordHead"),
            (("word",), "wordId"),
            (("word",), "content"),
            (("word", "content"), "usphone"),
            (("word", "content"), "ukphone"),
            (("word", "content"), "trans"),
            (("word", "content", "trans", 0), "tranCn"),
            (("word", "content", "trans", 0), "pos"),
            (("word", "content", "trans", 0), "sentence_example"),
        ]
        for path, key in paths:
            with self.subTest(path=path, key=key):
                item = record()
                target = item
                for part in path:
                    target = target[part]
                del target[key]
                self.assert_invalid([item])

    def test_extra_fields_at_every_object_level(self):
        paths = [(), ("word",), ("word", "content"), ("word", "content", "trans", 0)]
        for path in paths:
            with self.subTest(path=path):
                item = record()
                target = item
                for part in path:
                    target = target[part]
                target["language"] = "zh-Hans"
                self.assert_invalid([item])

    def test_separate_lesson_field_is_not_supported(self):
        item = record()
        item["word"]["lesson"] = "Lesson 1"
        self.assert_invalid([item])

    def test_leaf_values_must_be_strings(self):
        paths = [
            ("word", "wordHead"), ("word", "wordId"), ("word", "unit"),
            ("word", "content", "usphone"), ("word", "content", "ukphone"),
            ("word", "content", "trans", 0, "tranCn"),
            ("word", "content", "trans", 0, "pos"),
            ("word", "content", "trans", 0, "sentence_example"),
        ]
        for path in paths:
            for value in [None, 1, True, [], {}]:
                with self.subTest(path=path, value=value):
                    item = record(unit="Lesson 1")
                    target = item
                    for part in path[:-1]:
                        target = target[part]
                    target[path[-1]] = value
                    self.assert_invalid([item])

    def test_invalid_container_types_return_errors(self):
        cases = [None, [], "bad", 1, True]
        for path in [(), ("word",), ("word", "content"), ("word", "content", "trans", 0)]:
            for value in cases:
                with self.subTest(path=path, value=value):
                    if not path:
                        self.assert_invalid([value])
                        continue
                    item = record()
                    target = item
                    for part in path[:-1]:
                        target = target[part]
                    target[path[-1]] = value
                    self.assert_invalid([item])
        for value in [None, {}, "bad", True, []]:
            with self.subTest(trans=value):
                item = record()
                item["word"]["content"]["trans"] = value
                self.assert_invalid([item])

    def test_ids_are_continuous_strings(self):
        for value in [1, "0", "01", "2", "", " 1 ", True]:
            with self.subTest(value=value):
                self.assert_invalid([record(word_id=value)])
        self.assert_invalid([record(), record("pear", "3")])

    def test_headwords_have_trimmed_length_bounds(self):
        for value in ["", " ", " apple", "apple ", "a" * 201]:
            with self.subTest(value=value):
                self.assert_invalid([record(value)])
        self.assert_valid([record("a" * 200)])

    def test_definitions_cannot_be_empty(self):
        for value in ["", " \t", ";；,，"]:
            with self.subTest(value=value):
                self.assert_invalid([record(senses=[sense(value)])])

    def test_expanded_meanings_cannot_repeat_with_same_pos(self):
        for delimiter in [",", "，", ";", "；"]:
            with self.subTest(delimiter=delimiter):
                self.assert_invalid([record(senses=[sense("苹果" + delimiter + "苹果")])])
                self.assert_invalid([record(senses=[sense("苹果" + delimiter + "果实"), sense("果实")])])

    def test_different_pos_preserves_same_gloss(self):
        self.assert_valid([record("plan", senses=[sense("计划", "n"), sense("计划", "v")])])

    def test_unknown_pos_and_non_enum_pos_are_supported(self):
        for pos in ["", "vt", "vi", "n pl", "phr v", "prep phr"]:
            with self.subTest(pos=pos):
                self.assert_valid([record(senses=[sense(pos=pos)])])
        self.assert_invalid([record(senses=[sense(pos="n.")])])

    def test_examples_require_exactly_two_nonempty_lf_lines(self):
        invalid_examples = [
            "", "Just one line.", "English.\n", "\n译文。", "English.\n   ",
            "   \n译文。", "English.\n译文。\nExtra.", "English.\n译文。\n",
            "English.\r\n译文。", "English.\r译文。", "English.\\n译文。",
        ]
        for example in invalid_examples:
            with self.subTest(example=repr(example)):
                self.assert_invalid([record(senses=[sense(example=example)])])

    def test_short_complete_expressions_are_allowed(self):
        self.assert_valid([record("Hello", senses=[sense("你好", "exclam", "Hello!\n你好！")])])

    def test_unknown_phonetics_and_multiple_verified_variants_are_allowed(self):
        item = record()
        self.assert_valid([item])
        item["word"]["content"]["usphone"] = "ˈæpəl"
        item["word"]["content"]["ukphone"] = "ə; eɪ"
        self.assert_valid([item])

    def test_phonetics_cannot_have_outer_slashes_or_brackets(self):
        for field in ["usphone", "ukphone"]:
            for value in ["/ˈæpəl/", "[ˈæpəl]", "ə; /eɪ/", "[ə]; eɪ"]:
                with self.subTest(field=field, value=value):
                    item = record()
                    item["word"]["content"][field] = value
                    self.assert_invalid([item])

    def test_template_placeholders_are_rejected(self):
        paths = [
            ("word", "wordHead"), ("word", "unit"), ("word", "content", "usphone"),
            ("word", "content", "trans", 0, "tranCn"),
            ("word", "content", "trans", 0, "pos"),
            ("word", "content", "trans", 0, "sentence_example"),
        ]
        for path in paths:
            with self.subTest(path=path):
                item = record(unit="Lesson 1")
                target = item
                for part in path[:-1]:
                    target = target[part]
                target[path[-1]] = "{{replace_me}}" if path[-1] != "sentence_example" else "I see an apple.\n{{translation}}"
                self.assert_invalid([item])

    def test_validate_book_does_not_mutate_input(self):
        for data in [[record()], [record(), record(word_id="2")], [{"word": None}]]:
            with self.subTest(data=data):
                before = copy.deepcopy(data)
                validator.validate_book(data)
                self.assertEqual(before, data)

    def test_record_limit_accepts_boundary_and_rejects_overflow(self):
        data = [record("apple"), record("pear", "2"), record("peach", "3")]
        self.assert_valid(data)
        with patch.object(validator, "MAX_RECORDS", 2):
            self.assert_valid(data[:2])
            self.assert_invalid(data)


class ValidateFileTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "自分の本.json"

    def write_json(self, data=None):
        self.path.write_text(json.dumps([record()] if data is None else data, ensure_ascii=False), encoding="utf-8")
        return self.path

    def assert_invalid_path(self, path):
        result = validator.validate_path(path)
        self.assertFalse(result["valid"])
        self.assertTrue(result["errors"])

    def test_valid_path_has_result_contract(self):
        result = validator.validate_path(self.write_json())
        self.assertTrue(result["valid"])
        self.assertEqual([], result["errors"])
        self.assertIsInstance(result["stats"], dict)
        self.assertIn("path", result)

    def test_utf8_bom_is_accepted(self):
        self.path.write_text(json.dumps([record()], ensure_ascii=False), encoding="utf-8-sig")
        self.assertTrue(validator.validate_path(self.path)["valid"])

    def test_invalid_utf8_is_rejected_without_exception(self):
        self.path.write_bytes(b"[\xff]")
        self.assert_invalid_path(self.path)

    def test_malformed_json_is_rejected_without_exception(self):
        for text in ["", "[", "[{},]", "```json\n[]\n```", "[]\n[]", "// comment\n[]"]:
            with self.subTest(text=text):
                self.path.write_text(text, encoding="utf-8")
                self.assert_invalid_path(self.path)

    def test_duplicate_object_keys_cannot_silently_replace_values(self):
        text = json.dumps([record()], ensure_ascii=False)
        text = text.replace('"wordHead": "apple"', '"wordHead": "pear", "wordHead": "apple"')
        self.path.write_text(text, encoding="utf-8")
        self.assert_invalid_path(self.path)

    def test_non_json_numeric_constants_are_rejected(self):
        for constant in ["NaN", "Infinity", "-Infinity", "1e400"]:
            with self.subTest(constant=constant):
                self.path.write_text("[" + constant + "]", encoding="utf-8")
                self.assert_invalid_path(self.path)

    def test_missing_path_and_directory_report_errors(self):
        self.assert_invalid_path(self.path)
        self.assert_invalid_path(Path(self.directory.name))

    def test_file_byte_limit_accepts_boundary_and_rejects_overflow(self):
        self.write_json()
        size = self.path.stat().st_size
        with patch.object(validator, "MAX_FILE_BYTES", size):
            self.assertTrue(validator.validate_path(self.path)["valid"])
        with patch.object(validator, "MAX_FILE_BYTES", size - 1):
            self.assert_invalid_path(self.path)

    def test_cli_validates_multiple_files_read_only(self):
        good = self.write_json()
        bad = good.with_name("invalid.json")
        bad.write_text("[]", encoding="utf-8")
        good_before, bad_before = good.read_bytes(), bad.read_bytes()
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(good), str(bad), "--json"],
            capture_output=True, text=True, encoding="utf-8", cwd=self.directory.name,
        )
        self.assertEqual(1, completed.returncode, completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertFalse(payload["valid"])
        self.assertEqual([True, False], [result["valid"] for result in payload["results"]])
        self.assertEqual(good_before, good.read_bytes())
        self.assertEqual(bad_before, bad.read_bytes())
        self.assertEqual({good.name, bad.name}, {item.name for item in Path(self.directory.name).iterdir()})

    def test_cli_success_from_an_unrelated_directory(self):
        good = self.write_json()
        before = good.read_bytes()
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(good)],
            capture_output=True, text=True, encoding="utf-8", cwd=self.directory.name,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertTrue(completed.stdout.strip())
        self.assertEqual(before, good.read_bytes())


if __name__ == "__main__":
    unittest.main()
