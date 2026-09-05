import unittest

import contract_v3
import training_data_v3


class FakeTokenizer:
    def __call__(self, text, max_length, padding, truncation, return_offsets_mapping):
        offsets = []
        cursor = 0
        for token in text.split():
            start = text.index(token, cursor)
            end = start + len(token)
            offsets.append([start, end]); cursor = end
        offsets = offsets[:max_length]
        padding_count = max_length - len(offsets)
        return {
            "input_ids": list(range(1, len(offsets) + 1)) + [0] * padding_count,
            "attention_mask": [1] * len(offsets) + [0] * padding_count,
            "offset_mapping": offsets + [[0, 0]] * padding_count,
        }


def v3_row():
    text = "Marco says Anna does not dislike Luca after dinner"
    def span(value):
        start = text.index(value); return [start, start + len(value)]
    return {
        "contractVersion": contract_v3.CONTRACT_VERSION,
        "id": "synthetic:v3", "language": "en", "text": text,
        "mentions": [
            {"mentionId": "m0", "span": span("Marco"), "entityType": "PERSON"},
            {"mentionId": "m1", "span": span("Anna"), "entityType": "PERSON"},
            {"mentionId": "m2", "span": span("Luca"), "entityType": "PERSON"},
        ],
        "claims": [{
            "claimId": "c0", "sourceSpan": [0, len(text)],
            "subjectSpans": [span("Anna")], "objectSpans": [span("Luca")],
            "negationCueSpans": [span("not")],
            "temporalEvidence": [{"temporalId": "t0", "span": span("dinner")}],
            "entityMentionIds": ["m0", "m1", "m2"],
            "labels": {
                "dialogueAct": "ASSERT", "predicate": "preference.like",
                "subjectReferent": "mention:m1", "targetReferent": "mention:m2",
                "ownerReferent": "mention:m1", "perspectiveReferent": "mention:m0",
                "sourceReferent": "mention:m0", "polarity": "POSITIVE",
                "temporalRelation": {"relation": "AFTER", "anchorRef": "temporal:t0"},
                "claimKind": "REPORT",
            },
        }],
    }


class TrainingDataV3Test(unittest.TestCase):
    def test_plural_cue_and_pointer_targets_are_encoded_without_data_io(self):
        examples = training_data_v3.build_v3_examples(
            v3_row(), FakeTokenizer(), 32, {"speaker": "player", "observer": "matrix"}
        )
        self.assertEqual(["boundary", "claim"], [item["kind"] for item in examples])
        claim = examples[1]
        self.assertIn(1, claim["token_labels"]["negation"])
        self.assertEqual(
            claim["role_pointer_values"].index("mention:m0"),
            claim["role_pointer_labels"]["sourceReferent"],
        )
        self.assertEqual(
            claim["temporal_anchor_values"].index("temporal:t0"),
            claim["temporal_anchor_label"],
        )

    def test_v2_row_is_rejected_not_reinterpreted(self):
        row = v3_row(); row["contractVersion"] = "MATRIX_NLU_DATASET_V2"
        with self.assertRaises(ValueError):
            training_data_v3.build_v3_examples(
                row, FakeTokenizer(), 32, {"speaker": "s", "observer": "o"}
            )


if __name__ == "__main__":
    unittest.main()
