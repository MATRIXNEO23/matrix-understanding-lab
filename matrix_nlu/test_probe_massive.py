import json
import unittest

import probe_massive


class MassiveProbeTest(unittest.TestCase):
    def test_inventory_preserves_official_partitions_and_labels(self):
        rows = [
            {"partition": "train", "intent": "alarm_set", "scenario": "alarm",
             "annot_utt": "wake me at [time : five]"},
            {"partition": "test", "intent": "weather_query", "scenario": "weather",
             "annot_utt": "weather in [place_name : Rome]"},
        ]
        result = probe_massive.inventory_jsonl(json.dumps(row) + "\n" for row in rows)
        self.assertEqual({"test": 1, "train": 1}, result["partitions"])
        self.assertEqual(2, result["intentCount"])
        self.assertEqual(["place_name", "time"], result["slotTypesObserved"])


if __name__ == "__main__":
    unittest.main()
