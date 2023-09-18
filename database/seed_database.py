"""Script to seed database."""

import os
import sys
import csv
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import hashlib
import json
import random
from random import choice, randint
from datetime import datetime
from sqlalchemy import text
from itertools import product

import crud
import model

from backend_tools import utils
import server


version_number = 0.4
program_name = "PARM Database Seeder 3,000,000"

db_init_message = "Generated automatically upon database creation."
number_of_users_to_generate = 15


# Drop and create database
os.system('dropdb parm')
os.system('createdb parm')


# Execute SQL script on the database
os.system('psql -d parm < PARM-Schema.sql')

model.connect_to_db(server.app)
model.db.create_all()




def populate_initial_colors():
    try:

        primary_color_01 = crud.create.color("Paper White | Default",
                                             "#f0eae7",
                                             audit=False,
                                             commit=False)
        
        secondary_color_01 = crud.create.color("Sky Blue | Default",
                                               "#17baeb",
                                               audit=False,
                                               commit=False)
        

        primary_color_02 = crud.create.color("Dark Gray | Default",
                                             "#0f0d12",
                                             audit=False,
                                             commit=False)
        
        secondary_color_02 = crud.create.color("Hot Red | Default",
                                               "#eb315d",
                                               audit=False,
                                               commit=False)        
        

        model.db.session.commit()
        utils.successMessage()

        return primary_color_01, secondary_color_01, primary_color_02, secondary_color_02

    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)



def populate_initial_ui_themes(primary_color_01_id, secondary_color_01_id, primary_color_02_id, secondary_color_02_id):
    try:

        light_ui_theme = crud.create.ui_theme("Light Theme",
                                              "Clean & Cultured",
                                              primary_color_01_id,
                                              secondary_color_01_id,
                                              audit=False,
                                              commit=False)
        
        dark_ui_theme = crud.create.ui_theme("Dark Theme",
                                             "Cyberpunk Styling",
                                             primary_color_02_id,
                                             secondary_color_02_id,
                                             audit=False,
                                             commit=False)

        model.db.session.commit()
        utils.successMessage()

        return light_ui_theme, dark_ui_theme

    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)



def populate_initial_global_settings(deployment_fingerprint=None,
                                     default_currency_id=1):
    try:

        if deployment_fingerprint is None:
            deployment_fingerprint = generate_deployment_fingerprint() 
        else:
            deployment_fingerprint = generate_deployment_fingerprint(deployment_fingerprint)

        global_settings = crud.create.global_settings(deployment_fingerprint=deployment_fingerprint,
                                                      default_currency_id=default_currency_id,
                                                      audit=False,
                                                      commit=False)

        model.db.session.commit()
        utils.successMessage()

        return global_settings


    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)



def populate_boostrap_user(password_hash,
                           first_name,
                           last_name,
                           currency_id,
                           time_format_is_24h,
                           ui_theme_id,
                           middle_name=None,
                           nickname=None,
                           nickname_preferred=None,
                           last_login=None):
    try:

        bootstrap_user, bootstrap_user_settings = crud.create.bootstrap_user(id=0,
                                                    password_hash=password_hash,
                                                    first_name=first_name,
                                                    last_name=last_name,
                                                    currency_id=currency_id,
                                                    time_format_is_24h=time_format_is_24h,
                                                    ui_theme_id=ui_theme_id,
                                                    middle_name=middle_name,
                                                    nickname=nickname,
                                                    nickname_preferred=nickname_preferred,
                                                    last_login=last_login,
                                                    audit=False,
                                                    commit=False)

        # Attempt to make sure the auto-incrementing sequences start back at "1".
        adjust_sequence("user_settings_id_seq", 1, commit=False)
        adjust_sequence("users_id_seq", 1, commit=False)

        model.db.session.commit()
        utils.successMessage()

        return bootstrap_user, bootstrap_user_settings


    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)


# # Adjust sequence after inserting into user_settings
# adjust_sequence(sequence_name="user_settings_id_seq", value=0)


