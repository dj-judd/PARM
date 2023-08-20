import sys
import csv
import json
import os
from utils import openingText, Spinner, signal_handler, RED, RED_BOLD, YELLOW, YELLOW_BOLD, GREEN, GREEN_BOLD, RESET
import signal

version_number = 0.2
program_name = "CSV -> JSON Converter"


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


# From utils.py. Handles CTRL + C for graceful stopping.
signal.signal(signal.SIGINT, signal_handler)


def main():
    openingText(program_name, version_number)


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

if __name__ == "__main__":
    main()