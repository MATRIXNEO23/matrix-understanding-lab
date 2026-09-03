import unittest

import export_onnx


class OnnxExportContractTest(unittest.TestCase):
    def test_output_contract_is_stable_and_complete(self):
        expected = (len(export_onnx.TOKEN_HEADS) + len(export_onnx.SEQUENCE_HEADS) + 2)
        self.assertEqual(expected, len(export_onnx.OUTPUT_NAMES))
        self.assertEqual(len(set(export_onnx.OUTPUT_NAMES)), len(export_onnx.OUTPUT_NAMES))
        self.assertIn("token.boundary", export_onnx.OUTPUT_NAMES)
        self.assertIn("sequence.ownerReferent", export_onnx.OUTPUT_NAMES)
        self.assertIn("massive.slot", export_onnx.OUTPUT_NAMES)

    def test_percentile_is_deterministic(self):
        self.assertEqual(5, export_onnx.percentile([5, 1, 4, 2, 3], .95))
        self.assertEqual(1, export_onnx.percentile([5, 1, 4, 2, 3], 0))


if __name__ == "__main__":
    unittest.main()