# # Adjust sequence after inserting the bootstrap user
# adjust_sequence(sequence_name="users_id_seq", value=0)


# def disable_not_null_constraint(table_name, column_name):
#     model.db.session.execute(f"ALTER TABLE {table_name} ALTER COLUMN {column_name} DROP NOT NULL;")
#     model.db.session.commit()


# def enable_not_null_constraint(table_name, column_name):
#     model.db.session.execute(f"ALTER TABLE {table_name} ALTER COLUMN {column_name} SET NOT NULL;")
#     model.db.session.commit()


def adjust_sequence(sequence_name, value=0, commit=True):
    model.db.session.execute(f"SELECT setval('{sequence_name}', {value}, false);")
    if commit:
        model.db.session.commit()


def populate_bootstrap_audit_entries(p_color_01_id,
                                     s_color_01_id,
                                     p_color_02_id,
                                     s_color_02_id,
                                     light_ui_id,
                                     dark_ui_id,
                                     global_settings_fingerprint,
                                     bootstrap_user_settings_id,
                                     bootstrap_user_id):
    
    try:
        primary_color_01_audit_entry = crud.create.audit_entry(operation_type = model.OperationType.CREATE.value,
                                                               auditable_entity_type = model.CLASS_TO_ENUM_MAP['Color'],
                                                               related_entity_id = p_color_01_id,
                                                               audit_details = db_init_message,
                                                               created_by_user_id = bootstrap_user_id,
                                                               commit = False)

        secondary_color_01_audit_entry = crud.create.audit_entry(operation_type = model.OperationType.CREATE.value,
                                                                 auditable_entity_type = model.CLASS_TO_ENUM_MAP['Color'],
                                                                 related_entity_id = s_color_01_id,
                                                                 audit_details = db_init_message,
                                                                 created_by_user_id = bootstrap_user_id,
                                                                 commit = False)
        
        primary_color_02_audit_entry = crud.create.audit_entry(operation_type = model.OperationType.CREATE.value,
                                                               auditable_entity_type = model.CLASS_TO_ENUM_MAP['Color'],
                                                               related_entity_id = p_color_02_id,
                                                               audit_details = db_init_message,
                                                               created_by_user_id = bootstrap_user_id,
                                                               commit = False)
        
        secondary_color_02_audit_entry = crud.create.audit_entry(operation_type = model.OperationType.CREATE.value,
                                                                 auditable_entity_type = model.CLASS_TO_ENUM_MAP['Color'],
                                                                 related_entity_id = s_color_02_id,
                                                                 audit_details = db_init_message,
                                                                 created_by_user_id = bootstrap_user_id,
                                                                 commit = False)
        
        light_theme_ui_theme_audit_entry = crud.create.audit_entry(operation_type = model.OperationType.CREATE.value,
                                                                   auditable_entity_type = model.CLASS_TO_ENUM_MAP['UiTheme'],
                                                                   related_entity_id = light_ui_id,
                                                                   audit_details = db_init_message,
                                                                   created_by_user_id = bootstrap_user_id,
                                                                   commit = False)
        
        dark_theme_ui_theme_audit_entry = crud.create.audit_entry(operation_type = model.OperationType.CREATE.value,
                                                                  auditable_entity_type = model.CLASS_TO_ENUM_MAP['UiTheme'],
                                                                  related_entity_id = dark_ui_id,
                                                                  audit_details = db_init_message,
                                                                  created_by_user_id = bootstrap_user_id,
                                                                  commit = False)
        
        global_settings_audit_entry = crud.create.audit_entry(operation_type = model.OperationType.CREATE.value,
                                                              auditable_entity_type = model.CLASS_TO_ENUM_MAP['GlobalSettings'],
                                                              related_entity_hash = global_settings_fingerprint,
                                                              audit_details = db_init_message,
                                                              created_by_user_id = bootstrap_user_id,
                                                              commit = False)
        
        bootstrap_user_settings_audit_entry = crud.create.audit_entry(operation_type = model.OperationType.CREATE.value,
                                                                      auditable_entity_type = model.CLASS_TO_ENUM_MAP['UserSettings'],
                                                                      related_entity_id = bootstrap_user_settings_id,
                                                                      audit_details = db_init_message,
                                                                      created_by_user_id = bootstrap_user_id,
                                                                      commit = False)
        
        bootstrap_user_audit_entry = crud.create.audit_entry(operation_type = model.OperationType.CREATE.value,
                                                             auditable_entity_type = model.CLASS_TO_ENUM_MAP['User'],
                                                             related_entity_id = bootstrap_user_id,
                                                             audit_details = db_init_message,
                                                             created_by_user_id = bootstrap_user_id,
                                                             commit = False)
        
        
        model.db.session.add(primary_color_01_audit_entry)
        model.db.session.add(secondary_color_01_audit_entry)
        model.db.session.add(primary_color_02_audit_entry)
        model.db.session.add(secondary_color_02_audit_entry)
        model.db.session.add(light_theme_ui_theme_audit_entry)
        model.db.session.add(dark_theme_ui_theme_audit_entry)
        model.db.session.add(global_settings_audit_entry)
        model.db.session.add(bootstrap_user_settings_audit_entry)
        model.db.session.add(bootstrap_user_audit_entry)

        model.db.session.commit()

        utils.successMessage()

    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)



