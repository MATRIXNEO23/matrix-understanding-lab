import pathlib
import tempfile
import unittest

import export_onnx
import export_mixed_head_protected_onnx as mixed_export


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

    def test_mixed_head_protected_policy_covers_matrix_heads(self):
        for output in (
            "token.negation",
            "token.object",
            "token.subject",
            "token.temporal",
            "sequence.dialogueAct",
            "sequence.predicate",
            "sequence.subjectReferent",
            "sequence.targetReferent",
            "sequence.ownerReferent",
            "sequence.perspectiveReferent",
            "sequence.polarity",
            "sequence.temporalRelation",
        ):
            self.assertIn(output, mixed_export.PROTECTED_OUTPUTS)
        self.assertNotIn("massive.intent", mixed_export.PROTECTED_OUTPUTS)
        self.assertNotIn("massive.slot", mixed_export.PROTECTED_OUTPUTS)

    def test_mixed_head_protected_status_is_experimental(self):
        self.assertEqual(
            "EXPERIMENTAL_TEST_CANDIDATE_NOT_PRODUCTION_APPROVED",
            mixed_export.EXPERIMENTAL_STATUS,
        )

    def test_flatten_grouped_nodes_is_stable_and_unique(self):
        grouped = {
            "sequence_heads.predicate": ["nodeA", "nodeB"],
            "sequence_heads.polarity": ["nodeB", "nodeC"],
        }
        self.assertEqual(["nodeA", "nodeB", "nodeC"], mixed_export.flatten_grouped_nodes(grouped))

    def test_protected_nodes_follow_outputs_and_cover_gemm_rewrite(self):
        import onnx
        from onnx import TensorProto, helper

        nodes = [
            helper.make_node("MatMul", ["input", "token_weight"], ["token_linear"],
                             name="/model/boundary/MatMul"),
            helper.make_node("Add", ["token_linear", "token_bias"], ["token.boundary"],
                             name="/model/boundary/Add"),
            helper.make_node("Gemm", ["input", "sequence_weight", "sequence_bias"],
                             ["sequence.predicate"], name="/model/predicate/Gemm"),
            helper.make_node("MatMul", ["input", "encoder_weight"], ["encoded"],
                             name="/model/encoder/layer.0/MatMul"),
            helper.make_node("MatMul", ["/model/encoder/output", "head_weight"],
                             ["unprotected"], name="/model/auxiliary/MatMul"),
        ]
        graph = helper.make_graph(
            nodes,
            "head-protection-test",
            [helper.make_tensor_value_info("input", TensorProto.FLOAT, [1, 2])],
            [helper.make_tensor_value_info("token.boundary", TensorProto.FLOAT, [1, 2]),
             helper.make_tensor_value_info("sequence.predicate", TensorProto.FLOAT, [1, 2])],
        )
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "model.onnx"
            onnx.save(helper.make_model(graph), path)
            grouped = mixed_export.protected_nodes(
                path, outputs=("token.boundary", "sequence.predicate")
            )
            self.assertEqual(["/model/boundary/MatMul"], grouped["token.boundary"])
            self.assertEqual(["/model/predicate/Gemm"], grouped["sequence.predicate"])
            self.assertEqual(
                ["/model/boundary/MatMul", "/model/predicate/Gemm",
                 "/model/predicate/Gemm_MatMul"],
                mixed_export.quantizer_exclusion_names(path, grouped),
            )
            self.assertEqual(
                ["/model/encoder/layer.0/MatMul"],
                mixed_export.encoder_quantizable_nodes(path),
            )


if __name__ == "__main__":
    unittest.main()
