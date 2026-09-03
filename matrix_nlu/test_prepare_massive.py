import unittest

import prepare_massive


class PrepareMassiveTest(unittest.TestCase):
    def test_annotation_round_trip_and_spans(self):
        text, slots = prepare_massive.parse_annotated(
            "weather in [place_name : New York] [date : tomorrow]")
        self.assertEqual("weather in New York tomorrow", text)
        self.assertEqual("New York", text[slice(*slots[0]["span"])])
        self.assertEqual("tomorrow", text[slice(*slots[1]["span"])])

    def test_selection_is_reproducible(self):
        rows = [{"id": str(i), "utt": str(i)} for i in range(20)]
        self.assertEqual(prepare_massive.select(rows, 5, 7),
                         prepare_massive.select(list(reversed(rows)), 5, 7))


if __name__ == "__main__":
    unittest.main()
