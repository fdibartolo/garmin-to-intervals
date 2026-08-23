from garminconnect import Garmin

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
