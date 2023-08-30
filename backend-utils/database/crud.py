"""CRUD operations."""

# from sqlalchemy import func
# from model import db, User, Asset, Rating, connect_to_db
import model

def create_timezone_entry(id, identifier, abbreviation, utc_offset_minutes, has_dst, commit=True):
    
    # Check to make sure that the value is in the Enum list
    if identifier not in [e.value for e in model.TimezoneIdentifier]:
        raise ValueError(f"Invalid operation type: {identifier}")
    
    # Check to make sure that the value is in the Enum list
    if abbreviation not in [e.value for e in model.TimezoneAbbreviation]:
        raise ValueError(f"Invalid operation type: {abbreviation}")

    timezone_entry = model.Timezone(
        id = id,
        identifier = identifier,
        abbreviation = abbreviation,
        utc_offset_minutes = utc_offset_minutes,
        has_dst = has_dst
    )

    if commit:
        model.db.session.add(timezone_entry)
        model.db.session.commit()

    return timezone_entry




def create_currency_entry(id, name, symbol, iso_code, exchange_rate, commit=True):
    
    # Check to make sure that the value is in the Enum list
    if iso_code not in [e.value for e in model.CurrencyIsoCode]:
        raise ValueError(f"Invalid operation type: {iso_code}")
    
    currency_entry = model.Currency(
        id = id,
        name = name,
        symbol = symbol,
        iso_code = iso_code,
        exchange_rate = exchange_rate
    )

    if commit:
        model.db.session.add(currency_entry)
        model.db.session.commit()

    return currency_entry




def create_audit_entry(operation_type, created_by_user_id, details=None, commit=True):
    """Create and return a new audit info entry."""

    # Check to make sure that the value is in the Enum list
    if operation_type not in [e.value for e in model.OperationType]:
        raise ValueError(f"Invalid operation type: {operation_type}")

    audit_entry = model.AuditInfoEntry(
        operation_type = operation_type,
        details = details,
        created_by = created_by_user_id,
        last_edited_by = created_by_user_id
    )

    if commit:
        model.db.session.add(audit_entry)
        model.db.session.commit()

    return audit_entry

def create_user_setting(created_by_user_id,
                        details,
                        currency_id = 0,
                        time_format_is_24 = False,
                        is_darkmode = False,
                        commit = True):
    """Create and return a settings for a user."""

    # Check to make sure that the value is in the Enum list
    if currency_id not in [e.value for e in model.CurrencyIsoCode]:
        raise ValueError(f"Invalid operation type: {currency_id}")
    
    user_setting_audit_entry = create_audit_entry("CREATE",
                                                    created_by_user_id,
                                                    details)

    user_setting = model.UserSetting(
        currency_id = currency_id,
        time_format_is_24 = time_format_is_24,
        is_darkmode = is_darkmode,
        audit_info_entry_id = user_setting_audit_entry.id
    )

    if commit:
        model.db.session.add(user_setting_audit_entry)
        model.db.session.add(user_setting)
        model.db.session.commit()

    return user_setting, user_setting_audit_entry


def create_user(password_hash,
                first_name,
                last_name,
                currency_id,
                time_format_is_24,
                created_by_user_id,
                details = None,
                is_darkmode = False,
                middle_name = None,
                nickname = None,
                nickname_prefered = None,
                last_login = None,
                commit = True):
    """Create and return a new user."""

    # user_audit_entry = create_audit_entry("CREATE",
    #                                  details,
    #                                  created_by_user_id)
    
    user_audit_entry = create_audit_entry("CREATE",
                                 created_by_user_id,
                                 details)

    
    user_setting, user_setting_audit_entry = create_user_setting(currency_id,
                                                                  time_format_is_24,
                                                                  is_darkmode,
                                                                  created_by_user_id,
                                                                  details)

    user = model.User(
        password_hash = password_hash, 
        first_name = first_name,
        middle_name = middle_name,
        last_name = last_name,
        nickname = nickname,
        nickname_prefered = nickname_prefered,
        user_settings_id = user_setting.id,
        last_login = last_login,
        audit_info_entry_id = user_audit_entry.id
    )

    if commit:
        model.db.session.add(user_audit_entry)
        model.db.session.add(user_setting_audit_entry)
        model.db.session.add(user_setting)
        model.db.session.add(user)
        model.db.session.commit()

    return user, user_audit_entry, user_setting, user_setting_audit_entry





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