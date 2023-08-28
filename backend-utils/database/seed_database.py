"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server


os.system('dropdb parm')
os.system('createdb parm')

model.connect_to_db(server.app)
model.db.create_all()

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


for n in range(10):

    password_hash = 'test'
    first_name = 'bob'
    last_name = 'theBuilder'
    # email = f'{first_name}{n}@builder.net'  # Voila! A unique email!

    db_user = crud.create_user(password_hash, first_name, last_name)
    model.db.session.add(db_user)

    # # TODO: Create 10 Reservations for each user
    # for n in range(10):

    #     temp_movie = choice(movies_in_db)
    #     temp_rating = randint(1,5)

    #     db_rating = crud.create_rating(db_user, temp_movie, temp_rating)

    #     model.db.session.add(db_rating)
        
    model.db.session.commit()