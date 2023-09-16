import requests
import os
import sys
import json
import re
import signal
from utils import openingText, Spinner, signal_handler, UNDERLINED, GREEN_BOLD, YELLOW_BOLD, RESET

version_number = 0.3
program_name = "JSON Image Scraper"

def sanitize_filename(filename):
    # Replace apostrophes (') with "ft"
    filename = filename.replace('\'', 'ft')
    
    # Replace double quotes (") with "in"
    filename = filename.replace('"', 'in')
    
    # Remove invalid characters
    filename = re.sub(r'[\\/*?:<>|]', '_', filename)  
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Remove leading or trailing whitespace
    filename = filename.strip()
    return filename

def download_image(url, save_directory, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    filename = os.path.join(save_directory, f"{filename}.jpg")
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)



def main():
    openingText(program_name, version_number)
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

    save_directory = "/home/dj/src/PARM-Production_Asset_Reservation_Manager/database/data/raw_images"

    # Ensure the save directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)


    spinner = Spinner()

    # From utils.py. Handles CTRL + C for graceful stopping.
    signal.signal(signal.SIGINT, lambda signum, frame: signal_handler(spinner, signum, frame))


    spinner.start()

    # Download images
    for entry in data:
        # Sanitize the image name
        sanitized_image_name = sanitize_filename(entry.get("Name"))

        # Add the sanitized name to the entry with a new key "Sanitized_Name"
        entry["Sanitized_ImageFile_Name"] = sanitized_image_name

        image_name = sanitized_image_name
        image_url = entry.get("Image Url")
        
        if image_name and image_url:
            file_path = os.path.join(save_directory, f"{image_name}.jpg")
            if not os.path.exists(file_path):
                download_image(image_url, save_directory, image_name)
                print(f"Image for {UNDERLINED}{image_name}{RESET} has been {GREEN_BOLD}downloaded{RESET}.")
            else:
                print(f"Image for {UNDERLINED}{image_name}{RESET} has been {YELLOW_BOLD}skipped{RESET}.")


    # Derive the new filename with the "_modified" suffix
    base, ext = os.path.splitext(json_file_path)
    new_filename = f"{base}_images_downloaded{ext}"

    # Write the modified data back to the new JSON file
    with open(new_filename, 'w') as file:
        json.dump(data, file, indent=4)

    
    spinner.stop()

    print(f"\n{GREEN_BOLD}Images Downloaded successfully!{RESET}\n\n")

if __name__ == "__main__":
    main()
