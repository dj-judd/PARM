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
        "created_by": 0,
        "created_at": datetime.utcnow(),
        "last_edited_by": 0,
        "last_edited_at": datetime.utcnow(),
        "is_archived": False,
        "archived_at": None
    })

    prime_audit_entry_id = result.fetchone()[0]
    db.session.commit()

    # Adjust the sequence immediately after inserting the bootstrap audit info entry
    sequence_name = "audit_info_entries_id_seq"
    db.session.execute(f"SELECT setval('{sequence_name}', 1, true);")
    db.session.commit()

    return prime_audit_entry_id


def insert_bootstrap_user(prime_audit_entry_id, password_hash, first_name, last_name, last_login):
    # Step 1: Set User Settings audit requirements off
    db.session.execute("ALTER TABLE user_settings ALTER COLUMN audit_info_entry_id DROP NOT NULL;")
    db.session.commit()

    # Step 2: Inserting the bootstrap user_setting
    insert_sql_for_user_setting = text("""
        INSERT INTO user_settings 
        (id, audit_info_entry_id) 
        VALUES (:id, :audit_info_entry_id)
        RETURNING id
        """)

    result = db.session.execute(insert_sql_for_user_setting, {
        "id": 0,
        "audit_info_entry_id": prime_audit_entry_id
    })

    user_settings_id = result.fetchone()[0]
    db.session.commit()

    # Adjust the sequence immediately after inserting the bootstrap user setting
    sequence_name = "user_settings_id_seq"
    db.session.execute(f"SELECT setval('{sequence_name}', 1, true);")
    db.session.commit()

    # Step 3: Set Users audit requirement off
    db.session.execute("ALTER TABLE users ALTER COLUMN audit_info_entry_id DROP NOT NULL;")
    db.session.commit()

    # Step 4: Inserting the bootstrap user
    insert_sql_for_user = text("""
        INSERT INTO users 
        (id, password_hash, first_name, last_name, user_settings_id, last_login, audit_info_entry_id) 
        VALUES (:id, :password_hash, :first_name, :last_name, :user_settings_id, :last_login, :audit_info_entry_id)
        """)

    db.session.execute(insert_sql_for_user, {
        "id":0,
        "password_hash": password_hash,
        "first_name": first_name,
        "last_name": last_name,
        "user_settings_id": user_settings_id,
        "last_login": last_login,
        "audit_info_entry_id": prime_audit_entry_id
    })

    prime_user_id = result.fetchone()[0]
    db.session.commit()

    # Adjust the sequence immediately after inserting the bootstrap user
    sequence_name = "users_id_seq"
    db.session.execute(f"SELECT setval('{sequence_name}', 1, true);")
    db.session.commit()

    # Step 5: Alter users table's audit requirement back to on
    db.session.execute("ALTER TABLE users ALTER COLUMN audit_info_entry_id SET NOT NULL;")
    db.session.commit()

    return prime_user_id

def main_bootstrap(password_hash="password", first_name="Admin", last_name="Admin", last_login=datetime.utcnow()):

    # Step 1: We create the initial Bootstrap Audit Entry and get it's ID
    prime_audit_entry_id = insert_bootstrap_audit_entry()

    # Step 2: We create the initial Bootstrap User and pass it the Bootstrap Audit Entry
    prime_user_id = insert_bootstrap_user(prime_audit_entry_id, password_hash=password_hash, first_name=first_name, last_name=last_name, last_login=last_login)

    # At this point, the Bootstrap User should have ID 0
    # Step 3: Now, we update the Bootstrap Audit Entry to reference the correct User ID
    update_sql = text("""
        UPDATE audit_info_entries 
        SET created_by = :user_id, last_edited_by = :user_id
        WHERE id = :audit_entry_id
        """)

    db.session.execute(update_sql, {
        "user_id": 0,
        "audit_entry_id": prime_audit_entry_id
    })

    db.session.commit()

    # Step 4: We can now set the NOT NULL constraints back on the necessary columns
    db.session.execute("ALTER TABLE audit_info_entries ALTER COLUMN created_by SET NOT NULL;")
    db.session.execute("ALTER TABLE audit_info_entries ALTER COLUMN last_edited_by SET NOT NULL;")
    db.session.commit()

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
        
    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        print(f"\n{RED_BOLD}Error occurred!{RESET}\nseed_database.py\n{UNDERLINED}Line 73{RESET}\n{e}")


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
        
    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        print(f"\n{RED_BOLD}Error occurred!{RESET}\nseed_database.py\n{UNDERLINED}Line 102{RESET}\n{e}")


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

    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        print(f"\n{RED_BOLD}Error occurred!{RESET}\nseed_database.py\n{UNDERLINED}Line 167{RESET}\n{e}")


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
        
    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        print(f"\n{RED_BOLD}Error occurred!{RESET}\nseed_database.py\n{UNDERLINED}Line 162{RESET}\n{e}")


def generate_deployment_fingerprint(input_data=None):
    if input_data is None:
        input_data = os.urandom(32)  # Generate 32 random bytes if no data is provided
    elif isinstance(input_data, str):
        input_data = input_data.encode()  # Encode only if it's a string

    fingerprint = hashlib.sha256(input_data).hexdigest()  # Generate SHA-256 hash
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


    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        print(f"\n{RED_BOLD}Error occurred!{RESET}\nseed_database.py\n{UNDERLINED}Line 197{RESET}\n{e}")


def populate_users():

    # Initial creation of prime user and audit entry to create all other data and users
    prime_audit_entry_id, prime_user_id = main_bootstrap('fire', 'Prometheus', 'Admin', datetime.utcnow())

    # crud.create_user(password_hash="password",
    #                 first_name="John",
    #                 last_name="Doe",
    #                 currency_id=1,
    #                 time_format_is_24=False,
    #                 created_by_user_id=0,
    #                 details=db_init_message,
    #                 commit=True)

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





def main():
    utils.openingText(program_name, version_number)

    # with open('backend-utils/database/data/Cheqroom_Item_Export-2023-08-12 21_06_57_images_downloaded.json') as f:
    #     movie_data = json.loads(f.read())

    # Create movies, store them in list so we can use them
    # to create fake ratings later
    # movies_in_db = []
    # for movie in movie_data:
    #     # TODO: get the title, overview, and poster_path from the movie
    #     # dictionary. Then, get the release_date and convert it to a
    #     # datetime object with datetime.strptime
    #     title = movie['title']
    #     overview = movie["overview"]
    #     poster_path = movie['poster_path']

    #     # date format "2019-09-20"  so   'YYYY-MM-DD'
    #     release_date_string = movie['release_date']
    #     release_date = datetime.strptime(release_date_string, '%Y-%m-%d')



    #     # TODO: create a movie here and append it to movies_in_db
    #     # movies_in_db.append({
    #     #     'title': movie,
    #     #     'overview': overview,
    #     #     'poster_path': poster_path,
    #     #     'release_date': release_date
    #     #     })

    populate_timezones()

    populate_currencies()

    populate_countries()

    populate_states()
    
    populate_global_settings()

    populate_users()

    # TODO: Create 10 Reservations for each user
    # for n in range(10):



if __name__ == "__main__":
    main()