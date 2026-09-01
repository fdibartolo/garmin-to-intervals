#!/usr/bin/env python3
""" Garmin to Intervals.icu Activity Uploader """

import sys, os
from dotenv import load_dotenv
from datetime import datetime
from constants import GREEN, RED, RESET, YELLOW
from helper import Helper
from garmin_connect import GarminConnect
from intervals_uploader import IntervalsUploader

def process_activities(start_date):
    print(f"{YELLOW} ➜ Processing activities...{RESET}")
    
    garmin_connect = GarminConnect(os.getenv("GARMIN_USERNAME"), os.getenv("GARMIN_PASSWORD"))
    files = garmin_connect.download_activity_files(start_date)
    if len(files) > 0:
        print(f"{GREEN} ✓ Downloaded {len(files)} activity files from Garmin...{RESET}")

        intervals_uploader = IntervalsUploader(os.getenv("INTERVALS_ATHLETE_ID"), os.getenv("INTERVALS_USERNAME"), os.getenv("INTERVALS_PASSWORD"))
        success = intervals_uploader.upload_activity_files(files)
        if success:
            print(f"{GREEN} ✓ Uploaded {len(files)} activity files to Intervals.icu!{RESET}")
        
        print(f"{YELLOW} ➜ Cleaning things up...{RESET}")
        [os.remove(file) for file in files]
        print(f"{GREEN} ✓ Done!{RESET}")
    else:
        print(f"{YELLOW} ➜ No activities were uploaded.{RESET}")
    
def main(args):
    if len(args) == 1:
        print(f"{YELLOW} ➜ Defaulting to today's date to process activities...{RESET}")
        start_date = datetime.today().strftime('%Y-%m-%d')
    elif len(args) == 2:
        start_date = Helper.parse_start_date_from(args[1])
        if start_date is None:
            print(f"{RED} ✗ Invalid date format: {args[1]}. Please use YYYY-MM-DD.{RESET}")
            sys.exit(1)
        print(f"{YELLOW} ➜ Using {start_date} to process activities...{RESET}")
    else:
        print("Usage: python main.py <start_date | YYYY-MM-DD>. If no date is provided, today's date will be used.")
        sys.exit(1)

    try:
        process_activities(start_date)
    except Exception as e:
        print(f"{RED} ✗ An error occurred while processing activities: {e}{RESET}")
        sys.exit(1)
    
if __name__ == "__main__":
    load_dotenv() 
    main(sys.argv)