import unittest
import djg
from random import Random
from unittest.mock import patch


class TestNumberGeneration(unittest.TestCase):
    def setUp(self) -> None:
        self.random = Random(666)

    @patch("djg.random")
    def test_number(self, mock_random):
        djg.random.randrange._mock_side_effect = self.random.randrange  # type: ignore
        number = djg._gen_number(minimum=0, maximum=10)
        self.assertEqual(number, 7)

    def test_number_bounds(self):
        number = djg._gen_number(minimum=0, maximum=10)
        self.assertGreaterEqual(number, 0)
        self.assertLessEqual(number, 10)

    def test_multiple_of(self):
        number = djg._gen_number(minimum=10, maximum=100, multiple_of=7)
        self.assertGreaterEqual(number, 10)
        self.assertLessEqual(number, 100)
        self.assertEqual(number % 7, 0)

    def test_number_float(self):
        number = djg._gen_number(minimum=2, maximum=15.6)
        self.assertIsInstance(number, float)
        self.assertGreaterEqual(number, 2)
        self.assertLessEqual(number, 15.6)

    def test_multiple_of_float(self):
        number = djg._gen_number(minimum=10, maximum=100, multiple_of=7.5)
        self.assertIsInstance(number, float)
        self.assertGreaterEqual(number, 10.0)
        self.assertLessEqual(number, 100.0)
        self.assertEqual(number % 7.5, 0)

    @patch("djg.random")
    def test_number_multiple_of(self, mock_random):
        djg.random.randrange._mock_side_effect = self.random.randrange  # type: ignore
        multiple_of = 17
        number = djg._gen_number(minimum=0, maximum=100, multiple_of=multiple_of)
        self.assertEqual(number, 68)
        self.assertEqual(number % multiple_of, 0)


class TestStringGeneration(unittest.TestCase):
    def test_str_bounds(self):
        length = len(djg._gen_str())
        self.assertGreaterEqual(length, 1)
        self.assertLessEqual(length, 10)

    def test_ignore_min_max(self):
        length = len(djg._gen_str(pattern=r"[a-z]{15,20}", min_length=5, max_length=10))
        self.assertGreater(length, 10)


class TestJsonObject(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = {
            "type": "object",
            "properties": {
                "ProductIdentifier": {
                    "type": "object",
                    "properties": {
                        "Name": {"type": "string", "pattern": "[a-zA-Z]{5,10}"},
                        "Uid": {
                            "type": "number",
                            "minimum": 1000,
                            "maximum": 100000,
                        },
                    },
                },
                "ProductQuantity": {"type": "number", "minimum": 0, "maximum": 100},
            },
        }

    def test_const(self):
        self.schema["properties"]["ProductIdentifier"]["properties"]["Name"]["const"] = "test"
        json_obj = djg.gen_from_schema(self.schema)
        self.assertEqual(json_obj["ProductIdentifier"]["Name"], "test")  # type: ignore


class TestArray(unittest.TestCase):
    def test_array_len(self):
        array = djg._gen_array(items={"type": "number"}, min_items=5, max_items=10)
        self.assertGreaterEqual(len(array), 5)
        self.assertLessEqual(len(array), 10)

    def test_prefix_items(self):
        streets = ["Street", "Avenue", "Boulevard"]
        directions = ["NW", "NE", "SW", "SE"]
        prefix_items = [
            {"type": "number"},
            {"type": "string"},
            {"enum": streets},
            {"enum": directions},
        ]
        array = djg._gen_array(prefix_items=prefix_items)
        self.assertEqual(len(array), 4)
        self.assertIn(array[2], streets)
        self.assertIn(array[3], directions)
