import requests
import time
from src.constants import GREEN, RED, RESET, YELLOW

class IntervalsClient:
    """Intervals.icu interface"""

    def __init__(self, athlete_id, username, password):
        self.url = f"https://intervals.icu/api/v1/athlete/{athlete_id}/activities"
        self.username = username
        self.password = password

    def upload_activity_files(self, file_names):
        """ Uploads given activity files to intervals site """

        # files = {'file': (f, open(f, 'rb'), 'multipart/form-data') for f in file_names}
        try:
            for f in file_names:
                files = {'file': (f, open(f, 'rb'), 'multipart/form-data')}
                print(f"{YELLOW} ➜ Uploading {f} to intervals.icu...{RESET}")

                response = requests.post(self.url, auth=(self.username, self.password), files=files)
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
                print(f"{GREEN} ✓ Uploaded {f} to intervals.icu successfully!{RESET}")
                time.sleep(2)  # To avoid hitting rate limits
            result = True
        except requests.exceptions.RequestException as e:
            print(f"{RED} ✗ An error occurred: {e} - {response.text}{RESET}")
            result = False
        finally:
            for f in files.values():
                f[1].close()
        return result