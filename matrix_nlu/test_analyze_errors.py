import json
import pathlib
import tempfile
import unittest

from analyze_errors import analyze, classify


class ErrorAnalysisTest(unittest.TestCase):
    def test_taxonomy_distinguishes_critical_families(self):
        self.assertEqual("MODEL_CLAIM_SEGMENTATION", classify({"kind": "CLAIM_COUNT"}))
        self.assertEqual("AUTHORITY_OR_REFERENT_DECODING",
                         classify({"kind": "FIELD", "field": "owner"}))
        self.assertEqual("MODEL_ENTITY_RESOLUTION", classify({"kind": "ENTITY"}))

    def test_report_groups_by_language_without_fixing_frozen_examples(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "errors.jsonl"
            path.write_text(json.dumps({"id": "x", "language": "es", "text": "texto",
                "errors": [{"kind": "SPAN", "field": "objectSpan"}]}) + "\n")
            result = analyze(path)
            self.assertEqual(1, result["failedObservations"])
            self.assertEqual(1, result["families"][0]["byLanguage"]["es"])
            self.assertIn("Do not patch frozen", result["fixPolicy"])


if __name__ == "__main__":
    unittest.main()
