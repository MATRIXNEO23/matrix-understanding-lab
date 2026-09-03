import unittest

from train import stage_complete


class TrainResumePolicyTest(unittest.TestCase):
    def test_completed_epoch_range_is_not_replayed(self):
        checkpoint = {"stage": "matrix", "nextEpoch": 4, "epochsWithoutImprovement": 0}
        self.assertTrue(stage_complete(checkpoint, "matrix", 4, 2))
        self.assertFalse(stage_complete(checkpoint, "massive-aux", 1, 2))

    def test_early_stopped_stage_is_complete(self):
        checkpoint = {"stage": "matrix", "nextEpoch": 3, "epochsWithoutImprovement": 2}
        self.assertTrue(stage_complete(checkpoint, "matrix", 5, 2))

    def test_incomplete_stage_remains_resumable(self):
        checkpoint = {"stage": "matrix", "nextEpoch": 2, "epochsWithoutImprovement": 1}
        self.assertFalse(stage_complete(checkpoint, "matrix", 4, 2))


if __name__ == "__main__":
    unittest.main()
