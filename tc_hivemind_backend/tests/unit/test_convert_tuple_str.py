import unittest

from tc_hivemind_backend.db.pg_db_utils import convert_tuple_str


class TestConvertTupleStr(unittest.TestCase):
    def test_convert_tuple_str_single_item(self):
        data = ["item1"]
        result = convert_tuple_str(data)
        self.assertEqual(result, "('item1')")

    def test_convert_tuple_str_multiple_items(self):
        data = ["item1", "item2", "item3"]
        result = convert_tuple_str(data)
        self.assertEqual(result, "('item1', 'item2', 'item3')")

    def test_convert_tuple_str_empty_list(self):
        data = []
        result = convert_tuple_str(data)
        self.assertEqual(result, "()")

    def test_convert_tuple_str_numbers(self):
        data = ["1", "2", "3"]
        result = convert_tuple_str(data)
        self.assertEqual(result, "('1', '2', '3')")

    def test_convert_tuple_str_special_characters(self):
        data = ["@", "#", "$"]
        result = convert_tuple_str(data)
        self.assertEqual(result, "('@', '#', '$')")


if __name__ == "__main__":
    unittest.main()
