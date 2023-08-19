from sys import argv
import csv
import json
import os

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
        if len(filename) > 4:
            return True
        else: 
            print(f"\n({RED_BOLD}ERROR{RESET}): No file name detected.\n")
            return False
    else:
        return False

    # return filename.endswith(".csv")

def isValidFile(filepath):
    return os.path.exists(filepath)




# Starts Here
openingText()



if len(argv) > 1:
    file_import = argv[1]

else:
    print(f"Enter a valid .csv file. Ex: {GREEN}numbers.csv{RESET}")
    file_import = input("Enter the .csv file or filepath here: ")


while not isValidCSV(file_import):

    print(f"{RED_BOLD}That is not a valid .csv file.{RESET}")
    file_import = input("Please re-enter the .csv file or filepath: \n")



print(f"\n{GREEN_BOLD}File detected{RESET} for import. Processing {GREEN_BOLD}{file_import}{RESET}: ")