def populate_timezones():
    try:
        # Open and load the JSON file
        with open('data/timezones.json', 'r') as file:
            timezones = json.load(file)
        
        # Iterate over each timezone in the JSON file
        for timezone in timezones:
            tz = crud.create.timezone(id=timezone['id'],
                                      identifier=timezone['identifier'],
                                      abbreviation=timezone['abbreviation'],
                                      utc_offset_minutes=timezone['utc_offset_minutes'],
                                      has_dst=timezone['has_dst'],
                                      commit=False)
            
            model.db.session.add(tz)
        
        model.db.session.commit()
        utils.successMessage()
        
    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)


def populate_countries():
    try:
        # Open and load the JSON file
        with open('data/countries.json', 'r') as file:
            countries = json.load(file)

        
        # Iterate over each country in the JSON file
        for country in countries:
            entry = crud.create.country(id=country['id'],
                                        code=country['code'],
                                        intl_phone_code=country['intl_phone_code'],
                                        name=country['name'],
                                        commit=False)
            
            model.db.session.add(entry)
        
        model.db.session.commit()
        utils.successMessage()
        
    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)


def populate_states():
    # Read the JSON data
    with open('data/states.json', 'r') as file:
        states_data = json.load(file)

    try:
        
        for state in states_data:
            state_entry = crud.create.state(code=state["code"],
                                            name=state["name"],
                                            timezone_id=state["timezone_id"],
                                            country_id=state["country_id"],
                                            commit=False)
            
            model.db.session.add(state_entry)

        model.db.session.commit()
        utils.successMessage()

    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)


def populate_currencies():
    try:
        # Open and load the JSON file
        with open('data/currencies.json', 'r') as file:
            currencies = json.load(file)
        
        # Iterate over each currency in the JSON file
        for currency in currencies:
            entry = crud.create.currency(id=currency['id'],
                                         name=currency['name'],
                                         symbol=currency['symbol'],
                                         iso_code=currency['iso_code'],
                                         exchange_rate=currency['exchange_rate'],
                                         commit=False)

            model.db.session.add(entry)
        
        model.db.session.commit()
        utils.successMessage()
        
    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)


def generate_deployment_fingerprint(input_data=None):
    if input_data is None:
        input_data = os.urandom(32)  # Generate 32 random bytes if no data is provided
    elif isinstance(input_data, str):
        input_data = input_data.encode()  # Encode only if it's a string

    fingerprint = hashlib.sha256(input_data).hexdigest()  # Generate SHA-256 hash
    utils.successMessage()
    return fingerprint



