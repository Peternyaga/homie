from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_model import validate_document  # noqa: E402


class ValidateModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(
            (ROOT / "schemas" / "family-home.schema.json").read_text(encoding="utf-8")
        )
        cls.document = json.loads(
            (ROOT / "experiments" / "ordinary-weekday.json").read_text(encoding="utf-8")
        )

    def test_reference_experiment_is_valid(self) -> None:
        self.assertEqual(validate_document(self.document, self.schema), [])

    def test_unknown_affected_participant_is_rejected(self) -> None:
        document = copy.deepcopy(self.document)
        document["episodes"][0]["affected"][0]["participant"] = "unknown_person"

        errors = validate_document(document, self.schema)

        self.assertTrue(any("unknown participant 'unknown_person'" in error for error in errors))

    def test_unexercised_required_coverage_is_rejected(self) -> None:
        document = copy.deepcopy(self.document)
        document["episodes"] = [
            episode
            for episode in document["episodes"]
            if episode["steward"]["mode"] != "escalate"
        ]

        errors = validate_document(document, self.schema)

        self.assertTrue(any("values not exercised" in error and "escalate" in error for error in errors))

    def test_private_information_cannot_include_home_steward(self) -> None:
        document = copy.deepcopy(self.document)
        private_item = next(
            item
            for episode in document["episodes"]
            for item in episode["information"]
            if item["class"] == "private"
        )
        private_item["recipients"].append("homie")

        errors = validate_document(document, self.schema)

        self.assertTrue(any("private information cannot include the home steward" in error for error in errors))

    def test_empty_rights_floor_check_is_rejected(self) -> None:
        document = copy.deepcopy(self.document)
        document["episodes"][0]["authority"]["rights_floor_check"] = ""

        errors = validate_document(document, self.schema)

        self.assertTrue(any("rights_floor_check" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
