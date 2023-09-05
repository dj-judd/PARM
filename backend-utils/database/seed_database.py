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



from model import db


def insert_bootstrap_colors(audit_entry_id):
    insert_sql = text("""
        INSERT INTO colors 
        (name, hex_value, audit_info_entry_id) 
        VALUES (:name, :hex_value, :audit_info_entry_id)
        RETURNING id
    """)

    primary_color_id = db.session.execute(insert_sql, {
        "name": "Default Primary",
        "hex_value": "#f0eae7", # Default primary hex value
        "audit_info_entry_id": audit_entry_id
    }).fetchone()[0]

    secondary_color_id = db.session.execute(insert_sql, {
        "name": "Default Secondary",
        "hex_value": "#17baeb", # Default secondary hex value
        "audit_info_entry_id": audit_entry_id
    }).fetchone()[0]

    db.session.commit()
    
    return primary_color_id, secondary_color_id


def insert_bootstrap_ui_theme(primary_color_id, secondary_color_id, audit_entry_id):
    insert_sql = text("""
        INSERT INTO ui_themes 
        (name, description, primary_color, secondary_color, audit_info_entry_id) 
        VALUES (:name, :description, :primary_color, :secondary_color, :audit_info_entry_id)
        RETURNING id
    """)
    
    result = db.session.execute(insert_sql, {
        "name": "Default Theme",
        "description": "The default user interface theme.",
        "primary_color": primary_color_id,
        "secondary_color": secondary_color_id,
        "audit_info_entry_id": audit_entry_id
    })

    ui_theme_id = result.fetchone()[0]
    db.session.commit()

    return ui_theme_id


def insert_bootstrap_audit_entry():
    # Step 1: Set AuditEntry's user_id requirements off
    db.session.execute("ALTER TABLE audit_info_entries ALTER COLUMN created_by DROP NOT NULL;")
    db.session.execute("ALTER TABLE audit_info_entries ALTER COLUMN last_edited_by DROP NOT NULL;")
    db.session.commit()

    # Step 2: Inserting the bootstrap audit entry
    insert_sql_for_audit_entry = text("""
        INSERT INTO audit_info_entries 
        (id, operation_type, details, created_by, created_at, last_edited_by, last_edited_at, is_archived, archived_at)
        VALUES (:id, :operation_type, :details, :created_by, :created_at, :last_edited_by, :last_edited_at, :is_archived, :archived_at)
        RETURNING id
        """)

    result = db.session.execute(insert_sql_for_audit_entry, {
        "id": 0,
        "operation_type": "CREATE",
        "details": "Bootstrap entry",
        "created_by": None,
        "created_at": datetime.utcnow(),
        "last_edited_by": None,
        "last_edited_at": datetime.utcnow(),
        "is_archived": False,
        "archived_at": None
    })

    prime_audit_entry_id = result.fetchone()[0]
    db.session.commit()

    # Adjust the sequence immediately after inserting the bootstrap audit info entry
    adjust_sequence(sequence_name="audit_info_entries_id_seq", value=1)

    return prime_audit_entry_id


def insert_complete_bootstrap_user(prime_audit_entry_id, password_hash, first_name, last_name, last_login, ui_theme_id, default_currency_id):
    # Insert user_settings
    insert_sql_for_user_setting = """
        INSERT INTO user_settings 
        (id, currency_id, time_format_is_24h, ui_theme_id, audit_info_entry_id) 
        VALUES (:id, :currency_id, :time_format_is_24h, :ui_theme_id, :audit_info_entry_id)
        RETURNING id
    """

    result = db.session.execute(insert_sql_for_user_setting, {
        "id": 0,  # Explicitly setting the ID to 0
        "currency_id": default_currency_id,
        "time_format_is_24h": True,  # Default to 24hr format
        "ui_theme_id": ui_theme_id,
        "audit_info_entry_id": prime_audit_entry_id
    })

    user_settings_id = result.fetchone()[0]
    db.session.commit()

    # Adjust sequence after inserting into user_settings
    adjust_sequence(sequence_name="user_settings_id_seq", value=1)

    # Insert users
    insert_sql_for_user = text("""
        INSERT INTO users 
        (id, password_hash, first_name, last_name, user_settings_id, last_login, audit_info_entry_id) 
        VALUES (:id, :password_hash, :first_name, :last_name, :user_settings_id, :last_login, :audit_info_entry_id)
        RETURNING id
    """)

    result = db.session.execute(insert_sql_for_user, {
        "id": 0,
        "password_hash": password_hash,
        "first_name": first_name,
        "last_name": last_name,
        "user_settings_id": user_settings_id,
        "last_login": last_login,
        "audit_info_entry_id": prime_audit_entry_id
    })

    prime_user_id = result.fetchone()[0]
    db.session.commit()

    # Adjust sequence after inserting the bootstrap user
    adjust_sequence(sequence_name="users_id_seq", value=1)

    return prime_user_id


