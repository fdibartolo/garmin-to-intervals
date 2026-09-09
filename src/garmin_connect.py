from garminconnect import Garmin
from garminconnect.workout import BaseWorkout

DEFAULT_ACTIVITY_TYPES = (
    "cycling",
    "indoor_cycling",
    "running",
    "lap_swimming",
    "treadmill_running",
    "open_water_swimming",
)

class GarminConnect:
    """Garmin Connect interface"""

    def __init__(self, username, password):
        self.client = Garmin(username, password)
        self.client.login()

    def download_activity_files(self, start_date, filter_by=None):
        """Download matching activities starting on ``start_date``."""

        if filter_by is None:
            filter_by = DEFAULT_ACTIVITY_TYPES

        activities = self.client.get_activities_by_date(start_date)

        activity_ids = [
            (activity["activityId"], activity["activityType"]["typeKey"])
            for activity in activities
            if activity["activityType"]["typeKey"] in filter_by
        ]

        for activity_id, activity_type in activity_ids:
            data = self.client.download_activity(activity_id, dl_fmt=self.client.ActivityDownloadFormat.ORIGINAL)
            with open(f"{activity_id}_{activity_type}.zip", "wb") as file_object:
                file_object.write(data)

        return [f"{activity_id}_{activity_type}.zip" for activity_id, activity_type in activity_ids]

    def is_valid_workout(self, workout_as_json):
        """Validate a workout JSON object against the Garmin Training API schema."""
        try:
            workout = BaseWorkout.model_validate(workout_as_json)
            return workout is not None
        except Exception:
            return False

    def upload_workout(self, workout_as_json):
        """Upload a workout JSON object to Garmin Connect."""
        try:
            result = self.client.upload_workout(workout_as_json)
            return result
        except Exception:
            return None

    def get_devices(self):
        """Retrieve the list of devices associated with the Garmin account."""
        try:
            devices = self.client.get_devices()
            return [{"key": str(i + 1), "device": device["displayName"], "id": device["deviceId"]} for i, device in enumerate(devices)]
        except Exception:
            return None
        
    def push_workout_to_device(self, workout_id, device_id):
        """Push a workout to a specific device."""
        try:
            success = self.client.push_workout_to_device(workout_id, device_id)
            return success
        except Exception:
            return False