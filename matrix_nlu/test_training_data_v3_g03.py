"""Focused G03 regression tests; synthetic inputs only, no models or datasets."""
import copy
import unittest

from contract_v3 import FIELD_STATUSES, ROLE_HEADS
from training_data_v3 import IGNORE, build_v3_examples, role_supervision
from test_training_data_v3 import FakeTokenizer, v3_row


class G03TargetsTest(unittest.TestCase):
    def setUp(self):
        self.row = v3_row()
        self.claim = self.row['claims'][0]
        self.values = ['ctx:speaker', 'ctx:observer', 'mention:m0', 'mention:m1', 'mention:m2', 'NONE', 'UNKNOWN']

    def ambiguous(self, head='targetReferent'):
        self.claim['labels'][head] = 'UNKNOWN'
        self.claim.setdefault('fieldStatusByField', {})[head] = 'AMBIGUOUS'
        self.claim.setdefault('alternativesByField', {})[head] = [
            {'value': 'mention:m2', 'rank': 1}, {'value': 'mention:m0', 'rank': 2}]

    def test_known_none_unknown_and_ambiguous_are_distinct(self):
        self.ambiguous()
        self.claim['labels']['ownerReferent'] = 'NONE'
        self.claim['labels']['sourceReferent'] = 'UNKNOWN'
        out = role_supervision(self.claim, self.values, 16)
        decoded = {h: FIELD_STATUSES[i] for h, i in out['role_status_labels'].items()}
        self.assertEqual({'subjectReferent': 'RESOLVED', 'targetReferent': 'AMBIGUOUS',
                          'ownerReferent': 'NOT_APPLICABLE', 'perspectiveReferent': 'RESOLVED',
                          'sourceReferent': 'UNKNOWN'}, decoded)

    def test_ordered_alternatives_encode_candidate_ids_without_selecting_one(self):
        self.ambiguous()
        before = copy.deepcopy(self.row)
        examples = build_v3_examples(self.row, FakeTokenizer(), 32, {'speaker': 's', 'observer': 'o'})
        result = examples[1]
        values = result['role_pointer_values']
        self.assertEqual('UNKNOWN', values[result['role_pointer_labels']['targetReferent']])
        self.assertEqual([values.index('mention:m2'), values.index('mention:m0')] + [IGNORE] * 14,
                         result['role_alternative_pointer_labels']['targetReferent'])
        self.assertEqual([1, 1] + [0] * 14, result['role_alternative_mask']['targetReferent'])
        self.assertEqual(before, self.row)

    def test_annotation_rank_not_candidate_position_controls_order(self):
        self.ambiguous()
        first = role_supervision(self.claim, self.values, 16)
        reversed_values = list(reversed(self.values))
        second = role_supervision(self.claim, reversed_values, 16)
        for out, values in [(first, self.values), (second, reversed_values)]:
            self.assertEqual(['mention:m2', 'mention:m0'],
                             [values[i] for i in out['role_alternative_pointer_labels']['targetReferent'][:2]])

    def test_each_role_is_encoded_independently(self):
        for head in ROLE_HEADS:
            with self.subTest(head=head):
                self.claim = copy.deepcopy(v3_row()['claims'][0])
                self.ambiguous(head)
                out = role_supervision(self.claim, self.values, 16)
                self.assertEqual(1, sum(FIELD_STATUSES[i] == 'AMBIGUOUS' for i in out['role_status_labels'].values()))
                self.assertEqual(2, sum(out['role_alternative_mask'][head]))

    def test_boundary_and_zero_claim_have_no_role_supervision(self):
        self.row['claims'] = []
        examples = build_v3_examples(self.row, FakeTokenizer(), 32, {})
        self.assertEqual(1, len(examples))
        for head in ROLE_HEADS:
            self.assertEqual(IGNORE, examples[0]['role_status_labels'][head])
            self.assertEqual([IGNORE] * 16, examples[0]['role_alternative_pointer_labels'][head])
            self.assertEqual([0] * 16, examples[0]['role_alternative_mask'][head])

    def test_invalid_status_pointer_combinations_fail_closed(self):
        for value, status in [('NONE', 'RESOLVED'), ('UNKNOWN', 'RESOLVED'),
                              ('mention:m0', 'UNKNOWN'), ('mention:m0', 'AMBIGUOUS'),
                              ('UNKNOWN', 'NOT_APPLICABLE'), ('mention:m0', 'KNOWN')]:
            with self.subTest(value=value, status=status):
                self.claim['labels']['targetReferent'] = value
                self.claim['fieldStatusByField'] = {'targetReferent': status}
                with self.assertRaises(ValueError):
                    role_supervision(self.claim, self.values, 16)

    def test_invalid_or_lost_alternatives_fail_closed(self):
        cases = [[], [{'value': 'mention:m0', 'rank': 1}],
                 [{'value': 'mention:m0', 'rank': 1}, {'value': 'mention:m0', 'rank': 2}],
                 [{'value': 'mention:m0', 'rank': 2}, {'value': 'mention:m2', 'rank': 1}],
                 [{'value': 'mention:m0', 'rank': True}, {'value': 'mention:m2', 'rank': 2}]]
        for value in ['NONE', 'UNKNOWN', 'entity:lost']:
            cases.append([{'value': 'mention:m0', 'rank': 1}, {'value': value, 'rank': 2}])
        for items in cases:
            with self.subTest(items=items):
                self.ambiguous()
                self.claim['alternativesByField']['targetReferent'] = items
                with self.assertRaises(ValueError):
                    role_supervision(self.claim, self.values, 16)

    def test_missing_explicit_status_with_alternatives_is_rejected(self):
        self.ambiguous()
        del self.claim['fieldStatusByField']
        with self.assertRaises(ValueError):
            role_supervision(self.claim, self.values, 16)

    def test_bounded_overflow_cannot_silently_drop_alternative(self):
        self.row['mentions'] = []
        self.claim['labels'] = {**self.claim['labels'], **{h: 'ctx:speaker' for h in ROLE_HEADS}}
        self.ambiguous()
        self.claim['alternativesByField']['targetReferent'] = [
            {'value': 'entity:a', 'rank': 1}, {'value': 'entity:c', 'rank': 2}]
        context = {'contextEntities': [{'entityRef': x} for x in ['a', 'b', 'c']]}
        with self.assertRaisesRegex(ValueError, 'not an available referent'):
            build_v3_examples(self.row, FakeTokenizer(), 32, context, max_referent_candidates=4)


if __name__ == '__main__':
    unittest.main()
