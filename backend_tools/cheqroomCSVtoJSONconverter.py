import sys
import csv
import json
import os

import utils

from collections import OrderedDict

version_number = 0.3
program_name = "CSV -> JSON Converter"


category_id_mapping = {
    'Uncategorized': 1, 'Video': 2, 'Cameras': 3, 'Drones': 4, 'Accessories': 75,
    'Camera Supports': 7, 'Tripods': 8, 'Gimbals': 10, 'Lenses': 12, 'Primes': 13,
    'Zooms': 14, 'Cables': 93, 'HDMI': 16, 'HD-SDI': 17, 'DisplayPort': 18, 'Displays': 20,
    'Desktop': 21, 'Field': 22, 'EVF': 23, 'Switchers': 25, 'Audio': 26, 'Microphones': 27,
    'XLR': 32, '3.5mm | 1/8in': 34, '6.35mm | 1/4in': 33, 'Adapters': 35, 'Wireless': 36,
    'Recorders': 37, 'Interfaces': 38, 'Communications': 39, 'Radios': 40, 'Speakers': 41,
    'Lighting': 42, 'Modifiers': 43, 'Reflectors & Diffusion': 44, 'Holders': 45,
    'Softboxes': 46, 'Bowens Mount': 53, 'Barndoors': 48, 'Snoots': 50, 'Projection Lenses': 52,
    'Lights': 54, 'Grip': 56, 'Stands': 57, 'Light Stands': 58, 'Rollable': 59, 'Foldable': 60,
    'C-Stands': 62, 'Mic Stands': 63, 'Baby Pin Accessories': 65, 'Sandbags': 66,
    'Stage/Studio': 67, 'Backdrops': 68, 'Apple Boxes': 69, 'Computer': 76, 'iPads': 71,
    'Desktops': 73, 'Laptops': 74, 'Batteries': 77, 'V-Mount': 78, 'Chargers': 91,
    'Gold Mount': 80, 'NP-F': 82, 'BP-U30': 84, 'LP-E6NH': 86, 'Mini 2': 88, 'Mavic 3': 90,
    'Ronin 2': 92, 'Extension Cords': 94, 'Storage & Transport': 95, 'Cases': 96, 'Carts': 97
}

category_parent_mapping = {
    (None, 'Uncategorized'): 1, (None, 'Video'): 2, ('Video', 'Cameras'): 3, ('Cameras', 'Drones'): 4,
    ('Drones', 'Accessories'): 5, ('Cameras', 'Accessories'): 6, ('Video', 'Camera Supports'): 7,
    ('Camera Supports', 'Tripods'): 8, ('Tripods', 'Accessories'): 9, ('Camera Supports', 'Gimbals'): 10,
    ('Gimbals', 'Accessories'): 11, ('Video', 'Lenses'): 12, ('Lenses', 'Primes'): 13, ('Lenses', 'Zooms'): 14,
    ('Video', 'Cables'): 15, ('Cables', 'HDMI'): 16, ('Cables', 'HD-SDI'): 17, ('Cables', 'DisplayPort'): 18,
    ('Cables', 'Accessories'): 19, ('Video', 'Displays'): 20, ('Displays', 'Desktop'): 21, ('Displays', 'Field'): 22,
    ('Displays', 'EVF'): 23, ('Displays', 'Accessories'): 24, ('Video', 'Switchers'): 25, (None, 'Audio'): 26,
    ('Audio', 'Microphones'): 27, ('Microphones', 'XLR'): 28, ('Microphones', '3.5mm | 1/8in'): 29,
    ('Microphones', 'Accessories'): 30, ('Audio', 'Cables'): 31, ('Cables', 'XLR'): 32,
    ('Cables', '6.35mm | 1/4in'): 33, ('Cables', '3.5mm | 1/8in'): 34, ('Cables', 'Adapters'): 35,
    ('Audio', 'Wireless'): 36, ('Audio', 'Recorders'): 37, ('Audio', 'Interfaces'): 38,
    ('Audio', 'Communications'): 39, ('Communications', 'Radios'): 40, ('Audio', 'Speakers'): 41,
    (None, 'Lighting'): 42, ('Lighting', 'Modifiers'): 43, ('Modifiers', 'Reflectors & Diffusion'): 44,
    ('Reflectors & Diffusion', 'Holders'): 45, ('Modifiers', 'Softboxes'): 46, ('Softboxes', 'Bowens Mount'): 47,
    ('Modifiers', 'Barndoors'): 48, ('Barndoors', 'Bowens Mount'): 49, ('Modifiers', 'Snoots'): 50,
    ('Snoots', 'Bowens Mount'): 51, ('Modifiers', 'Projection Lenses'): 52, ('Projection Lenses', 'Bowens Mount'): 53,
    ('Lighting', 'Lights'): 54, ('Lights', 'Accessories'): 55, (None, 'Grip'): 56, ('Grip', 'Stands'): 57,
    ('Stands', 'Light Stands'): 58, ('Light Stands', 'Rollable'): 59, ('Light Stands', 'Foldable'): 60,
    ('Light Stands', 'Accessories'): 61, ('Stands', 'C-Stands'): 62, ('Stands', 'Mic Stands'): 63,
    ('Stands', 'Accessories'): 64, ('Grip', 'Baby Pin Accessories'): 65, ('Grip', 'Sandbags'): 66,
    ('Grip', 'Stage/Studio'): 67, ('Stage/Studio', 'Backdrops'): 68, ('Stage/Studio', 'Apple Boxes'): 69,
    (None, 'Computer'): 76, ('Computer', 'iPads'): 71, ('iPads', 'Accessories'): 72, ('Computer', 'Desktops'): 73,
    ('Computer', 'Laptops'): 74, ('Computer', 'Accessories'): 75, ('Computer', 'Batteries'): 77,
    ('Batteries', 'V-Mount'): 78, ('V-Mount', 'Chargers'): 79, ('Batteries', 'Gold Mount'): 80,
    ('Gold Mount', 'Chargers'): 81, ('Batteries', 'NP-F'): 82, ('NP-F', 'Chargers'): 83, ('Batteries', 'BP-U30'): 84,
    ('BP-U30', 'Chargers'): 85, ('Batteries', 'LP-E6NH'): 86, ('LP-E6NH', 'Chargers'): 87, ('Batteries', 'Mini 2'): 88,
    ('Mini 2', 'Chargers'): 89, ('Batteries', 'Mavic 3'): 90, ('Mavic 3', 'Chargers'): 91, ('Batteries', 'Ronin 2'): 92,
    ('Ronin 2', 'Chargers'): 93, ('Batteries', 'Accessories'): 94, (None, 'Storage & Transport'): 95,
    ('Storage & Transport', 'Cases'): 96, ('Cases', 'Accessories'): 97
}


