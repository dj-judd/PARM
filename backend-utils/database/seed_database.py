"""Script to seed database."""

import hashlib
import os
import json
import sys
from random import choice, randint
from datetime import datetime
from sqlalchemy import text

import crud
import model
import permissions
import server

# Modify sys.path to include the parent directory
sys.path.append('..')
import utils
from utils import UNDERLINED, GREEN_BOLD, YELLOW_BOLD, RED_BOLD, RESET

# # Turn off SQL output before seeding
# model.db.engine.echo = False

# Your seeding logic here...

# # Optionally turn on SQL output after seeding
# model.engine.echo = True


version_number = 0.2
program_name = "PARM Database Seeder 3,000,000"

db_init_message = "Generated automatically upon database creation."


# Drop and create database
os.system('dropdb parm')
os.system('createdb parm')


# Execute SQL script on the database
os.system('psql -d parm < PARM-Schema.sql')

model.connect_to_db(server.app)
model.db.create_all()




def populate_initial_colors():
    try:

        primary_color_01 = crud.create_color("Paper White | Default",
                                  "#f0eae7",
                                  audit=False,
                                  commit=False
                                  )
        
        secondary_color_01 = crud.create_color("Sky Blue | Default",
                                  "17baeb",
                                  audit=False,
                                  commit=False
                                  )
        

        primary_color_02 = crud.create_color("Dark Gray | Default",
                                  "#0f0d12",
                                  audit=False,
                                  commit=False
                                  )
        
        secondary_color_02 = crud.create_color("Hot Red | Default",
                                  "#eb315d",
                                  audit=False,
                                  commit=False
                                  )        
        

        model.db.session.commit()
        utils.successMessage()

        return primary_color_01, secondary_color_01, primary_color_02, secondary_color_02

    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)



def populate_initial_ui_themes(primary_color_01_id, secondary_color_01_id, primary_color_02_id, secondary_color_02_id):
    try:

        light_ui_theme = crud.create_ui_theme("Light Theme",
                                        "Clean & Cultured",
                                        primary_color_01_id,
                                        secondary_color_01_id,
                                        audit=False,
                                        commit=False
                                        )
        
        dark_ui_theme = crud.create_ui_theme("Dark Theme",
                                        "Cyberpunk Styling",
                                        primary_color_02_id,
                                        secondary_color_02_id,
                                        audit=False,
                                        commit=False
                                        )

        model.db.session.commit()
        utils.successMessage()

        return light_ui_theme, dark_ui_theme

    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)



