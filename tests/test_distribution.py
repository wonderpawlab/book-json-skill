"""Validate distributable resources; optional packages are development-only."""

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

from tests.test_validate_book import validator

try:
    import jsonschema
except ImportError:
    jsonschema = None

try:
    import yaml
except ImportError:
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "book-json"
EXAMPLES = [
    "book.en.json", "book.zh-Hans.json", "book.zh-Hant.json",
    "book.ja.json", "book.ko.json", "book.lessons.json",
]


class DistributionTests(unittest.TestCase):
    def test_all_shipped_examples_pass_the_validator(self):
        for name in EXAMPLES:
            with self.subTest(example=name):
                path = ROOT / "examples" / name
                self.assertTrue(path.is_file(), str(path))
                result = validator.validate_path(path)
                self.assertTrue(result["valid"], result["errors"])

    def test_scaffold_is_json_but_not_a_deliverable_book(self):
        path = SKILL / "assets" / "book.template.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(validator.validate_book(data))

    def test_skill_local_markdown_links_resolve_inside_package(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
        self.assertTrue(links)
        for target in links:
            if "://" in target or target.startswith("#"):
                continue
            with self.subTest(target=target):
                resolved = (SKILL / target.split("#", 1)[0]).resolve()
                self.assertTrue(resolved.is_relative_to(SKILL.resolve()))
                self.assertTrue(resolved.is_file(), str(resolved))

    @unittest.skipIf(yaml is None, "PyYAML is optional locally; install requirements-dev.txt for metadata checks")
    def test_skill_and_agent_metadata(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        metadata = yaml.safe_load(text.split("---", 2)[1])
        self.assertEqual(SKILL.name, metadata["name"])
        self.assertIsInstance(metadata["description"], str)
        self.assertTrue(metadata["description"].strip())
        agent = yaml.safe_load((SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8"))
        interface = agent["interface"]
        self.assertIsInstance(interface["display_name"], str)
        self.assertGreaterEqual(len(interface["short_description"]), 25)
        self.assertLessEqual(len(interface["short_description"]), 64)
        self.assertIn("$book-json", interface["default_prompt"])


@unittest.skipIf(jsonschema is None, "jsonschema is optional locally; install requirements-dev.txt for schema checks")
class JsonSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((SKILL / "assets" / "book.schema.json").read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(cls.schema)
        cls.checker = jsonschema.Draft202012Validator(cls.schema)

    def test_all_examples_match_the_editor_schema(self):
        for name in EXAMPLES:
            with self.subTest(example=name):
                data = json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))
                self.checker.validate(data)

    def test_schema_rejects_extra_keys_and_numeric_ids(self):
        base = json.loads((ROOT / "examples" / "book.en.json").read_text(encoding="utf-8"))
        base[0]["word"]["wordId"] = 1
        self.assertTrue(list(self.checker.iter_errors(base)))
        base[0]["word"]["wordId"] = "1"
        base[0]["word"]["language"] = "en"
        self.assertTrue(list(self.checker.iter_errors(base)))


if __name__ == "__main__":
    unittest.main()
