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

	@classmethod
	def strip_markdown(cls, text: str) -> str:
		response_text = text.strip()
		if response_text.startswith("```"):
			response_text = response_text.split("\n", 1)[1]
			response_text = response_text.rsplit("\n```", 1)[0].strip()
		return response_text
