import os
import sys
import inspect
import json
import re
import shutil

from typing import Optional
from PIL import Image
import requests
from io import BytesIO


utils_version_number = 0.3
utils_program_name = "Utils"


# ANSI codes for colors and text attributes
UNDERLINED = "\033[4m"
RED = '\033[31m'           # Red
RED_BOLD = '\033[1;31m'    # Bold and Red
YELLOW = '\033[33m'        # Yellow
YELLOW_BOLD = '\033[1;33m' # Bold and Yellow
GREEN = '\033[32m'         # Green
GREEN_BOLD = '\033[1;32m'  # Bold and Green
BLUE = '\033[34m'          # Blue
BLUE_BOLD = '\033[1;34m'   # Bold and Blue
RESET = '\033[0m'          # Reset to default


def openingText(program_name, version_number):
    

    program_name_formatted = f"{YELLOW_BOLD}SuperNew{RESET} {program_name}"
    version_number_formatted = f"v{YELLOW}{version_number}{RESET}"

    print()
    print("~" * (len(program_name_formatted)-(len(YELLOW_BOLD)+len(RESET))))
    print(program_name_formatted)
    print(version_number_formatted)
    print("~" * (len(program_name_formatted)-(len(YELLOW_BOLD)+len(RESET))))
    print()


def errorMessage(e,
                 origin_file: Optional[str] = None,
                 line_number: Optional[int] = None):
    if origin_file is None or line_number is None:
        current_frame = inspect.currentframe()
        outer_frame = inspect.getouterframes(current_frame, 2)

        # Get the caller's file name
        origin_file = outer_frame[1][1]

        # Get the basename of the file
        filename = os.path.basename(origin_file)

        # Get the line number in the caller
        line_number = outer_frame[1][2]

        # Get the name of the caller function
        caller_name = inspect.stack()[1].function

        # Get type of object that the caller function is bound to
        frame = inspect.stack()[1]
        bound_to_type = frame[0].f_globals.get(frame[3])
        if inspect.ismethod(bound_to_type):
            object_type = type(bound_to_type).__name__
        else:
            object_type = "Method"

    print(f"\n{RED_BOLD}Error occurred!{RESET} on {UNDERLINED}Line {line_number}{RESET} in {YELLOW}{filename}{RESET}.")
    print(f"{BLUE}{object_type}{RESET} {YELLOW}{caller_name}{RESET} failed.\n")
    print(f"{e}\n\n")


def successMessage():
    # Get the name of the caller function
    caller_name = inspect.stack()[1].function
    print(f"{GREEN_BOLD}Success!{RESET} {YELLOW}{caller_name}{RESET} finished {GREEN}successfully.{RESET}")


def sanitize_name(name):
    if name is None:
        return None
    
    # Replace apostrophes (') with "ft"
    name = name.replace('\'', 'ft')
    
    # Replace double quotes (") with "in"
    name = name.replace('"', 'in')
    
    # Remove invalid characters
    name = re.sub(r'[\\/*?:<>|]', '_', name)  
    
    # Replace spaces with underscores
    name = name.replace(' ', '_')
    
    # Remove leading or trailing whitespace
    name = name.strip()
    
    return name


class ImageURLScaping:

    version_number = 0.32
    program_name = "Image Scraper Tools"


    @staticmethod
    def download_and_save_image(url, save_directory, filename):
        response = ImageURLScaping.requests.get(url, stream=True)
        response.raise_for_status()

        filename = os.path.join(save_directory, f"{filename}.jpg")
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)


    @staticmethod
    def download_image(url):
        response = requests.get(url)
        response.raise_for_status()
        img_data = BytesIO(response.content)
        img_obj = Image.open(img_data)

        return img_obj



    def batch_from_json(json_file_path,
                  save_directory):
        
        openingText(ImageURLScaping.program_name,
                    ImageURLScaping.version_number)

        # Read the JSON data
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # save_directory = "/home/dj/src/PARM-Production_Asset_Reservation_Manager/database/data/raw_images"

        # Ensure the save directory exists
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)


        # Download images
        for entry in data:
            # Sanitize the image name
            sanitized_image_name = sanitize_name(entry.get("Name"))

            # Add the sanitized name to the entry with a new key "Sanitized_Name"
            entry["Sanitized_ImageFile_Name"] = sanitized_image_name

            image_name = sanitized_image_name
            image_url = entry.get("Image Url")
            
            if image_name and image_url:
                file_path = os.path.join(save_directory, f"{image_name}.jpg")
                if not os.path.exists(file_path):
                    ImageURLScaping.download_and_save_image(image_url, save_directory, image_name)
                    print(f"Image for {UNDERLINED}{image_name}{RESET} has been {GREEN_BOLD}downloaded{RESET}.")
                else:
                    print(f"Image for {UNDERLINED}{image_name}{RESET} has been {YELLOW_BOLD}skipped{RESET}.")


        # Derive the new filename with the "_modified" suffix
        base, ext = os.path.splitext(json_file_path)
        new_filename = f"{base}_images_downloaded{ext}"

        # Write the modified data back to the new JSON file
        with open(new_filename, 'w') as file:
            json.dump(data, file, indent=4)

        
        print(f"\n{GREEN_BOLD}Images Downloaded successfully!{RESET}\n\n")


    def individual(image_url: str,
                   save_directory: str,
                   filename: str):
        
        # Ensure the save directory exists
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)


        # Sanitize the image name
        sanitized_image_name = sanitize_name(filename)

        image_name = sanitized_image_name
        
        if image_name and image_url:
            file_path = os.path.join(save_directory, f"{image_name}.jpg")
            if not os.path.exists(file_path):
                img = ImageURLScaping.download_and_save_image(image_url, save_directory, image_name)
                # with Image.open(file_path) as img:
                #     for label, max_size in ImageProcessing.image_size_map.items():
                #         ImageProcessing.resize_image_from_object(img, save_directory, label)
                print(f"Image for {image_name} has been downloaded.")
            else:
                print(f"Image for {image_name} has been skipped.")

        return img

        # print(f"\n{GREEN_BOLD}Images Downloaded successfully!{RESET}\n\n")