def populate_initial_global_settings(deployment_fingerprint=None,
                                     default_currency_id=1
                                     ):
    try:

        if deployment_fingerprint is None:
            deployment_fingerprint = generate_deployment_fingerprint() 
        else:
            deployment_fingerprint = generate_deployment_fingerprint(deployment_fingerprint)

        global_settings = crud.create_global_settings(deployment_fingerprint=deployment_fingerprint,
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
                           last_login=None,
                           ):
    try:

        bootstrap_user, bootstrap_user_settings = crud.create_bootstrap_user(id=0,
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
                                     bootstrap_user_id
                                     ):
    try:
        primary_color_01_audit_entry = crud.create_audit_entry(operation_type = model.OperationType.CREATE.value,
                                                               auditable_entity_type = model.CLASS_TO_ENUM_MAP['Color'],
                                                               related_entity_id = p_color_01_id,
                                                               details = db_init_message,
                                                               created_by_user_id = bootstrap_user_id,
                                                               commit = False
                                                               )

        secondary_color_01_audit_entry = crud.create_audit_entry(operation_type = model.OperationType.CREATE.value,
                                                                 auditable_entity_type = model.CLASS_TO_ENUM_MAP['Color'],
                                                                 related_entity_id = s_color_01_id,
                                                                 details = db_init_message,
                                                                 created_by_user_id = bootstrap_user_id,
                                                                 commit = False
                                                                 )
        
        primary_color_02_audit_entry = crud.create_audit_entry(operation_type = model.OperationType.CREATE.value,
                                                               auditable_entity_type = model.CLASS_TO_ENUM_MAP['Color'],
                                                               related_entity_id = p_color_02_id,
                                                               details = db_init_message,
                                                               created_by_user_id = bootstrap_user_id,
                                                               commit = False
                                                               )
        
        secondary_color_02_audit_entry = crud.create_audit_entry(operation_type = model.OperationType.CREATE.value,
                                                                 auditable_entity_type = model.CLASS_TO_ENUM_MAP['Color'],
                                                                 related_entity_id = s_color_02_id,
                                                                 details = db_init_message,
                                                                 created_by_user_id = bootstrap_user_id,
                                                                 commit = False
                                                                 )
        
        light_theme_ui_theme_audit_entry = crud.create_audit_entry(operation_type = model.OperationType.CREATE.value,
                                                                   auditable_entity_type = model.CLASS_TO_ENUM_MAP['UiTheme'],
                                                                   related_entity_id = light_ui_id,
                                                                   details = db_init_message,
                                                                   created_by_user_id = bootstrap_user_id,
                                                                   commit = False
                                                                   )
        
        dark_theme_ui_theme_audit_entry = crud.create_audit_entry(operation_type = model.OperationType.CREATE.value,
                                                                  auditable_entity_type = model.CLASS_TO_ENUM_MAP['UiTheme'],
                                                                  related_entity_id = dark_ui_id,
                                                                  details = db_init_message,
                                                                  created_by_user_id = bootstrap_user_id,
                                                                  commit = False
                                                                  )
        
        global_settings_audit_entry = crud.create_audit_entry(operation_type = model.OperationType.CREATE.value,
                                                              auditable_entity_type = model.CLASS_TO_ENUM_MAP['GlobalSettings'],
                                                              related_entity_hash = global_settings_fingerprint,
                                                              details = db_init_message,
                                                              created_by_user_id = bootstrap_user_id,
                                                              commit = False
                                                              )
        
        bootstrap_user_settings_audit_entry = crud.create_audit_entry(operation_type = model.OperationType.CREATE.value,
                                                                      auditable_entity_type = model.CLASS_TO_ENUM_MAP['UserSettings'],
                                                                      related_entity_id = bootstrap_user_settings_id,
                                                                      details = db_init_message,
                                                                      created_by_user_id = bootstrap_user_id,
                                                                      commit = False
                                                                      )
        
        bootstrap_user_audit_entry = crud.create_audit_entry(operation_type = model.OperationType.CREATE.value,
                                                             auditable_entity_type = model.CLASS_TO_ENUM_MAP['User'],
                                                             related_entity_id = bootstrap_user_id,
                                                             details = db_init_message,
                                                             created_by_user_id = bootstrap_user_id,
                                                             commit = False
                                                             )
        
        
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
            tz = crud.create_timezone_entry(
                id=timezone['id'],
                identifier=timezone['identifier'],
                abbreviation=timezone['abbreviation'],
                utc_offset_minutes=timezone['utc_offset_minutes'],
                has_dst=timezone['has_dst'],
                commit=False
            )
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
            entry = crud.create_country_entry(
                id=country['id'],
                code=country['code'],
                intl_phone_code=country['intl_phone_code'],
                name=country['name'],
                commit=False
            )
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
            state_entry = crud.create_state_entry(
                code=state["code"],
                name=state["name"],
                timezone_id=state["timezone_id"],
                country_id=state["country_id"],
                commit=False
            )
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
            entry = crud.create_currency_entry(
                id=currency['id'],
                name=currency['name'],
                symbol=currency['symbol'],
                iso_code=currency['iso_code'],
                exchange_rate=currency['exchange_rate'],
                commit=False
            )
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
        
        # permission_id_mapping dictionary to store permission name and its corresponding ID
        permission_id_mapping = {}

        # Iterate over each category of permissions in the JSON
        for category, permissions in permissions_data.items():
            for permission in permissions:
                # Create the permission using crud.py's function
                new_permission, _ = crud.create_permission(
                    name=permission["permission"],
                    description=permission["description"],
                    created_by_user_id=created_by_user_id,
                    audit_details=f"Seeding permission: {permission['permission']}",
                    commit=False
                )

                
                # Adding the created permission's ID to the permission_id_mapping
                permission_id_mapping[permission["permission"]] = new_permission.id
                model.db.session.add(new_permission)

        # Commit all the permissions at once
        model.db.session.commit()
        utils.successMessage()

        # Return the permission_id_mapping to be used elsewhere if needed
        return permission_id_mapping
        
    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)
        return {}
    

def populate_roles(created_by_user_id=0, permission_id_mapping={}):
    try:
        # Open and load the default_roles.json file
        with open('data/default_roles.json', 'r') as file:
            roles_data = json.load(file)["default_roles"]
        
        # role_id_mapping dictionary to store role name and its corresponding ID
        role_id_mapping = {}

        # Iterate over each role in the JSON
        for role in roles_data:
            # Create the role using crud.py's function
            new_role, _ = crud.create_role(
                name=role["name"],
                description=role["description"],
                created_by_user_id=created_by_user_id,
                audit_details=f"Seeding role: {role['name']}",
                commit=False
            )

            # Flush to get the, now created, id for this entity
            model.db.session.flush()

            # Assigning permissions to the role
            for permission_code in role["permissions"]:
                permission_id = permission_id_mapping.get(permission_code)
                if permission_id:
                    crud.create_role_permission(
                        role_id=new_role.id,
                        permission_id=permission_id,
                        created_by_user_id=created_by_user_id,
                        audit_details=f"Assigning permission {permission_code} to role {role['name']}",
                        commit=False
                    )

            
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







def populate_users():

    try:

        crud.create_user("password",
                         "John",
                         "Doe",
                         1,
                         0,
                         False,
                         "1st Normal User after Bootstrap",
                         2,
                         None,
                         None,
                         None,
                         None,
                         commit=True,
                         )

        pass

    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)





def main():
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


    populate_users()

    permission_mapping = populate_permissions()
    populate_roles(permission_id_mapping=permission_mapping)

    # TODO: Create 10 Reservations for each user
    # for n in range(10):

    # return


if __name__ == "__main__":
    main()