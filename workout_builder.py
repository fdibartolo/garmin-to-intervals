#!/usr/bin/env python3
""" Garmin Workout Builder """

import json
import os
import sys
from dotenv import load_dotenv
from src.constants import GREEN, RED, RESET, YELLOW
from src.genai import GenAI
from src.garmin_connect import GarminConnect
from src.helper import Helper

def print_help():
    print("\nGarmin workout builder")
    print("----------------------")
    print("Usage: python workout_builder.py [-h] [-f <path>]")
    print("  -f <path>   Load the workout from a JSON file")
    print("  -h          Show this help message")
    print("\n")
    print("  if no args are passed, you will be prompted to describe the workout, and will be generated using AI")
    print("\n")

def generate_workout(prompt):
    print(f"{YELLOW} ➜ Generating workout...{RESET}")
    genai_client = GenAI(os.getenv("GEMINI_API_KEY"), os.getenv("GEMINI_MODEL"))
    response = genai_client.generate_content(prompt)

    if os.getenv("WORKOUT_UPLOAD_CONFIRMATION").lower() == "true":
        print(response)
        proceed = input(f"{YELLOW}\n ➜ Please review the generated workout. Proceed with uploading it?\n[y]es\n[n]o\n ➜ {RESET}")
        if proceed.lower() != "y":
            print(f"{YELLOW} ➜ Upload skipped by the user, exiting...{RESET}")
            return None

    return json.loads(response)

def upload_workout(garmin_connect, workout_as_json):
    if not garmin_connect.is_valid_workout(workout_as_json):
        print(f"{RED} ✗ Generated workout is invalid.{RESET}")
        return None

    print(f"{YELLOW} ➜ Uploading workout...{RESET}")
    result = garmin_connect.upload_workout(workout_as_json)
    if result is None:
        print(f"{RED} ✗ Failed to upload workout.{RESET}")
        return None

    print(f"{GREEN} ✓ Workout uploaded successfully! (ID: {result['workoutId']}){RESET}")
    return result

def offer_push_to_device(garmin_connect, workout_id):
    devices = garmin_connect.get_devices()
    if not devices:
        return

    device_options = "\n".join([f"[{d['key']}] {d['device']}" for d in devices])
    push_to_device = input(f"{YELLOW}\n ➜ Do you want to push the workout to your device?\n{device_options}\n[s]kip\n ➜ {RESET}")
    if push_to_device not in [d['key'] for d in devices]:
        return

    device_id = next(d['id'] for d in devices if d['key'] == push_to_device)
    if garmin_connect.push_workout_to_device(workout_id, device_id):
        print(f"{GREEN} ✓ Workout pushed to device successfully!{RESET}")
    else:
        print(f"{RED} ✗ Failed to push workout to device.{RESET}")

def offer_save_locally(workout_as_json, result):
    save_workout = input(f"{YELLOW}\n ➜ Do you want to save the workout locally?\n[y]es\n[n]o\n ➜ {RESET}")
    if save_workout.lower() != "y":
        return

    filename = f"{result['workoutName']}_({result['workoutId']}).json"
    Helper.save_workout(filename, workout_as_json)
    print(f"{GREEN} ✓ Workout saved locally at {filename}{RESET}")

def main(argv):
    if "-h" in argv:
        print_help()
        return

    try:
        if "-f" in argv:
            file_index = argv.index("-f")
            with open(argv[file_index + 1], "r", encoding="utf-8") as file:
                workout_as_json = json.load(file)
        else:
            prompt = input(f"{YELLOW}\n ➜ Describe the workout you want to build: {RESET}")
            workout_as_json = generate_workout(prompt)

        if workout_as_json is None:
            return

        garmin_connect = GarminConnect(os.getenv("GARMIN_USERNAME"), os.getenv("GARMIN_PASSWORD"))
        result = upload_workout(garmin_connect, workout_as_json)
        if result is None:
            return

        offer_push_to_device(garmin_connect, result['workoutId'])
        offer_save_locally(workout_as_json, result)

    except Exception as e:
        print(f"{RED} ✗ An error occurred: {e}{RESET}")
        return

if __name__ == "__main__":
    load_dotenv() 
    main(sys.argv)