def update_audit_entry_with_user_reference(audit_entry_id, user_id):
    update_sql = text("""
        UPDATE audit_info_entries 
        SET created_by = :user_id, last_edited_by = :user_id
        WHERE id = :audit_entry_id
    """)
    
    db.session.execute(update_sql, {
        "audit_entry_id": audit_entry_id,
        "user_id": user_id
    })
    db.session.commit()


def disable_not_null_constraint(table_name, column_name):
    db.session.execute(f"ALTER TABLE {table_name} ALTER COLUMN {column_name} DROP NOT NULL;")
    db.session.commit()


def enable_not_null_constraint(table_name, column_name):
    db.session.execute(f"ALTER TABLE {table_name} ALTER COLUMN {column_name} SET NOT NULL;")
    db.session.commit()


def adjust_sequence(sequence_name, value=0):
    db.session.execute(f"SELECT setval('{sequence_name}', {value}, false);")
    db.session.commit()


def main_bootstrap(password_hash="password", first_name="Admin", last_name="Admin", last_login=datetime.utcnow(), default_currency_id=1):
    
    # Step 1: Disable the NOT NULL constraint on the created_by column
    disable_not_null_constraint("audit_info_entries", "created_by")
    
    # Create the bootstrap audit entry with ID of 0
    prime_audit_entry_id = insert_bootstrap_audit_entry()

    # Insert bootstrap colors
    primary_color_id, secondary_color_id = insert_bootstrap_colors(prime_audit_entry_id)
    
    # Insert bootstrap UI theme
    ui_theme_id = insert_bootstrap_ui_theme(primary_color_id, secondary_color_id, prime_audit_entry_id)
    
    # Continue with creating the bootstrap user
    prime_user_id = insert_complete_bootstrap_user(prime_audit_entry_id, password_hash, first_name, last_name, last_login, ui_theme_id, default_currency_id)
    update_audit_entry_with_user_reference(prime_audit_entry_id, prime_user_id)


    # Step 5: Re-enable the NOT NULL constraints
    enable_not_null_constraint("users", "audit_info_entry_id")
    enable_not_null_constraint("user_settings", "audit_info_entry_id")
    enable_not_null_constraint("colors", "audit_info_entry_id")
    enable_not_null_constraint("ui_themes", "audit_info_entry_id")
    enable_not_null_constraint("audit_info_entries", "created_by")
    enable_not_null_constraint("audit_info_entries", "last_edited_by")
    utils.successMessage()

    return prime_audit_entry_id, prime_user_id



def populate_timezones():
    try:
        # Open and load the JSON file
        with open('data/timezones.json', 'r') as file:
            timezones = json.load(file)
        
        model.db.session.begin()
        
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
        
        model.db.session.begin()
        
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
        model.db.session.begin()
        
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
        
        model.db.session.begin()
        
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



def populate_global_settings(deployment_fingerprint=None, default_currency_id=1):
    try:
        model.db.session.begin()

        if deployment_fingerprint is None:
            deployment_fingerprint = generate_deployment_fingerprint() 
        else:
            deployment_fingerprint = generate_deployment_fingerprint(deployment_fingerprint)

        crud.create_global_settings(deployment_fingerprint=deployment_fingerprint,
                                    default_currency_id=default_currency_id,
                                    commit=False)

        model.db.session.commit()
        utils.successMessage()


    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        utils.errorMessage(e)



def populate_permissions(created_by_user_id=0, audit_info_entry_id=0):
    try:
        # Open and load the default_permissions.json file
        with open('data/default_permissions.json', 'r') as file:
            permissions_data = json.load(file)["default_permissions"]
        
        model.db.session.begin()
        
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

                # Override the audit_info_entry_id to 0 to denote it was created during seeding
                new_permission.audit_info_entry_id = audit_info_entry_id
                
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
    

