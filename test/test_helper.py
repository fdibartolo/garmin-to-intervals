import unittest
from src.helper import Helper

class TestHelper(unittest.TestCase):
    def test_parse_start_date_returns_date_in_expected_format(self):
        result = Helper.parse_start_date_from("2026-08-22")
        self.assertEqual(result, "2026-08-22")

    def test_parse_start_date_normalizes_zero_padding(self):
        result = Helper.parse_start_date_from("2026-8-2")
        self.assertEqual(result, "2026-08-02")

    def test_parse_start_date_returns_none_for_invalid_calendar_date(self):
        result = Helper.parse_start_date_from("2026-02-30")
        self.assertIsNone(result)

    def test_parse_start_date_returns_none_for_malformed_date(self):
        result = Helper.parse_start_date_from("22-08-2026")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