def populate_permissions(created_by_user_id=0):
    try:
        # Open and load the default_permissions.json file
        with open('data/default_permissions.json', 'r') as file:
            permissions_data = json.load(file)["default_permissions"]

            print(f"{utils.YELLOW_BOLD}Permissions Data: {utils.RESET}{permissions_data}\n")  #DEBUG

        # permission_id_mapping dictionary to store permission name and its corresponding ID
        permission_id_mapping = {}

        # Iterate over each category of permissions in the JSON
        for category, permissions in permissions_data.items():
            for permission in permissions:
                # Create the permission using crud.py's function
                new_permission, _ = crud.create.permission(name=permission["permission"],
                                                           description=permission["description"],
                                                           created_by_user_id=created_by_user_id,
                                                           audit_details=f"Seeding permission: {permission['permission']}",
                                                           commit=False)

                
                # Adding the created permission's ID to the permission_id_mapping
                permission_id_mapping[permission["permission"]] = new_permission.id
                model.db.session.add(new_permission)

        # Commit all the permissions at once
        model.db.session.commit()
        print(f"{utils.YELLOW}Permission ID Mapping: {utils.RESET}{permission_id_mapping}\n")  # DEBUG
        utils.successMessage()

        # Return the permission_id_mapping to be used elsewhere if needed
        return permission_id_mapping
        
    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)
        return {}
    

def populate_roles(created_by_user_id=0,
                   permission_id_mapping={}):
    try:
        # Open and load the default_roles.json file
        with open('data/default_roles.json', 'r') as file:
            roles_data = json.load(file)["default_roles"]
        
        # role_id_mapping dictionary to store role name and its corresponding ID
        role_id_mapping = {}

        # Iterate over each role in the JSON
        for role in roles_data:
            # Create the role using crud.py's function
            new_role, _ = crud.create.role(name=role["name"],
                                           description=role["description"],
                                           created_by_user_id=created_by_user_id,
                                           audit_details=f"Seeding role: {role['name']}",
                                           commit=False)

            # Flush to get the, now created, id for this entity
            model.db.session.flush()

            # Assigning permissions to the role
            for permission_code in role["permissions"]:
                permission_id = permission_id_mapping.get(permission_code)
                print(f"\nTrying to assign permission {utils.YELLOW}{permission_code}{utils.RESET} to role {utils.BLUE}{role['name']}{utils.RESET}") #  DEBUG
                if permission_id:
                    print(f"Assigning permission {utils.GREEN}{permission_code}{utils.RESET} to role {utils.BLUE}{role['name']}{utils.RESET}\n\n")  #  DEBUG
                    crud.create.role_permission(role_id=new_role.id,
                                                permission_id=permission_id,
                                                created_by_user_id=created_by_user_id,
                                                audit_details=f"\n\n {utils.YELLOW}Assigning permission {permission_code}{utils.RESET} to role {utils.BLUE}{role['name']}{utils.RESET}\n\n",
                                                commit=False)
                else:                                                  # DEBUG
                    print(f"Permission {utils.YELLOW}{permission_code} {utils.RED_BOLD}not found{utils.RESET}\n\n")   # DEBUG

            
            # Adding the created role's ID to the role_id_mapping
            role_id_mapping[role["name"]] = new_role.id
            model.db.session.add(new_role)

        # Commit all the roles and role-permissions at once
        model.db.session.commit()
        utils.successMessage()

        return role_id_mapping
        
    except Exception as e:
        model.db.session.rollback()
        utils.errorMessage(e)
        return {}




def populate_user_roles(number_of_users_to_generate,
                        audit_details):
    try:

        # Assign Account Owner
        crud.create.user_role(user_id=1,
                              role_id=1,
                              created_by_user_id=0,
                              audit_details="Account Owner Creation",
                              commit=True)

        for user_id in range(2, number_of_users_to_generate + 1):
            role_id = random.randint(2, 11)
            created_by_user_id = random.randint(1, number_of_users_to_generate)
            audit_details = audit_details

            crud.create.user_role(user_id=user_id,
                                  role_id=role_id,
                                  created_by_user_id=created_by_user_id,
                                  audit_details=audit_details,
                                  commit=True)
        
        utils.successMessage()
    
    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)




