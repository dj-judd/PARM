"""CRUD operations."""

import os
import sys
import model

from datetime import datetime

from backend_utils import utils
from backend_utils.utils import UNDERLINED, GREEN_BOLD, YELLOW_BOLD, RED_BOLD, RESET



def create_timezone_entry(id,
                          identifier,
                          abbreviation,
                          utc_offset_minutes,
                          has_dst,
                          commit=True):
    
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



def create_country_entry(id,
                         code,
                         name,
                         intl_phone_code,
                         commit=True):
    
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



def create_audit_entry(operation_type,
                       auditable_entity_type: model.AuditableEntityTypes, #Type hint
                       created_by_user_id,
                       related_entity_id=None,
                       related_entity_hash=None,
                       related_composite_id=None,
                       audit_details=None,
                       commit=True):
    """Create and return a new audit info entry."""

    # Check to make sure that the value is in the Enum list
    if operation_type not in [e.value for e in model.OperationType]:
        raise ValueError(f"Invalid operation type: {operation_type}")

    if related_entity_id is None and related_entity_hash is None:
        raise ValueError("Either related_entity_id or related_entity_hash must be provided.")

    time_stamp = datetime.utcnow()
    audit_entry = model.AuditEntry(
        operation_type=operation_type,
        auditable_entity_type=auditable_entity_type,
        related_entity_id=related_entity_id,
        related_entity_hash=related_entity_hash,
        related_composite_id=related_composite_id,  # For composite Foreign Keys
        details=audit_details,
        created_by=created_by_user_id,
        created_at=time_stamp,
        last_edited_by=created_by_user_id,
        last_edited_at=time_stamp
    )
    # Always add to the session
    model.db.session.add(audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return audit_entry



def create_global_settings(deployment_fingerprint,
                           default_currency_id,
                           audit=True,
                           created_by_user_id=None,
                           audit_details=None,
                           commit=True):
    """Create and return a global settings entry."""

    currency = model.db.session.query(model.Currency).filter_by(id=default_currency_id).first()

    # Check if currency exists
    if not currency:
        raise ValueError(f"Invalid currency ID: {default_currency_id}")

    global_settings = model.GlobalSettings(
        deployment_fingerprint=deployment_fingerprint,
        default_currency_id=default_currency_id
    )

    # Add the global_setting to the session
    model.db.session.add(global_settings)


    # Adding this just to the ones that need initalized for database creation
    if audit:
        # Flush to get the, now created, id for this entity for the AuditEntry
        model.db.session.flush()

        audit_entry = create_audit_entry(
            operation_type=model.OperationType.CREATE.value,
            auditable_entity_type=model.CLASS_TO_ENUM_MAP['GlobalSettings'],
            related_entity_id=global_settings.id,
            created_by_user_id=created_by_user_id,
            audit_details=audit_details
        )

        # Add the audit_entry to the session
        model.db.session.add(audit_entry)


    # Commit only if commit=True
    if commit:
        model.db.session.commit()


    if audit:
        return global_settings, audit_entry
    else:
        return global_settings



def create_color(name,
                 hex_value,
                 audit=True,
                 created_by_user_id=None,
                 audit_details=None,
                 commit=True):
    """Create and return a color."""

    color = model.Color(
        name=name,
        hex_value=hex_value,
    )

    # Always add to the session
    model.db.session.add(color)


    # Adding this just to the ones that need initalized for database creation
    if audit:
        # Flush to get id for this entity for the AuditEntry
        model.db.session.flush()

        audit_entry = create_audit_entry(
            operation_type=model.OperationType.CREATE.value,
            auditable_entity_type=model.CLASS_TO_ENUM_MAP['Color'],
            related_entity_id=color.id,
            created_by_user_id=created_by_user_id,
            audit_details=audit_details
        )

        # Add the audit_entry to the session
        model.db.session.add(audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()


    if audit:
        return color, audit_entry
    else:
        return color



def create_ui_theme(name,
                    description,
                    primary_color_id,
                    secondary_color_id,
                    audit=True,
                    created_by_user_id=None,
                    audit_details=None,
                    commit=True):
    """Create and return a UI Theme."""

    uiTheme = model.UiTheme(
        name=name,
        description=description,
        primary_color_id=primary_color_id,
        secondary_color_id=secondary_color_id
    )

    # Always add to the session
    model.db.session.add(uiTheme)


    # Adding this just to the ones that need initalized for database creation
    if audit:
        # Flush to get id for this entity for the AuditEntry
        model.db.session.flush()

        audit_entry = create_audit_entry(
            operation_type=model.OperationType.CREATE.value,
            auditable_entity_type=model.CLASS_TO_ENUM_MAP['Color'],
            related_entity_id=uiTheme.id,
            created_by_user_id=created_by_user_id,
            audit_details=audit_details
        )

        # Add the audit_entry to the session
        model.db.session.add(audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()


    if audit:
        return uiTheme, audit_entry
    else:
        return uiTheme



def create_user_settings(currency_id,
                         time_format_is_24h,
                         ui_theme_id, 
                         audit=True,
                         created_by_user_id=None,
                         audit_details=None,
                         commit=True,
                         id=None):
    """Create and return a settings for a user."""

    # Validate the currency_id against the database
    currency_exists = model.db.session.query(model.Currency).filter_by(id=currency_id).first()
    if not currency_exists:
        raise ValueError(f"Invalid currency ID: {currency_id}")
    

    user_settings = model.UserSettings(
        id=id,
        currency_id=currency_id,
        time_format_is_24h=time_format_is_24h,
        ui_theme_id=ui_theme_id
    )

    # Always add to the session
    model.db.session.add(user_settings)


    # Adding this just to the ones that need initalized for database creation
    if audit:
        # Flush to get id for this entity for the AuditEntry
        model.db.session.flush()

        audit_entry = create_audit_entry(
            operation_type=model.OperationType.CREATE.value,
            auditable_entity_type=model.CLASS_TO_ENUM_MAP['UserSettings'],
            related_entity_id=user_settings.id,
            created_by_user_id=created_by_user_id,
            audit_details=audit_details
        )

        # Add the audit_entry to the session
        model.db.session.add(audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()


    if audit:
        return user_settings, audit_entry
    else:
        return user_settings



def create_bootstrap_user(password_hash,
                          first_name,
                          last_name,
                          currency_id,
                          time_format_is_24h=False,
                          ui_theme_id=1,
                          middle_name=None,
                          nickname=None,
                          nickname_preferred=None,
                          last_login=None,
                          audit=False,
                          created_by_user_id=None,
                          audit_details=None,
                          commit=True,
                          id=None):
    """Create and return a new bootstrap user for DB initialization."""

    bootstrap_user_settings = create_user_settings(
        id=id,
        currency_id=currency_id,
        time_format_is_24h=time_format_is_24h,
        ui_theme_id=ui_theme_id,
        audit=audit,
        created_by_user_id=created_by_user_id,
        audit_details=audit_details,
        commit=False
        )

    ## They already get added in the create method
    # model.db.session.add(user_settings)

    # Flush to get id for this entity for the User
    model.db.session.flush()

    bootstrap_user = model.User(
        id=id,
        password_hash=password_hash, 
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        nickname=nickname,
        nickname_preferred=nickname_preferred,
        user_settings_id=bootstrap_user_settings.id,
        last_login=last_login
        )


    # Add user to the session for flush
    model.db.session.add(bootstrap_user)


    ## BOOTSTRAP USER WILL NEVER GET AN AUDIT IN IT'S INITIALIZATION
    # # Flush to get id for this entity for the AuditEntry
    # model.db.session.flush()


    # user_audit_entry = create_audit_entry(
    #     operation_type=model.OperationType.CREATE.value,
    #     auditable_entity_type=model.CLASS_TO_ENUM_MAP['User'],
    #     related_entity_id=user.id,
    #     created_by_user_id=created_by_user_id,
    #     details=audit_details
    # )

    # # Add the user_audit_entry to the session
    # model.db.session.add(user_audit_entry)


    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return bootstrap_user, bootstrap_user_settings



def create_user(password_hash,
                first_name,
                last_name,
                currency_id,
                created_by_user_id,
                time_format_is_24h=False,
                audit_details=None,
                ui_theme_id=1,
                middle_name=None,
                nickname=None,
                nickname_preferred=None,
                last_login=None,
                commit=True):
    """Create and return a new user."""

    user_settings, user_settings_audit_entry = create_user_settings(
        currency_id=currency_id,
        time_format_is_24h=time_format_is_24h,
        ui_theme_id=ui_theme_id,
        created_by_user_id=created_by_user_id,
        audit_details=audit_details,
        commit=False
        )

    ## Always add to the session
    ## They already get added in the create method
    # model.db.session.add(user_settings, user_settings_audit_entry)

    # Flush to get id for this entity for the AuditEntry & User
    model.db.session.flush()

    user = model.User(
        password_hash=password_hash, 
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        nickname=nickname,
        nickname_preferred=nickname_preferred,
        user_settings_id=user_settings.id,
        last_login=last_login
        )


    # Add user to the session for flush
    model.db.session.add(user)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()


    user_audit_entry = create_audit_entry(
        operation_type=model.OperationType.CREATE.value,
        auditable_entity_type=model.CLASS_TO_ENUM_MAP['User'],
        related_entity_id=user.id,
        created_by_user_id=created_by_user_id,
        audit_details=audit_details
    )

    # Add the user_audit_entry to the session
    model.db.session.add(user_audit_entry)


    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return user, user_audit_entry, user_settings, user_settings_audit_entry



def create_phone_number(phoneable_entity_type: model.PhoneableEntityTypes, #Type hint
                        entity_id,
                        phone_type: model.PhoneType, #Type hint,
                        is_cell,
                        country_code,
                        area_code,
                        phone_number,
                        created_by_user_id,
                        audit_details=None,
                        extension=None,
                        is_verified=False,
                        is_primary=False,
                        commit=True):
    """Create and return a phone number."""

    phone_number = model.PhoneNumber(
        phoneable_entity_type=phoneable_entity_type,
        entity_id=entity_id,
        phone_type=phone_type,
        is_cell=is_cell,
        country_code=country_code,
        area_code=area_code,
        phone_number=phone_number,
        extension=extension,
        is_verified=is_verified,
        is_primary=is_primary
    )

    # Add phone_number to the session for flush
    model.db.session.add(phone_number)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    phone_number_audit_entry = create_audit_entry(
        operation_type=model.OperationType.CREATE.value,
        auditable_entity_type=model.CLASS_TO_ENUM_MAP['PhoneNumber'],
        related_entity_id=phone_number.id,
        created_by_user_id=created_by_user_id,
        audit_details=audit_details
    )

    # Add the user_audit_entry to the session
    model.db.session.add(phone_number_audit_entry)


    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return phone_number, phone_number_audit_entry



def create_email_address(emailable_entity_type: model.EmailableEntityTypes, #Type hint
                         entity_id,
                         email_type: model.EmailType, #Type hint,email_type: model.EmailType, #Type hint
                         email_address, 
                         created_by_user_id,
                         audit_details=None,
                         is_verified=False, 
                         is_primary=None, 
                         is_shared=None, 
                         commit=True):
    """Create and return a new email address."""
    
    email_address = model.EmailAddress(
        emailable_entity_type=emailable_entity_type,
        entity_id=entity_id,
        email_type=email_type,
        email_address=email_address,
        is_verified=is_verified,
        is_primary=is_primary,
        is_shared=is_shared
    )

    # Add email_address to the session for flush
    model.db.session.add(email_address)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    email_audit_entry = create_audit_entry(
        operation_type=model.OperationType.CREATE.value,
        auditable_entity_type=model.CLASS_TO_ENUM_MAP['EmailAddress'],
        related_entity_id=email_address.id,
        created_by_user_id=created_by_user_id,
        audit_details=audit_details
    )

    # Add the user_audit_entry to the session
    model.db.session.add(email_audit_entry)


    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return email_address, email_audit_entry



def create_user_role(user_id,
                     role_id,
                     created_by_user_id,
                     audit_details=None,
                     commit=True):
    """Create and return a new user role entry."""

    user_role = model.UserRole(
        user_id=user_id,
        role_id=role_id
    )
    
    # Add user_role to the session for flush
    model.db.session.add(user_role)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    audit_entry = create_audit_entry(
        operation_type=model.OperationType.CREATE.value,
        auditable_entity_type=model.CLASS_TO_ENUM_MAP['UserRole'],
        related_entity_id=user_role.user_id,
        related_composite_id=user_role.role_id,
        created_by_user_id=created_by_user_id,
        audit_details=audit_details
    )

    # Add the audit_entry to the session
    model.db.session.add(audit_entry)


    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return user_role, audit_entry



def create_role(name, description,
                created_by_user_id,
                audit_details=None,
                commit=True):
    """Create and return a new role entry."""

    role = model.Role(
        name=name,
        description=description
    )
    
    # Add role to the session for flush
    model.db.session.add(role)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    audit_entry = create_audit_entry(
        operation_type=model.OperationType.CREATE.value,
        auditable_entity_type=model.CLASS_TO_ENUM_MAP['Role'],
        related_entity_id=role.id,
        created_by_user_id=created_by_user_id,
        audit_details=audit_details
    )

    # Add the audit_entry to the session
    model.db.session.add(audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return role, audit_entry



def create_role_permission(role_id,
                           permission_id,
                           created_by_user_id,
                           audit_details=None,
                           commit=True):
    """Create and return a new role permission entry."""
    
    role_permission = model.RolePermission(
        role_id=role_id,
        permission_id=permission_id
    )
    
    # Add role_permission to the session for flush
    model.db.session.add(role_permission)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    audit_entry = create_audit_entry(
        operation_type=model.OperationType.CREATE.value,
        auditable_entity_type=model.CLASS_TO_ENUM_MAP['RolePermission'],
        related_entity_id=role_permission.role_id,
        related_composite_id=role_permission.permission_id,
        created_by_user_id=created_by_user_id,
        audit_details=audit_details
    )

    # Add the audit_entry to the session
    model.db.session.add(audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return role_permission, audit_entry



def create_permission(name,
                      description,
                      created_by_user_id,
                      audit_details=None,
                      commit=True):
    """Create and return a new permission entry."""
    
    permission = model.Permission(
        name=name,
        description=description
    )

    # Add permission to the session for flush
    model.db.session.add(permission)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    audit_entry = create_audit_entry(
        operation_type=model.OperationType.CREATE.value,
        auditable_entity_type=model.CLASS_TO_ENUM_MAP['Permission'],
        related_entity_id=permission.id,
        created_by_user_id=created_by_user_id,
        audit_details=audit_details
    )

    # Add audit_entry to the session
    model.db.session.add(audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return permission, audit_entry






# READ




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







# UPDATE






def update_default_currency(default_currency_id, commit=True):
    """Update the default currency in the global_settings table."""
    global_settings = model.db.session.query(model.GlobalSettings).first()
    
    if global_settings:
        # Update the default_currency_id
        global_settings.default_currency_id = default_currency_id
        if commit:
            model.db.session.commit()
            utils.successMessage()
        
        # Return the updated default currency ID
        return global_settings.default_currency_id
    else:
        utils.errorMessage("Global settings entry not found.")
        return None






# def update_default_currency(default_currency_id):
#     """Update the default currency in the global_settings table."""
#     global_settings = model.db.session.query(model.GlobalSettings).first()
    
#     if global_settings:
#         # Update the default_currency_id
#         global_settings.default_currency_id = default_currency_id
#         model.db.session.commit()
#         return {
#             utils.successMessage()
#         }
#     else:
#         return {
#             utils.errorMessage("Global settings entry not found.")
#         }



if __name__ == '__main__':
    from server import app
    model.connect_to_db(app)