def populate_roles(created_by_user_id=0, audit_info_entry_id=0, permission_id_mapping={}):
    try:
        # Open and load the default_roles.json file
        with open('data/default_roles.json', 'r') as file:
            roles_data = json.load(file)["default_roles"]
        
        model.db.session.begin()
        
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


            # Override the audit_info_entry_id to 0 to denote it was created during seeding
            new_role.audit_info_entry_id = audit_info_entry_id
            
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

        global_settings_default_currency_id = crud.read_global_settings().get('default_currency_id')

        # Initial creation of prime user and audit entry to create all other data and users
        prime_audit_entry_id, prime_user_id = main_bootstrap('fire', 'Prometheus', 'Admin', datetime.utcnow(), global_settings_default_currency_id)



        crud.create_user(password_hash="password",
                        first_name="John",
                        last_name="Doe",
                        currency_id=global_settings_default_currency_id,
                        time_format_is_24h=False,
                        created_by_user_id=prime_user_id,
                        audit_details=db_init_message,
                        commit=True)
        
        crud.create_phone_number(model.PhoneType.PERSONAL.value,
                                 True,
                                 1,
                                 479,
                                 3811605,
                                 0,
                                 "Testing phone number Creation",
                                 None,
                                 is_primary=True,
                                 associated_user_id=1,
                                 commit=True)
        
        crud.create_email_address(model.EmailType.PERSONAL.value,
                                  "john.doe@gmail.com",
                                  0,
                                  audit_details="Testing email Creation",
                                  is_primary=True,
                                  associated_user_id=1,
                                  commit=True
                                  )
        



        crud.create_user(password_hash="password",
                first_name="Jane",
                last_name="Doe",
                currency_id=global_settings_default_currency_id,
                time_format_is_24h=False,
                created_by_user_id=prime_user_id,
                audit_details=db_init_message,
                commit=True)
        
        crud.create_phone_number(model.PhoneType.PERSONAL.value,
                                 True,
                                 1,
                                 234,
                                 5678910,
                                 0,
                                 "Testing phone number Creation",
                                 None,
                                 is_primary=True,
                                 associated_user_id=2,
                                 commit=True)
        
        crud.create_email_address(model.EmailType.PERSONAL.value,
                                  "john.doe@gmail.com",
                                  0,
                                  audit_details="Testing email Creation",
                                  is_primary=True,
                                  associated_user_id=2,
                                  commit=True                                  
                                  )
        



        # # Generate 10 Users
        # for n in range(10):

        #     try:
        #         # Begin the transaction
        #         model.db.session.begin()

        #         password_hash = 'test'
        #         first_name = 'bob'
        #         last_name = 'theBuilder'

        #         # TODO: Generate an email, phone number, and select user roles
        #         # crud.create_email()
        #         # crud.create_phone_number()

        #         db_user, db_user_audit_entry, db_user_setting, db_user_setting_audit_entry = crud.create_user(password_hash,
        #                                                                                           first_name,
        #                                                                                           last_name,
        #                                                                                           currency_id=1,
        #                                                                                           time_format_is_24=True,  # or False, based on your needs
        #                                                                                           created_by_user_id=prime_creator_id,
        #                                                                                           details=db_init_message,
        #                                                                                           commit=False)


        #         model.db.session.add(db_user_audit_entry)
        #         model.db.session.add(db_user_setting_audit_entry)
        #         model.db.session.add(db_user_setting)
        #         model.db.session.add(db_user)

        #         # Commit all at once
        #         model.db.session.commit()


        #     except Exception as e:
        #         # If any error occurs, rollback the changes
        #         model.db.session.rollback()
        #         print(f"\n{RED_BOLD}Error occurred!{RESET}\nseed_database.py\n{UNDERLINED}Line 238{RESET}\n{e}")
        model.db.session.commit()

        
        utils.successMessage()

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
    
    populate_global_settings()

    populate_users()

    permission_mapping = populate_permissions()
    populate_roles(permission_id_mapping=permission_mapping)

    # TODO: Create 10 Reservations for each user
    # for n in range(10):



if __name__ == "__main__":
    main()