def populate_users(number_of_users_to_generate):
    first_names = ["John", "Jane", "Alice", "Bob", "Emily", "Tom", "Lucy", "Mark", "Sophia", "Jack"]
    last_names = ["Doe", "Smith", "Brown", "Williams", "Jones", "Davis", "Garcia", "Miller", "Wilson", "Anderson"]
    all_names = list(product(first_names, last_names))
    area_codes = [479, 501, 870, 212, 305, 415, 713, 802, 907, 808]  # Replace with actual area codes if needed

    audit_detail = "Created in user loop."

    # Initial Account Owner = id 1
    _, _, _, _ = crud.create.user("password",
                                  first_name="Big",
                                  last_name="Boss",
                                  currency_id=1,
                                  created_by_user_id=0,
                                  time_format_is_24h=False,
                                  audit_details="One off Account Owner",
                                  ui_theme_id=2,
                                  nickname="Bossman",
                                  nickname_preferred=True)

    try:
        for i in range(number_of_users_to_generate):
            if len(all_names) == 0:
                break
            
            creator_id = i + 1

            first_name, last_name = random.choice(all_names)
            all_names.remove((first_name, last_name))

            area_code = random.choice(area_codes)
            phone_number = random.randint(1000000, 9999999)
            email = f"{first_name.lower()}.{last_name.lower()}@gmail.com"

            user, _, _, _ = crud.create.user("password",
                                             first_name,
                                             last_name,
                                             1,
                                             creator_id,
                                             False,
                                             audit_detail,
                                             2
                                             )
            
            _, _ = crud.create.phone_number(model.PhoneableEntityTypes.USER.value,
                                            user.id,
                                            model.PhoneType.PERSONAL.value,
                                            True,
                                            1,
                                            area_code,
                                            phone_number,
                                            creator_id,
                                            audit_detail
                                            )
            
            _, _ = crud.create.email_address(model.EmailableEntityTypes.USER.value,
                                             user.id,
                                             model.PhoneType.PERSONAL.value,
                                             email,
                                             creator_id,
                                             audit_detail
                                             )
            
        utils.successMessage()

    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)



def populate_categories(created_by_user_id: int = 0):
    try:
        with open('data/default_categories.json', 'r') as file:
            data = json.load(file)["Default Categories"]
        
        color_id_mapping = {}
        category_id_mapping = {}
        category_parent_mapping = {}
        
        def process_category(category_data, parent_category_name=None, parent_category_id=None):
            color_name = category_data["color_name"]
            color_hex_value = category_data["color_hex_value"]

            if color_name not in color_id_mapping:
                new_color, _ = crud.create.color(name=color_name,
                                                 hex_value=color_hex_value,
                                                 created_by_user_id=created_by_user_id,
                                                 audit_details=f"Seeding color: {color_name}",
                                                 commit=False)
                model.db.session.flush()
                color_id_mapping[color_name] = new_color.id

            color_id = color_id_mapping[color_name]

            if parent_category_id is None:
                print(f"Root category: {utils.BLUE}{category_data['name']}{utils.RESET}")  # DEBUG
            
            new_category, _ = crud.create.category(name=category_data["name"],
                                                   color_id=color_id,
                                                   parent_category_id=parent_category_id,
                                                   created_by_user_id=created_by_user_id,
                                                   audit_details=f"Seeding category: {category_data['name']}",
                                                   commit=False)
            model.db.session.flush()
            category_id_mapping[category_data["name"]] = new_category.id
            category_parent_mapping[(parent_category_name, category_data["name"])] = new_category.id
            
            for subcategory_name, subcategory_data in category_data.items():
                if subcategory_name not in ["name", "color_name", "color_hex_value"]:
                    print(f"\nTrying to assign subcategory {utils.YELLOW}{subcategory_name}{utils.RESET} to category {utils.BLUE}{category_data['name']}{utils.RESET}")  #  DEBUG
                    process_category(subcategory_data, category_data["name"], new_category.id)
                    print(f"Assigning subcategory {utils.GREEN}{subcategory_name}{utils.RESET} to category {utils.BLUE}{category_data['name']}{utils.RESET}\n")  #  DEBUG
                else:
                    print(f"Field {utils.YELLOW}{subcategory_name}{utils.RESET} is not a subcategory")  # DEBUG
        
        for category_name, category_data in data.items():
            process_category(category_data)

        utils.successMessage
        # print(f"{utils.GREEN_BOLD}{category_id_mapping}{utils.RESET}")
        # print(f"{utils.GREEN_BOLD}{category_parent_mapping}{utils.RESET}")
        model.db.session.commit()
        return category_id_mapping, category_parent_mapping

    except Exception as e:
        model.db.session.rollback()
        utils.errorMessage(e)



