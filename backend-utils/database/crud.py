"""CRUD operations."""

# from sqlalchemy import func
# from model import db, User, Asset, Rating, connect_to_db
import model

def create_timezone_entry(id, identifier, abbreviation, utc_offset_minutes, has_dst, commit=True):
    
    # Check to make sure that the value is in the Enum list
    if identifier not in [e.value for e in model.TimezoneIdentifier]:
        raise ValueError(f"Invalid identifier: {identifier}")
    
    # Check to make sure that the value is in the Enum list
    if abbreviation not in [e.value for e in model.TimezoneAbbreviation]:
        raise ValueError(f"Invalid abbreviation: {abbreviation}")

    timezone_entry = model.Timezone(
        id = id,
        identifier = identifier,
        abbreviation = abbreviation,
        utc_offset_minutes = utc_offset_minutes,
        has_dst = has_dst
    )

    # Always add to the session
    model.db.session.add(timezone_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return timezone_entry



def create_country_entry(id, code, name, intl_phone_code, commit=True):
    
    # Check to make sure that the value is in the Enum list
    if code not in [e.value for e in model.CountryIsoCode]:
        raise ValueError(f"Invalid code: {code}")
    

    country_entry = model.Country(
        id = id,
        code = code,
        name = name,
        intl_phone_code = intl_phone_code,
    )

    # Always add to the session
    model.db.session.add(country_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return country_entry



def create_state_entry(code, name, timezone_id, country_id, commit=True):
    
    # Check to make sure that the value is in the Enum list
    if code not in [e.value for e in model.StateCodes]:
        raise ValueError(f"Invalid code: {code}")
    
    # Check to make sure that the value is in the Enum list
    if name not in [e.value for e in model.StateNames]:
        raise ValueError(f"Invalid name: {name}")

    state_entry = model.State(
        code = code,
        name = name,
        timezone_id = timezone_id,
        country_id = country_id
    )

    # Always add to the session
    model.db.session.add(state_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return state_entry


def create_currency_entry(id, name, symbol, iso_code, exchange_rate, commit=True):
    
    # Check to make sure that the value is in the Enum list
    if iso_code not in [e.value for e in model.CurrencyIsoCode]:
        raise ValueError(f"Invalid iso code: {iso_code}")
    
    currency_entry = model.Currency(
        id = id,
        name = name,
        symbol = symbol,
        iso_code = iso_code,
        exchange_rate = exchange_rate
    )

    # Always add to the session
    model.db.session.add(currency_entry)
    
    # Commit only if commit=True
    if commit:
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

    # Always add to the session
    model.db.session.add(audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return audit_entry

def create_global_settings(deployment_fingerprint, default_currency_id, commit=True):
    """Create and return a global settings entry."""

    currency = model.db.session.query(model.Currency).filter_by(id=default_currency_id).first()

    # Check if currency exists
    if not currency:
        raise ValueError(f"Invalid currency ID: {default_currency_id}")

    global_setting = model.GlobalSettings(
        deployment_fingerprint=deployment_fingerprint,
        default_currency_id=default_currency_id
    )

    # Always add the global_setting to the session
    model.db.session.add(global_setting)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return global_setting



def create_user_setting(created_by_user_id,
                        details,
                        currency_id=1,
                        time_format_is_24h=False,
                        ui_theme_id=1, 
                        commit=True):
    """Create and return a settings for a user."""

    # Validate the currency_id against the database
    currency_exists = model.db.session.query(model.Currency).filter_by(id=currency_id).first()
    if not currency_exists:
        raise ValueError(f"Invalid currency ID: {currency_id}")
    
    user_setting_audit_entry = create_audit_entry(model.OperationType.CREATE.value,
                                                  created_by_user_id,
                                                  details)

    user_setting = model.UserSettings(
        currency_id=currency_id,
        time_format_is_24h=time_format_is_24h,
        ui_theme_id=ui_theme_id,
        audit_info_entry_id=user_setting_audit_entry.id
    )

    # Always add to the session
    model.db.session.add(user_setting_audit_entry)
    model.db.session.add(user_setting)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()


    return user_setting, user_setting_audit_entry


def create_user(password_hash,
                first_name,
                last_name,
                currency_id,
                created_by_user_id,
                time_format_is_24h=False,
                audit_details = None,
                ui_theme_id = 1,
                middle_name = None,
                nickname = None,
                nickname_preferred = None,
                last_login = None,
                commit = True):
    """Create and return a new user."""

    
    user_audit_entry = create_audit_entry(model.OperationType.CREATE.value,
                                 created_by_user_id,
                                 audit_details)

    
    user_setting, user_setting_audit_entry = create_user_setting(created_by_user_id,
                                                             audit_details,
                                                             currency_id,
                                                             time_format_is_24h,
                                                             ui_theme_id)

    user = model.User(
        password_hash = password_hash, 
        first_name = first_name,
        middle_name = middle_name,
        last_name = last_name,
        nickname = nickname,
        nickname_preferred = nickname_preferred,
        user_settings_id = user_setting.id,
        last_login = last_login,
        audit_info_entry_id = user_audit_entry.id
    )

    # Always add to the session
    model.db.session.add(user_audit_entry)
    model.db.session.add(user_setting_audit_entry)
    model.db.session.add(user_setting)
    model.db.session.add(user)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return user, user_audit_entry, user_setting, user_setting_audit_entry



def create_phone_number(phone_type,
                        is_cell,
                        country_code,
                        area_code,
                        phone_number,
                        extension,
                        is_verified,
                        is_primary):



    phone_number_audit_entry = create_audit_entry(model.OperationType.CREATE.value,
                                 created_by_user_id,
                                 audit_details)









# Read




def read_global_settings():
    """Fetch default settings from the global_settings table."""
    global_settings = model.db.session.query(model.GlobalSettings).first()
    
    if global_settings:
        return {
            "deployment_fingerprint": global_settings.deployment_fingerprint,
            "default_currency_id": global_settings.default_currency_id
        }
    else:
        return None





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