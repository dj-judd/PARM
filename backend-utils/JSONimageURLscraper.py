import requests
import os
import sys
import json
from utils import Spinner, signal_handler, UNDERLINED, GREEN_BOLD, YELLOW_BOLD, RESET
import signal

version_number = 0.2
program_name = "JSON Image Scraper"


def download_image(url, save_directory, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    filename = os.path.join(save_directory, f"{filename}.jpg")
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)


def main():
    global spinner

    # Ensure we have the correct arguments
    if len(sys.argv) != 2:
        print("Usage: python script_name.py /path/to/jsonfile.json")
        sys.exit(1)

    json_file_path = sys.argv[1]
    
    if not os.path.exists(json_file_path):
        print(f"File not found: {json_file_path}")
        sys.exit(1)

    # Read the JSON data
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    save_directory = "/home/dj/src/PARM-Production_Asset_Reservation_Manager/backend-utils/database/data/images"

    # Ensure the save directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)


    spinner = Spinner()

    # From utils.py. Handles CTRL + C for graceful stopping.
    signal.signal(signal.SIGINT, lambda signum, frame: signal_handler(spinner, signum, frame))


    spinner.start()

    # Download images
    for entry in data:
        image_name = entry.get("Name")
        image_url = entry.get("Image Url")
        
        if image_name and image_url:
            file_path = os.path.join(save_directory, f"{image_name}.jpg")
            if not os.path.exists(file_path):
                download_image(image_url, save_directory, image_name)
                print(f"Image for {UNDERLINED}{image_name}{RESET} has been {GREEN_BOLD}downloaded{RESET}.")
            else:
                print(f"Image for {UNDERLINED}{image_name}{RESET} has been {YELLOW_BOLD}skipped{RESET}.")

    spinner.stop()
    print("\nImages processed successfully!")

if __name__ == "__main__":
    main()
