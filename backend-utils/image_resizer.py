import sys
import os
from PIL import Image
from utils import Spinner, signal_handler, RED, RED_BOLD, GREEN, GREEN_BOLD, RESET
import signal

version_number = 0.3
program_name = "Image Resizer"

size_map = {
    "0-original": None,  # No resizing for original
    "1-x-small": 64,
    "2-small": 128,
    "3-medium": 256,
    "4-large": 512,
    "5-x-large": 1024,
    "6-mongo": 2048
}

def isValidImage(filename):
    valid_exts = [".jpg", ".jpeg"]
    _, ext = os.path.splitext(filename)
    return ext.lower() in valid_exts

def isValidFile(filepath):
    return os.path.exists(filepath)

def resize_image(file_path, output_dir, label):
    with Image.open(file_path) as img:
        width, height = img.size
        output_filename = os.path.basename(file_path).split(".")[0] + "_" + label + ".jpg"
        output_path = os.path.join(output_dir, output_filename)

        if label == "0-original":
            img.save(output_path, "JPEG", quality=90)
            print(f"Processed image size: {GREEN_BOLD}{label}{RESET}")
            return

        if width > height:
            new_width = size_map[label]
            new_height = int((height / width) * size_map[label])
        else:
            new_height = size_map[label]
            new_width = int((width / height) * size_map[label])

        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        resized_img.save(output_path, "JPEG", quality=90)
        print(f"Processed image size: {GREEN_BOLD}{label}{RESET}")

# From utils.py. Handles CTRL + C for graceful stopping.
signal.signal(signal.SIGINT, signal_handler)

def main():
    if len(sys.argv) > 2:
        file_import = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        file_import = input("Enter the image file or filepath here: ")
        output_dir = input("Enter the output directory: ")

    while not isValidImage(file_import) or not isValidFile(file_import):
        if not isValidImage(file_import):
            print(f"{RED_BOLD}That is not a valid image file.{RESET}")
        else:
            print(f"{RED_BOLD}The file does not exist.{RESET}")
        file_import = input("Please re-enter the image file or filepath: \n")

    spinner = Spinner()
    spinner.start()

    print(f"{GREEN_BOLD}File detected{RESET} for processing. Resizing {GREEN_BOLD}{file_import}{RESET}: ")

    for label in size_map.items():
        resize_image(file_import, output_dir, label)

    spinner.stop()

    print(f"\n{GREEN_BOLD}Resizing completed!{RESET} Images saved in {GREEN_BOLD}{output_dir}{RESET}")

if __name__ == "__main__":
    main()
