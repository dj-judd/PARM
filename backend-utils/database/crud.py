"""CRUD operations."""

from sqlalchemy import func
# from model import db, User, Asset, Rating, connect_to_db
import model


def create_audit_entry(operation_type, created_by_user_id, details=None):
    """Create and return a new audit info entry."""

    audit_entry = model.AuditInfoEntry(
        operation_type=operation_type,
        details=details,
        created_by=created_by_user_id,
        last_edited_by=created_by_user_id
    )
    
    db.session.add(audit_entry)
    db.session.commit()

    return audit_entry


def create_user(password_hash, first_name, last_name, created_by_user_id):
    """Create and return a new user."""

    audit_entry = create_audit_entry("CREATE", created_by_user_id)

    user = model.User(
        password_hash=password_hash, 
        first_name=first_name, 
        last_name=last_name,
        audit_info_entry_id=audit_entry.id
    )
    
    db.session.add(user)
    db.session.commit()

    return user



# def create_movie(title, overview, release_date, poster_path):
#     """Create and return a new movie."""

#     movie = model.Movie(
#                   title=title,
#                   overview=overview,
#                   release_date=release_date,
#                   poster_path=poster_path,
#                   )

#     return movie

# def create_rating(user, movie, score):
    
#     rating = model.Rating(user=user, movie=movie, score=score)

#     return rating

if __name__ == '__main__':
    from server import app
    model.connect_to_db(app)