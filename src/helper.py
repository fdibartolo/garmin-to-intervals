from datetime import datetime

class Helper:
	@classmethod
	def parse_start_date_from(cls, arg) -> str:
		try:
			return datetime.strptime(arg, "%Y-%m-%d").strftime("%Y-%m-%d")
		except ValueError:
			return None
