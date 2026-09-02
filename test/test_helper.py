import unittest
import json
import os
import tempfile
import shutil
from src.helper import Helper

class TestHelper(unittest.TestCase):
    def setUp(self):
        # temp directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        # temp directory cleanup
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    # ********************* parse_start_date_from tests *********************************
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

    # ********************* save_workout tests ******************************************
    def test_save_workout_creates_generated_directory(self):
        self.assertFalse(os.path.exists("generated"))
        Helper.save_workout("test.json", {"name": "Test Workout"})
        self.assertTrue(os.path.exists("generated"))

    def test_save_workout_writes_valid_json_file(self):
        workout_data = {"name": "Test Workout", "duration": 60, "intensity": "high"}
        Helper.save_workout("test_workout.json", workout_data)
        
        self.assertTrue(os.path.exists("generated/test_workout.json"))
        with open("generated/test_workout.json", "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        self.assertEqual(loaded_data, workout_data)

    def test_save_workout_with_empty_dict(self):
        Helper.save_workout("empty.json", {})
        
        with open("generated/empty.json", "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        self.assertEqual(loaded_data, {})

    def test_save_workout_with_nested_data(self):
        workout_data = {
            "name": "Complex Workout",
            "exercises": [
                {"name": "Running", "distance": 5.2},
                {"name": "Cycling", "distance": 15.3}
            ],
            "metadata": {
                "date": "2026-08-22",
                "location": "Park"
            }
        }
        Helper.save_workout("complex.json", workout_data)
        
        with open("generated/complex.json", "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        self.assertEqual(loaded_data, workout_data)

    def test_save_workout_overwrites_existing_file(self):
        first_data = {"name": "First"}
        second_data = {"name": "Second"}
        
        Helper.save_workout("overwrite.json", first_data)
        Helper.save_workout("overwrite.json", second_data)
        
        with open("generated/overwrite.json", "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        self.assertEqual(loaded_data, second_data)

    def test_save_workout_uses_utf8_encoding(self):
        workout_data = {"name": "Workout with émojis 🏃"}
        Helper.save_workout("unicode.json", workout_data)
        
        with open("generated/unicode.json", "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        self.assertEqual(loaded_data, workout_data)

if __name__ == "__main__":
    unittest.main()