def populate_assets(created_by_user_id: int = 0,
                    image_population: bool = False):
    try:
        # Create an initial "Unknown" manufacturer
        unknown_manufacturer, _ = crud.create.manufacturer(name="Unknown",
                                                        created_by_user_id=created_by_user_id,
                                                        audit_details=db_init_message,
                                                        commit=False)
        model.db.session.flush()
        unknown_manufacturer_id = unknown_manufacturer.id

        with open('data/Cheqroom_Item_Export-2023-08-12 21_06_57.json', 'r') as file:
            data = json.load(file)

        downloaded_images = set()

        for item in data:
            # Create Manufacturer and Flush to get ID
            manufacturer_name = utils.sanitize_name(item.get("Manufacturer") or item.get("Brand"))
            existing_manufacturer = crud.read.Manufacturer.by_name(name=manufacturer_name)

            if existing_manufacturer:
                manufacturer_id = existing_manufacturer.id
            else:
                if manufacturer_name:
                    manufacturer, _ = crud.create.manufacturer(name=manufacturer_name,
                                                            created_by_user_id=created_by_user_id,
                                                            audit_details=db_init_message,
                                                            commit=False)
                    model.db.session.flush()
                    manufacturer_id = manufacturer.id
                else:
                    manufacturer_id = unknown_manufacturer_id

            # Create Financial Entries and Flush to get IDs
            purchase_price_id = msrp_id = residual_value_id = None

            if item.get("Purchase Price"):
                purchase_price, _ = crud.create.financial_entry(1,
                                                                float(item["Purchase Price"]),
                                                                created_by_user_id,
                                                                db_init_message,
                                                                commit = False)
                model.db.session.flush()
                purchase_price_id = purchase_price.id

            if item.get("MSRP"):
                msrp, _ = crud.create.financial_entry(1,
                                                      float(item["MSRP"]),
                                                      created_by_user_id,
                                                      db_init_message,
                                                      commit = False)
                model.db.session.flush()
                msrp_id = msrp.id

            if item.get("Residual Value"):
                residual_value, _ = crud.create.financial_entry(1,
                                                                float(item["Residual Value"]),
                                                                created_by_user_id,
                                                                db_init_message,
                                                                commit = False)
                model.db.session.flush()
                residual_value_id = residual_value.id

            # Prepare fields for Asset creation

            model_name = item.get("Name")
            model_number = item.get("Model")
            inventory_number = int(item.get("Item Number") or 1)
            online_item_page = item.get("Hyperlink")
            description = item.get("Description")
            category_id_str = item.get("category_id")
            if category_id_str == "Uncategorized" or category_id_str is None:
                category_id = 1
            else:
                try:
                    category_id = int(category_id_str)
                except ValueError:
                    category_id = 1


            # Create Asset
            asset, _ = crud.create.asset(manufacturer_id,
                                         model_name,
                                         inventory_number,
                                         created_by_user_id,
                                         model_number = model_number,
                                         category_id = category_id,
                                         purchase_price_id = purchase_price_id,
                                         msrp_id = msrp_id,
                                         residual_value_id = residual_value_id,
                                         online_item_page = online_item_page,
                                         description = description,
                                         audit_details = db_init_message,
                                         commit = False)

            # Create asset_location_log
            geo_value = item.get("Geo", None)
            if geo_value:
                latitude, longitude = map(float, geo_value.split(", "))
                crud.create.asset_location_log(asset.id,
                                            latitude,
                                            longitude,
                                            created_by_user_id,
                                            db_init_message,
                                            commit=False)
                

            if image_population:
                model.db.session.flush()
                asset_id = asset.id

                # Get the image from the JSON entry
                image_to_downloaded = item.get("Image Url")

                # Check that there's somthing there
                if image_to_downloaded:

                    # Check if it's already been downloaded
                    if model_name not in downloaded_images:
                        image = utils.ImageURLScaping.download_image(image_to_downloaded)
                        print(f"Image for {utils.UNDERLINED}{model_name}{utils.RESET} has been {utils.GREEN_BOLD}downloaded{utils.RESET}.")

                        raw_image_output = "/home/dj/src/PARM-Production_Asset_Reservation_Manager/database/data/raw_images"
                        processed_image_output = "/home/dj/src/PARM-Production_Asset_Reservation_Manager/database/data/processed_images"


                        # Loop through image_size_map
                        for label, max_size in utils.ImageProcessing.image_size_map.items():
                            output_path, image_size = utils.ImageProcessing.generate_single_image_variation(image,
                                                                                                            raw_image_output,
                                                                                                            processed_image_output,
                                                                                                            model_name,
                                                                                                            label,
                                                                                                            max_size)

                            crud.create.file_attachment(model.AttachableEntityTypes.ASSET.value,
                                                        asset_id,
                                                        output_path,
                                                        model.FileType.JPEG.value,
                                                        model.FileCategory.IMAGE.value,
                                                        created_by_user_id,
                                                        db_init_message,
                                                        image_size = image_size,
                                                        commit=False)
        
                        print(f"Images for {utils.UNDERLINED}{model_name}{utils.RESET}'s sizes have been {utils.GREEN_BOLD}created{utils.RESET}.")
                        downloaded_images.add(model_name)

                    else:
                        print(f"Image for {utils.UNDERLINED}{model_name}{utils.RESET} has been already been downloaded and is being {utils.YELLOW_BOLD}skipped{utils.RESET}.")

                

        
        utils.successMessage()
        model.db.session.commit()

    except Exception as e:
        model.db.session.rollback()
        utils.errorMessage(e)





