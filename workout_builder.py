#!/usr/bin/env python3
""" Garmin Workout Builder """

import json
import os
from dotenv import load_dotenv
from src.constants import GREEN, RED, RESET, YELLOW
from src.genai import GenAI
from src.garmin_connect import GarminConnect
from src.helper import Helper

def main():
    prompt = input(f"{YELLOW}\n ➜ Describe the workout you want to build: {RESET}")
    print(f"{YELLOW} ➜ Generating workout...{RESET}")

    try:
        genai_client = GenAI(os.getenv("GEMINI_API_KEY"), os.getenv("GEMINI_MODEL"))
        response = genai_client.generate_content(prompt)

        if os.getenv("WORKOUT_UPLOAD_CONFIRMATION").lower() == "true":
            print(response)
            proceed = input(f"{YELLOW}\n ➜ Please review the generated workout. Proceed with uploading it?\n[y]es\n[n]o\n ➜ {RESET}")
            if proceed.lower() != "y":
                print(f"{YELLOW} ➜ Upload skipped by the user, exiting...{RESET}")
                return

        workout_as_json = json.loads(response)
        
        garmin_connect = GarminConnect(os.getenv("GARMIN_USERNAME"), os.getenv("GARMIN_PASSWORD"))
        if not garmin_connect.is_valid_workout(workout_as_json):
            print(f"{RED} ✗ Generated workout is invalid.{RESET}")
            return
        
        print(f"{YELLOW} ➜ Uploading workout...{RESET}")
        result = garmin_connect.upload_workout(workout_as_json)
        if result is None:
            print(f"{RED} ✗ Failed to upload workout.{RESET}")
            return

        print(f"{GREEN} ✓ Workout uploaded successfully! (ID: {result['workoutId']}){RESET}")

        devices = garmin_connect.get_devices()
        if devices:
            device_options = "\n".join([f"[{d['key']}] {d['device']}" for d in devices])
            push_to_device = input(f"{YELLOW}\n ➜ Do you want to push the workout to your device?\n{device_options}\n[s]kip\n ➜ {RESET}")
            if push_to_device in [d['key'] for d in devices]:
                device_id = next(d['id'] for d in devices if d['key'] == push_to_device)
                success = garmin_connect.push_workout_to_device(result['workoutId'], device_id)
                if success:
                    print(f"{GREEN} ✓ Workout pushed to device successfully!{RESET}")
                else:
                    print(f"{RED} ✗ Failed to push workout to device.{RESET}")

        save_workout = input(f"{YELLOW}\n ➜ Do you want to save the workout locally?\n[y]es\n[n]o\n ➜ {RESET}")
        if save_workout.lower() == "y":
            filename = f"{result['workoutName']}_({result['workoutId']}).json"
            Helper.save_workout(filename, workout_as_json)
            print(f"{GREEN} ✓ Workout saved locally at {filename}{RESET}")

    except Exception as e:
        print(f"{RED} ✗ An error occurred while generating the workout: {e}{RESET}")
        return

if __name__ == "__main__":
    load_dotenv() 
    main()
