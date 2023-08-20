import sys
import csv
import json
import os
import time
import threading

version_number = 0.1

# ANSI codes for colors and text attributes
RED = '\033[31m'           # Red
RED_BOLD = '\033[1;31m'    # Bold and Red
YELLOW = '\033[33m'        # Yellow
YELLOW_BOLD = '\033[1;33m'  # Bold and Yellow
GREEN = '\033[32m'         # Green
GREEN_BOLD = '\033[1;32m'  # Bold and Green
RESET = '\033[0m'          # Reset to default


def openingText():
    

    program_name = f"{YELLOW_BOLD}SuperNew{RESET} CSV -> JSON Converter"
    version_number_formatted = f"v{YELLOW}{version_number}{RESET}"

    print()
    print("~" * (len(program_name)-(len(YELLOW_BOLD)+len(RESET))))
    print(program_name)
    print(version_number_formatted)
    print("~" * (len(program_name)-(len(YELLOW_BOLD)+len(RESET))))
    print()


def isValidCSV(filename):
    if filename.endswith(".csv"):
        if len(filename) == 4: 
            print(f"\n({RED_BOLD}ERROR{RESET}): No file name detected.\n")
            return False
        return True
    return False


def isValidFile(filepath):
    return os.path.exists(filepath)


def csv_to_json(csv_filename):
    spinner = Spinner()
    spinner.start()

    data = []
    
    # Open CSV file for reading
    with open(csv_filename, 'r') as csvfile:
        # Specify delimiter as ';'
        csvreader = csv.DictReader(csvfile, delimiter=';')
        
        # Convert each row into a dictionary, replace empty strings with None, and add to list
        for row in csvreader:
            processed_row = {k: (v if v != "" else None) for k, v in row.items()}
            data.append(processed_row)

    # Convert list of dictionaries to JSON format
    json_data = json.dumps(data, indent=4)
    
    # Write the JSON data to a new file
    with open(csv_filename.replace('.csv', '.json'), 'w') as jsonfile:
        jsonfile.write(json_data)
    
    spinner.stop()


# Spinner class to show processing animation
class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while True:
            for cursor in '|/-\\':
                yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)



# Program Starts Here
openingText()


if len(sys.argv) > 1:
    file_import = sys.argv[1]

else:
    print(f"Enter a valid .csv file. Ex: {GREEN}numbers.csv{RESET}")
    file_import = input("Enter the .csv file or filepath here: ")

while not isValidCSV(file_import) or not isValidFile(file_import):

    if not isValidCSV(file_import):
        print(f"{RED_BOLD}That is not a valid .csv file.{RESET}")

    else:
        print(f"{RED_BOLD}The file does not exist.{RESET}")

    file_import = input("Please re-enter the .csv file or filepath: \n")


print(f"{GREEN_BOLD}File detected{RESET} for import. Processing {GREEN_BOLD}{file_import}{RESET}: ")

# Convert the CSV to JSON
csv_to_json(file_import)

print(f"\n{GREEN_BOLD}Conversion completed!{RESET} JSON file saved as {GREEN_BOLD}{file_import.replace('.csv', '.json')}{RESET}")