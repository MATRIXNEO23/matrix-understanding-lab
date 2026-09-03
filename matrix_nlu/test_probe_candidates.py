import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).with_name("probe_candidates.py")
SPEC = importlib.util.spec_from_file_location("probe_candidates", MODULE_PATH)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


class FakeSibling:
    def __init__(self, name, size):
        self.rfilename = name
        self.size = size


class CandidateProbeTest(unittest.TestCase):
    def test_prefers_single_safetensors_weight_set(self):
        siblings = [
            FakeSibling("model.safetensors", 400),
            FakeSibling("pytorch_model.bin", 500),
            FakeSibling("config.json", 20),
        ]
        self.assertEqual(400, PROBE.weight_bytes(siblings))

    def test_rejects_license_mismatch(self):
        primary = {
            "role": "PRIMARY_PROBE", "repository": "x", "resolvedRevision": "abc",
            "licenseMatchesExpectation": False, "estimatedDynamicInt8WeightBytes": 1,
            "tokenization": {x: [{"unknownCount": 0}] for x in ("it", "en", "es")},
        }
        decision = PROBE.decide([primary])
        self.assertIsNone(decision["selectedForTraining"])
        self.assertTrue(decision["blockingReasons"])

    def test_rejects_unknown_tokens(self):
        primary = {
            "role": "PRIMARY_PROBE", "repository": "x", "resolvedRevision": "abc",
            "licenseMatchesExpectation": True, "estimatedDynamicInt8WeightBytes": 1,
            "tokenization": {x: [{"unknownCount": int(x == "it")}] for x in ("it", "en", "es")},
        }
        self.assertIsNone(PROBE.decide([primary])["selectedForTraining"])

    def test_primary_probe_error_is_preserved_as_blocker(self):
        primary = {
            "id": "p", "role": "PRIMARY_PROBE", "repository": "x",
            "errorType": "ValueError", "error": "broken tokenizer",
        }
        decision = PROBE.decide([primary])
        self.assertIsNone(decision["selectedForTraining"])
        self.assertIn("broken tokenizer", decision["blockingReasons"][0])


if __name__ == "__main__":
    unittest.main()
