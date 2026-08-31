from datetime import datetime
import json
import os

class Helper:
	@classmethod
	def parse_start_date_from(cls, arg) -> str:
		try:
			return datetime.strptime(arg, "%Y-%m-%d").strftime("%Y-%m-%d")
		except ValueError:
			return None

	@classmethod
	def save_workout(cls, filename: str, workout_as_json: dict) -> None:
		os.makedirs("generated", exist_ok=True)
		with open(f"generated/{filename}", "w", encoding="utf-8") as file:
			json.dump(workout_as_json, file, indent=2)
