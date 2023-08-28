"""CRUD operations."""

from sqlalchemy import func
# from model import db, User, Asset, Rating, connect_to_db
import model



def create_audit_entry(operation_type, created_by_user_id, details=None, commit=True):
    """Create and return a new audit info entry."""

    # Check to make sure that the value is in the Enum list
    if operation_type not in [e.value for e in model.OperationType]:
        raise ValueError(f"Invalid operation type: {operation_type}")

    audit_entry = model.AuditInfoEntry(
        operation_type=operation_type,
        details=details,
        created_by=created_by_user_id,
        last_edited_by=created_by_user_id
    )

    if commit:
        model.db.session.add(audit_entry)
        model.db.session.commit()

    return audit_entry


def create_user(password_hash, first_name, last_name, created_by_user_id, commit=True):
    """Create and return a new user."""

    audit_entry = create_audit_entry("CREATE", created_by_user_id)

    user = model.User(
        password_hash=password_hash, 
        first_name=first_name, 
        last_name=last_name,
        audit_info_entry_id=audit_entry.id
    )

    if commit:
        model.db.session.add(audit_entry)
        model.db.session.add(user)
        model.db.session.commit()

    return user, audit_entry





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