def main(image_population=False):
    utils.openingText(program_name, version_number)

    populate_timezones()

    populate_currencies()

    populate_countries()

    populate_states()


    primary_color_01 , secondary_color_01, primary_color_02, secondary_color_02 = populate_initial_colors()

    light_theme, dark_theme = populate_initial_ui_themes(primary_color_01.id, secondary_color_01.id, primary_color_02.id, secondary_color_02.id)

    global_settings = populate_initial_global_settings()

    bootstrap_user, bootstrap_user_settings = populate_boostrap_user("password",
                                                                     "Admin",
                                                                     "Administrator",
                                                                     global_settings.default_currency_id,
                                                                     time_format_is_24h=False,
                                                                     ui_theme_id=light_theme.id,
                                                                     last_login=datetime.utcnow())
    

    populate_bootstrap_audit_entries(primary_color_01.id,
                                     secondary_color_01.id,
                                     primary_color_02.id,
                                     secondary_color_02.id,
                                     light_theme.id,
                                     dark_theme.id,
                                     global_settings.deployment_fingerprint,
                                     bootstrap_user_settings.id,
                                     bootstrap_user.id)


    populate_users(number_of_users_to_generate)

    permission_mapping = populate_permissions()
    populate_roles(permission_id_mapping=permission_mapping)

    populate_user_roles(number_of_users_to_generate, db_init_message)

    crud.create.address("mom's hosue",
                        model.AddressType.RESIDENTIAL.value,
                        "2107 SE 9th St.",
                        "Bentonville",
                        4,
                        "72712-8000",
                        1,
                        0)
    
    category_id_mapping, category_parent_mapping = populate_categories()

    populate_assets(image_population = image_population)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the main program with optional arguments.')
    parser.add_argument('--image_population', action='store_true', help='Enable image population.')

    args = parser.parse_args()

    main(image_population=args.image_population)