class ImageProcessing:


    version_number = 0.34
    program_name = "Image Processor"


    image_size_map = {
        "0-original": None,  # No resizing for original
        "1-xsmall": 64,
        "2-small": 128,
        "3-medium": 256,
        "4-large": 512,
        "5-xlarge": 1024,
        "6-mongo": 2048
    }

    def isValidImage(filename):
        valid_exts = [".jpg", ".jpeg", ".png"]
        _, ext = os.path.splitext(filename)
        return ext.lower() in valid_exts

    def isValidFile(filepath):
        return os.path.exists(filepath)


    @staticmethod
    def resize_image_from_path(file_path, output_dir, label):
        with Image.open(file_path) as img:
            width, height = img.size
            output_filename = "_".join(os.path.basename(file_path).split(".")[:-1]) + "_" + label + ".jpg"
            output_path = os.path.join(output_dir, output_filename)

            if label == "0-original":
                img.save(output_path, "JPEG", quality=90)
                print(f"Generated image size: {GREEN_BOLD}{label}{RESET}")
                return

            if width > height:
                new_width = ImageProcessing.image_size_map[label]
                new_height = int((height / width) * ImageProcessing.image_size_map[label])
            else:
                new_height = ImageProcessing.image_size_map[label]
                new_width = int((width / height) * ImageProcessing.image_size_map[label])

            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            resized_img.save(output_path, "JPEG", quality=90)
            print(f"Generated image size: {GREEN_BOLD}{label}{RESET}")


    
    @staticmethod
    def generate_single_image_variation(img: Image.Image,
                                        original_output_dir: str,
                                        output_dir: str,
                                        base_name: str,
                                        label: str,
                                        max_size: int):
        """Generates and saves a single resized variation of a given image object."""

        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if not os.path.exists(original_output_dir):
            os.makedirs(original_output_dir)

        sanitized_base_name = sanitize_name(base_name)
        output_filename = f"{sanitized_base_name}_{label}.jpg"

        if label == "0-original":
            output_path = os.path.join(original_output_dir, output_filename)
            img.convert("RGB").save(output_path, "JPEG", quality=90)
            return output_path, label

        output_path = os.path.join(output_dir, output_filename)

        width, height = img.size
        if width > height:
            new_width = max_size
            new_height = int((height / width) * max_size)
        else:
            new_height = max_size
            new_width = int((width / height) * max_size)

        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        resized_img.convert("RGB").save(output_path, "JPEG", quality=90)
        
        return output_path, label


    @staticmethod
    def generate_image_variations(img: Image.Image,
                                  original_output_dir: str,
                                  output_dir: str,
                                  base_name: str):
        """Generates and saves multiple resized variations of a given image object."""

        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if not os.path.exists(original_output_dir):
            os.makedirs(original_output_dir)

        sanitized_base_name = sanitize_name(base_name)

        for label, max_size in ImageProcessing.image_size_map.items():
            output_filename = f"{sanitized_base_name}_{label}.jpg"

            if label == "0-original":
                output_path = os.path.join(original_output_dir, output_filename)
                img.convert("RGB").save(output_path, "JPEG", quality=90)
                print(f"{GREEN_BOLD}Generated{RESET} image size: {UNDERLINED}{label}{RESET}")
                continue

            output_path = os.path.join(output_dir, output_filename)

            width, height = img.size
            if width > height:
                new_width = max_size
                new_height = int((height / width) * max_size)
            else:
                new_height = max_size
                new_width = int((width / height) * max_size)

            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            resized_img.convert("RGB").save(output_path, "JPEG", quality=90)
            print(f"{GREEN_BOLD}Generated{RESET} image size: {UNDERLINED}{label}{RESET}")

        return output_path


    
    @staticmethod
    def generate_image_variations_from_file(img: Image.Image,
                                            output_dir: str,
                                            original_file_path: str):
        """Generates and saves multiple resized variations of a given image object."""
        
        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for label, max_size in ImageProcessing.image_size_map.items():
            output_filename = label + ".jpg"
            output_path = os.path.join(output_dir, output_filename)

            if label == "0-original":
                shutil.copy(original_file_path, output_path)
                print(f"Generated image size: {label}")
                continue

            width, height = img.size

            if width > height:
                new_width = max_size
                new_height = int((height / width) * max_size)
            else:
                new_height = max_size
                new_width = int((width / height) * max_size)

            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            resized_img.save(output_path, "JPEG", quality=90)
            print(f"Generated image size: {label}")



    def main(file_import,
             output_dir):
        
        openingText(ImageProcessing.program_name,
                    ImageProcessing.version_number)


        print(f"{GREEN_BOLD}File detected{RESET} for processing. Resizing {GREEN_BOLD}{file_import}{RESET}: ")

        for label, max_size in ImageProcessing.image_size_map.items():
            ImageProcessing.resize_image_from_path(file_import, output_dir, label)


        print(f"\n{GREEN_BOLD}Resizing completed!{RESET} Images saved in {GREEN}{output_dir}{RESET}\n\n")