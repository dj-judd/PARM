"""CRUD operations."""

from sqlalchemy import func
# from model import db, User, Asset, Rating, connect_to_db
import model


def create_user(password_hash, first_name, last_name):
    """Create and return a new user."""

    user = model.User(password_hash=password_hash, first_name=first_name, last_name=last_name)

    return user


def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = model.Movie(
                  title=title,
                  overview=overview,
                  release_date=release_date,
                  poster_path=poster_path,
                  )

    return movie

def create_rating(user, movie, score):
    
    rating = model.Rating(user=user, movie=movie, score=score)

    return rating

if __name__ == '__main__':
    from server import app
    model.connect_to_db(app)