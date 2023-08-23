import sys
import os
from PIL import Image
from utils import openingText, Spinner, signal_handler, RED, RED_BOLD, GREEN, GREEN_BOLD, RESET
import signal

version_number = 0.2
program_name = "Image Resizer"

size_map = {
    "x-small": 64,
    "small": 256,
    "medium": 512,
    "large": 1024,
    "x-large": 2048
}

def isValidImage(filename):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if any(filename.endswith(ext) for ext in valid_extensions):
        if len(filename) <= 4:
            print(f"\n({RED_BOLD}ERROR{RESET}): No file name detected.\n")
            return False
        return True
    return False

def isValidFile(filepath):
    return os.path.exists(filepath)

def resize_image(input_path, output_dir, size_label):
    spinner = Spinner()
    spinner.start()

    with Image.open(input_path) as img:
        width, height = img.size
        max_size = size_map[size_label]

        if width > height:
            new_width = max_size
            new_height = int((height / width) * max_size)
        else:
            new_height = max_size
            new_width = int((width / height) * max_size)

        resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)
        os.makedirs(output_dir, exist_ok=True)

        base_name = os.path.basename(input_path)
        name, ext = os.path.splitext(base_name)
        output_path = os.path.join(output_dir, f"{name}_{size_label}{ext}")

        resized_img.save(output_path, "JPEG")

    spinner.stop()

signal.signal(signal.SIGINT, signal_handler)

def main():
    openingText(program_name, version_number)

    if len(sys.argv) > 1:
        file_import = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    else:
        print(f"Enter a valid image file. Ex: {GREEN}sample.jpg{RESET}")
        file_import = input("Enter the image file or filepath here: ")
        output_dir = input("Enter the output directory or leave empty for current directory: ") or "."

    while not isValidImage(file_import) or not isValidFile(file_import):
        if not isValidImage(file_import):
            print(f"{RED_BOLD}That is not a valid image file.{RESET}")
        else:
            print(f"{RED_BOLD}The file does not exist.{RESET}")
        file_import = input("Please re-enter the image file or filepath: \n")

    print(f"{GREEN_BOLD}File detected{RESET} for processing. Resizing {GREEN_BOLD}{file_import}{RESET}: ")

    for label in size_map.keys():
        resize_image(file_import, output_dir, label)
        print(f"Processed image size: {GREEN_BOLD}{label}{RESET}")

    print(f"\n{GREEN_BOLD}Resizing completed!{RESET} Images saved in {GREEN_BOLD}{output_dir}{RESET}")

if __name__ == "__main__":
    main()
