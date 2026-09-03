import unittest

import training_data
import build_dataset
from labels import SEQUENCE_IDS


class TrainingDataTest(unittest.TestCase):
    def test_bio_uses_character_overlap_and_ignores_special_tokens(self):
        offsets = [(0, 0), (0, 3), (4, 8), (9, 13), (0, 0)]
        self.assertEqual([-100, 0, 1, 2, -100], training_data.bio(offsets, [[4, 13]]))

    def test_entity_labels_distinguish_person_and_composite_location(self):
        offsets = [(0, 5), (6, 11), (12, 16)]
        labels = training_data.entity_bio(offsets, [
            {"span": [0, 5], "type": "PERSON"},
            {"span": [6, 16], "type": "LOCATION"},
        ])
        self.assertEqual([1, 3, 4], labels)

    def test_massive_slot_vocabulary_is_stable(self):
        self.assertEqual(["O", "B-date", "I-date", "B-time", "I-time"],
                         training_data.massive_slot_vocab(["date", "time"]))

    def test_every_matrix_and_p05_sequence_label_is_in_training_vocabulary(self):
        rows = build_dataset.build_records()
        rows += build_dataset.load_p05(
            __import__("pathlib").Path(__file__).resolve().parents[1] / "gold" / "p05-gold-v1.json")
        for row in rows:
            for claim in row["claims"]:
                for head, vocabulary in SEQUENCE_IDS.items():
                    self.assertIn(claim["labels"][head], vocabulary, (row["id"], head))


if __name__ == "__main__":
    unittest.main()