def isValidCSV(filename):
    if filename.endswith(".csv"):
        if len(filename) == 4: 
            print(f"\n({utils.RED}ERROR{utils.RESET}): No file name detected.\n")
            return False
        return True
    return False


def isValidFile(filepath):
    return os.path.exists(filepath)


def read_csv_to_list_of_dicts(csv_filename):
    data = []
    with open(csv_filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',')
        for row in csvreader:
            processed_row = {k: (v if v != "" else None) for k, v in row.items()}
            data.append(processed_row)
    return data


def insert_category_id_to_list_of_dicts(data, category_id_mapping, category_parent_mapping):
    for row in data:
        ordered_row = OrderedDict(row)
        new_ordered_row = OrderedDict()
        
        category_name = ordered_row.get("Category Name", None)
        category_parent_name = ordered_row.get("Category Parent Name", None)
        
        category_id = category_parent_mapping.get((category_parent_name, category_name), 1)
        
        for key, value in ordered_row.items():
            new_ordered_row[key] = value
            if key == "Category Name":
                new_ordered_row["category_id"] = category_id
        
        row.clear()
        row.update(new_ordered_row)



def write_list_of_dicts_to_csv(data, csv_filename):
    fieldnames = data[0].keys()
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def list_of_dicts_to_json(data, json_filename):
    json_data = json.dumps(data, indent=4)
    with open(json_filename, 'w') as jsonfile:
        jsonfile.write(json_data)



def main():
    utils.openingText(program_name, version_number)


    if len(sys.argv) > 1:
        file_import = sys.argv[1]

    else:
        print(f"Enter a valid .csv file. Ex: {utils.GREEN}numbers.csv{utils.RESET}")
        file_import = input("Enter the .csv file or filepath here: ")

    while not isValidCSV(file_import) or not isValidFile(file_import):

        if not isValidCSV(file_import):
            print(f"{utils.RED_BOLD}That is not a valid .csv file.{utils.RESET}")

        else:
            print(f"{utils.RED_BOLD}The file does not exist.{utils.RESET}")

        file_import = input("Please re-enter the .csv file or filepath: \n")


    print(f"{utils.GREEN_BOLD}File detected{utils.RESET} for import. Processing {utils.GREEN_BOLD}{file_import}{utils.RESET}: ")


    data = read_csv_to_list_of_dicts(file_import)

    insert_category_id_to_list_of_dicts(data, category_id_mapping, category_parent_mapping)

    # write_list_of_dicts_to_csv(data, file_import)

    list_of_dicts_to_json(data, file_import.replace('.csv', '.json'))

    print(f"\n{utils.GREEN_BOLD}Conversion completed!{utils.RESET} JSON file saved as {utils.GREEN_BOLD}{file_import.replace('.csv', '.json')}{utils.RESET}")

if __name__ == "__main__":
    main()