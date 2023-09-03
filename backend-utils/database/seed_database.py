"""Script to seed database."""

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

init_message = "This was generated automatically when database was seeded."


# Drop and create database
os.system('dropdb parm')
os.system('createdb parm')


# Execute SQL script on the database
os.system('psql -d parm < PARM-Schema.sql')

model.connect_to_db(server.app)
model.db.create_all()



from model import db


def insert_bootstrap_user(password_hash, first_name, last_name, user_settings_id, last_login, audit_info_entry_id):
    # Alter table to set column as nullable
    alter_sql_1 = """ALTER TABLE users ALTER COLUMN audit_info_entry_id DROP NOT NULL;"""
    db.session.execute(alter_sql_1)
    db.session.commit()

    # Inserting the bootstrap user
    insert_sql = text("""
        INSERT INTO users 
        (password_hash, first_name, last_name, user_settings_id, last_login, audit_info_entry_id) 
        VALUES (:password_hash, :first_name, :last_name, :user_settings_id, :last_login, :audit_info_entry_id)
        """)

    db.session.execute(insert_sql, {
        "password_hash": password_hash,
        "first_name": first_name,
        "last_name": last_name,
        "user_settings_id": user_settings_id,
        "last_login": last_login,
        "audit_info_entry_id": audit_info_entry_id
    })

    bootstrap_user_id = result.fetchone()[0]

    db.session.commit()

    # Alter table to set column as NOT NULL again
    alter_sql_2 = """ALTER TABLE users ALTER COLUMN audit_info_entry_id SET NOT NULL;"""
    db.session.execute(alter_sql_2)
    db.session.commit()

    return bootstrap_user_id



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
        with open('countries.json', 'r') as file:
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
        with open('currencies.json', 'r') as file:
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
        print(f"\n{RED_BOLD}Error occurred!{RESET}\nseed_database.py\n{UNDERLINED}Line 158{RESET}\n{e}")




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
            # Initial creation of user to create all other data and users
    insert_bootstrap_user('fire', 'Prometheus', 'Admin', 1, datetime.utcnow(), 1)


    db_creator = bootstrap_user.id
    crud.create_user(password_hash="password",
                    first_name="John",
                    last_name="Doe",
                    currency_id=1,
                    time_format_is_24=True,
                    created_by_user_id=db_creator,
                    details=init_message,
                    commit=True)

    #     db_movie = crud.create_movie(title, overview, release_date, poster_path)
    #     movies_in_db.append(db_movie)
        
    # model.db.session.add_all(movies_in_db)
    # model.db.session.commit()



    
    populate_timezones()

    populate_countries()

    populate_states()
    
    populate_currencies()

    # Initial creation of user to create all other data and users
    db_creator = insert_bootstrap_user('fire', 'Prometheus', 'Admin', 1, datetime.utcnow(), 1)

    crud.create_user(password_hash="password",
                    first_name="John",
                    last_name="Doe",
                    currency_id=1,
                    time_format_is_24=True,
                    created_by_user_id=db_creator,
                    details=init_message,
                    commit=True)

    # Generate 10 Users
    for n in range(10):

        try:
            # Begin the transaction
            model.db.session.begin()

            password_hash = 'test'
            first_name = 'bob'
            last_name = 'theBuilder'

            # TODO: Generate an email, phone number, and select user roles

            # random_creator_user = randint(1,5)
            random_creator_user = 0


            # db_user, db_user_audit_entry, db_user_setting, db_user_setting_audit_entry = crud.create_user(password_hash,
            #                                                                                                 first_name,
            #                                                                                                 last_name,
            #                                                                                                 random_creator_user,
            #                                                                                                 currency_id = 0,
            #                                                                                                 details = seeded_message,
            #                                                                                                 commit = False)
            

            db_user, db_user_audit_entry, db_user_setting, db_user_setting_audit_entry = crud.create_user(password_hash,
                                                                                              first_name,
                                                                                              last_name,
                                                                                              currency_id=0,
                                                                                              time_format_is_24=True,  # or False, based on your needs
                                                                                              created_by_user_id=random_creator_user,
                                                                                              details=init_message,
                                                                                              commit=False)


            model.db.session.add(db_user_audit_entry)
            model.db.session.add(db_user_setting_audit_entry)
            model.db.session.add(db_user_setting)
            model.db.session.add(db_user)

            # TODO: Create 10 Reservations for each user
            # for n in range(10):

            # Commit all at once
            model.db.session.commit()


        except Exception as e:
            # If any error occurs, rollback the changes
            model.db.session.rollback()
            print(f"\n{RED_BOLD}Error occurred!{RESET}\nseed_database.py\n{UNDERLINED}Line 238{RESET}\n{e}")




if __name__ == "__main__":
    main()