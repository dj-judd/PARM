"""Script to seed database."""

import os
import json
import sys
from random import choice, randint
from datetime import datetime

import crud
import model
import server

# Modify sys.path to include the parent directory
sys.path.append('..')
import utils
from utils import UNDERLINED, GREEN_BOLD, YELLOW_BOLD, RED_BOLD, RESET


version_number = 0.2
program_name = "PARM Database Seeder 3,000,000"


# Drop and create database
os.system('dropdb parm')
os.system('createdb parm')


# Execute SQL script on the database
os.system('psql -d parm < PARM-Schema.sql')

model.connect_to_db(server.app)
model.db.create_all()

seeded_message = "This was generated automatically when database was seeded."




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
        

    #     db_movie = crud.create_movie(title, overview, release_date, poster_path)
    #     movies_in_db.append(db_movie)
        
    # model.db.session.add_all(movies_in_db)
    # model.db.session.commit()


    # Setup Timezones
    try:
        model.db.session.begin()
        # UTC
        utc = crud.create_timezone_entry(
            id = 0,
            identifier = model.TimezoneIdentifier.UTC.value,
            abbreviation = model.TimezoneAbbreviation.UTC.value,
            utc_offset_minutes = (0 * 60),
            has_dst = False,
            commit=False
            )
        # Hawaii
        hawaii = crud.create_timezone_entry(
            id = 1,
            identifier = model.TimezoneIdentifier.HONOLULU.value,
            abbreviation = model.TimezoneAbbreviation.HAWIIAN.value,
            utc_offset_minutes = (-10 * 60),
            has_dst = False,
            commit=False
            )
        # Alaska
        alaska = crud.create_timezone_entry(
            id = 2,
            identifier = model.TimezoneIdentifier.ANCHORAGE.value,
            abbreviation = model.TimezoneAbbreviation.ALASKAN.value,
            utc_offset_minutes = (-9 * 60),
            has_dst = True,
            commit=False
            )
        # Pacific
        pacific = crud.create_timezone_entry(
            id = 3,
            identifier = model.TimezoneIdentifier.LOS_ANGELES.value,
            abbreviation = model.TimezoneAbbreviation.PACIFIC.value,
            utc_offset_minutes = (-8 * 60),
            has_dst = True,
            commit=False
            )
        # Mountain
        mountain = crud.create_timezone_entry(
            id = 4,
            identifier = model.TimezoneIdentifier.DENVER.value,
            abbreviation = model.TimezoneAbbreviation.MOUNTAIN.value,
            utc_offset_minutes = (-7 * 60),
            has_dst = True,
            commit=False
            )
        # Phoenix
        phoenix = crud.create_timezone_entry(
            id = 5,
            identifier = model.TimezoneIdentifier.PHOENIX.value,
            abbreviation = model.TimezoneAbbreviation.MOUNTAIN.value,
            utc_offset_minutes = (-7 * 60),
            has_dst = False,
            commit=False
            )
        # Central
        central = crud.create_timezone_entry(
            id = 6,
            identifier = model.TimezoneIdentifier.CHICAGO.value,
            abbreviation = model.TimezoneAbbreviation.CENTRAL.value,
            utc_offset_minutes = (-6 * 60),
            has_dst = True,
            commit=False
            )
        # Eastern
        eastern = crud.create_timezone_entry(
            id = 7,
            identifier = model.TimezoneIdentifier.NEW_YORK.value,
            abbreviation = model.TimezoneAbbreviation.EASTERN.value,
            utc_offset_minutes = (-5 * 60),
            has_dst = True,
            commit=False
            )
        
        model.db.session.add(utc)
        model.db.session.add(hawaii)
        model.db.session.add(alaska)
        model.db.session.add(pacific)
        model.db.session.add(mountain)
        model.db.session.add(phoenix)
        model.db.session.add(central)
        model.db.session.add(eastern)

        model.db.session.commit()
        
    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        print(f"\nError occurred!\nseed_database.py\nLine 152\n{e}")




    # Setup Currencies
    try:
        model.db.session.begin()
        # United States
        usa = crud.create_currency_entry(
            id = 0,
            name = "United States Dollar",
            symbol = "$",
            iso_code = model.CurrencyIsoCode.UNITED_STATES.value,
            exchange_rate = 1,
            commit=False
            )
        # Canada
        canada = crud.create_currency_entry(
            id = 1,
            name = "Canadian Dollar",
            symbol = "Can$",
            iso_code = model.CurrencyIsoCode.CANADA.value,
            exchange_rate = 1.360252, 
            commit=False
            )
        # Mexico
        mexico = crud.create_currency_entry(
            id = 2,
            name = "Mexican Peso",
            symbol = "Mex$",
            iso_code = model.CurrencyIsoCode.MEXICO.value,
            exchange_rate = 16.78694,
            commit=False
            )

        
        model.db.session.add(usa)
        model.db.session.add(canada)
        model.db.session.add(mexico)

        model.db.session.commit()
        
    except Exception as e:
        # If any error occurs, rollback the changes
        model.db.session.rollback()
        print(f"\nError occurred!\nseed_database.py\nLine 198\n{e}")



    # crud.create_user(password_hash="admin",
    #                     first_name="admin",
    #                     last_name="admin",
    #                     currency_id=0,
    #                     time_format_is_24=True,  # or False, based on your needs
    #                     created_by_user_id=0,
    #                     details=seeded_message,
    #                     commit=True)
    


    # Create the bootstrap user without referencing the AuditInfoEntry
    bootstrap_user = model.User(
        password_hash="admin",
        first_name="admin",
        last_name="admin",
        currency_id=0,
        # ... other fields, but NOT the audit_info_entry_id
    )
    model.db.session.add(bootstrap_user)
    model.db.session.commit()


    created_by_user_id = bootstrap_user.id
    crud.create_user(password_hash="password",
                    first_name="John",
                    last_name="Doe",
                    currency_id=1,
                    time_format_is_24=True,
                    created_by_user_id=created_by_user_id,
                    details=seeded_message,
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
                                                                                              details=seeded_message,
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