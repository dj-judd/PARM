"Create methods for DB Entities"

import model

from typing import Optional
from datetime import datetime




# CREATE




def timezone(id: int,
             identifier: model.TimezoneIdentifier,
             abbreviation: model.TimezoneAbbreviation,
             utc_offset_minutes: int,
             has_dst: bool,
             commit: bool = True):
    """Create and return a Timezone entry."""
    
    # Check to make sure that the value is in the Enum list
    if identifier not in [e.value for e in model.TimezoneIdentifier]:
        raise ValueError(f"Invalid identifier: {identifier}")
    
    # Check to make sure that the value is in the Enum list
    if abbreviation not in [e.value for e in model.TimezoneAbbreviation]:
        raise ValueError(f"Invalid abbreviation: {abbreviation}")

    timezone = model.Timezone(id = id,
                              identifier = identifier,
                              abbreviation = abbreviation,
                              utc_offset_minutes = utc_offset_minutes,
                              has_dst = has_dst)

    # Always add to the session
    model.db.session.add(timezone)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return timezone




def country(id: int,
            code: model.CountryIsoCode,
            name: str,
            intl_phone_code: int,
            commit: bool = True):
    """Create and return a Country entry."""
    
    # Check to make sure that the value is in the Enum list
    if code not in [e.value for e in model.CountryIsoCode]:
        raise ValueError(f"Invalid code: {code}")
    

    country = model.Country(id = id,
                            code = code,
                            name = name,
                            intl_phone_code = intl_phone_code)

    # Always add to the session
    model.db.session.add(country)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return country




def state(code: model.StateCodes,
          name: model.StateNames,
          timezone_id: int,
          country_id: int,
          commit: bool = True):
    """Create and return a State entry."""
    
    # Check to make sure that the value is in the Enum list
    if code not in [e.value for e in model.StateCodes]:
        raise ValueError(f"Invalid code: {code}")
    
    # Check to make sure that the value is in the Enum list
    if name not in [e.value for e in model.StateNames]:
        raise ValueError(f"Invalid name: {name}")

    state = model.State(code = code,
                        name = name,
                        timezone_id = timezone_id,
                        country_id = country_id)

    # Always add to the session
    model.db.session.add(state)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return state




def currency(id: int,
             name: str,
             symbol: str,
             iso_code: model.CurrencyIsoCode,
             exchange_rate: int,
             commit: bool = True):
    """Create and return a Currency entry."""
    
    # Check to make sure that the value is in the Enum list
    if iso_code not in [e.value for e in model.CurrencyIsoCode]:
        raise ValueError(f"Invalid iso code: {iso_code}")
    
    currency = model.Currency(id = id,
                              name = name,
                              symbol = symbol,
                              iso_code = iso_code,
                              exchange_rate = exchange_rate)

    # Always add to the session
    model.db.session.add(currency)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return currency




def financial_entry(currency_id: int,
                    amount: int,
                    created_by_user_id: int,
                    audit_details: Optional[str] = None,
                    commit: bool = True):
    """Create and return a new Financial Entry entry."""

    financial_entry = model.FinancialEntry(currency_id=currency_id,
                                            amount=amount)
    
    # Add financial_entry to the session for flush
    model.db.session.add(financial_entry)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    financial_entry_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                              auditable_entity_type=model.CLASS_TO_ENUM_MAP['FinancialEntry'],
                                              related_entity_id=financial_entry.id,
                                              created_by_user_id=created_by_user_id,
                                              audit_details=audit_details)

    # Add the audit_entry to the session
    model.db.session.add(financial_entry_audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return financial_entry, financial_entry_audit_entry



def audit_entry(operation_type: model.OperationType,
                auditable_entity_type: model.AuditableEntityTypes,
                created_by_user_id: int,
                related_entity_id: int = None,
                related_entity_hash: str = None,
                related_composite_id: int = None,
                audit_details: Optional[str] = None,
                commit: bool = True):
    """Create and return a new Audit Info entry."""

    # Check to make sure that the value is in the Enum list
    if operation_type not in [e.value for e in model.OperationType]:
        raise ValueError(f"Invalid operation type: {operation_type}")

    if related_entity_id is None and related_entity_hash is None:
        raise ValueError("Either related_entity_id or related_entity_hash must be provided.")

    time_stamp = datetime.utcnow()
    audit_entry = model.AuditEntry(operation_type=operation_type,
                                   auditable_entity_type=auditable_entity_type,
                                   related_entity_id=related_entity_id,
                                   related_entity_hash=related_entity_hash,
                                   related_composite_id=related_composite_id,  # For composite Foreign Keys
                                   details=audit_details,
                                   created_by=created_by_user_id,
                                   created_at=time_stamp,
                                   last_edited_by=created_by_user_id,
                                   last_edited_at=time_stamp)
    
    # Always add to the session
    model.db.session.add(audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return audit_entry




def global_settings(deployment_fingerprint: str,
                    default_currency_id: int,
                    audit: bool = True,
                    created_by_user_id: int = None,
                    audit_details: Optional[str] = None,
                    commit: bool = True):
    """Create and return a Global Settings entry."""

    currency = model.db.session.query(model.Currency).filter_by(id=default_currency_id).first()

    # Check if currency exists
    if not currency:
        raise ValueError(f"Invalid currency ID: {default_currency_id}")

    global_settings = model.GlobalSettings(deployment_fingerprint=deployment_fingerprint,
                                           default_currency_id=default_currency_id)

    # Add the global_setting to the session
    model.db.session.add(global_settings)


    # Adding this just to the ones that need initalized for database creation
    if audit:
        # Flush to get the, now created, id for this entity for the AuditEntry
        model.db.session.flush()

        global_settings_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                                  auditable_entity_type=model.CLASS_TO_ENUM_MAP['GlobalSettings'],
                                                  related_entity_id=global_settings.id,
                                                  created_by_user_id=created_by_user_id,
                                                  audit_details=audit_details)

        # Add the audit_entry to the session
        model.db.session.add(global_settings_audit_entry)


    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    if audit:
        return global_settings, global_settings_audit_entry
    else:
        return global_settings




def color(name: str,
          hex_value: str,
          audit: bool = True,
          created_by_user_id: int = None,
          audit_details: Optional[str] = None,
          commit: bool = True):
    """Create and return a Color entry."""

    color = model.Color(name=name,
                        hex_value=hex_value)

    # Always add to the session
    model.db.session.add(color)


    # Adding this just to the ones that need initalized for database creation
    if audit:
        # Flush to get id for this entity for the AuditEntry
        model.db.session.flush()

        color_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                        auditable_entity_type=model.CLASS_TO_ENUM_MAP['Color'],
                                        related_entity_id=color.id,
                                        created_by_user_id=created_by_user_id,
                                        audit_details=audit_details)

        # Add the audit_entry to the session
        model.db.session.add(color_audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    if audit:
        return color, color_audit_entry
    else:
        return color




def ui_theme(name: str,
             description: str,
             primary_color_id: int,
             secondary_color_id: int,
             audit: bool = True,
             created_by_user_id: int = None,
             audit_details: Optional[str] = None,
             commit: bool = True):
    """Create and return a UI Theme entry."""

    uiTheme = model.UiTheme(name=name,
                            description=description,
                            primary_color_id=primary_color_id,
                            secondary_color_id=secondary_color_id)

    # Always add to the session
    model.db.session.add(uiTheme)


    # Adding this just to the ones that need initalized for database creation
    if audit:
        # Flush to get id for this entity for the AuditEntry
        model.db.session.flush()

        uiTheme_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                          auditable_entity_type=model.CLASS_TO_ENUM_MAP['Color'],
                                          related_entity_id=uiTheme.id,
                                          created_by_user_id=created_by_user_id,
                                          audit_details=audit_details)

        # Add the audit_entry to the session
        model.db.session.add(uiTheme_audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    if audit:
        return uiTheme, uiTheme_audit_entry
    else:
        return uiTheme




def user_settings(currency_id: int,
                  time_format_is_24h: bool,
                  ui_theme_id: int, 
                  audit: bool = True,
                  created_by_user_id: int = None,
                  audit_details: Optional[str] = None,
                  commit: bool = True,
                  id=None):
    """Create and return a User Settings entry."""

    # Validate the currency_id against the database
    currency_exists = model.db.session.query(model.Currency).filter_by(id=currency_id).first()
    if not currency_exists:
        raise ValueError(f"Invalid currency ID: {currency_id}")
    

    user_settings = model.UserSettings(id=id,
                                       currency_id=currency_id,
                                       time_format_is_24h=time_format_is_24h,
                                       ui_theme_id=ui_theme_id)

    # Always add to the session
    model.db.session.add(user_settings)


    # Adding this just to the ones that need initalized for database creation
    if audit:
        # Flush to get id for this entity for the AuditEntry
        model.db.session.flush()

        user_settings_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                                auditable_entity_type=model.CLASS_TO_ENUM_MAP['UserSettings'],
                                                related_entity_id=user_settings.id,
                                                created_by_user_id=created_by_user_id,
                                                audit_details=audit_details)

        # Add the audit_entry to the session
        model.db.session.add(user_settings_audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    if audit:
        return user_settings, user_settings_audit_entry
    else:
        return user_settings




def bootstrap_user(password_hash: str,
                   first_name: str,
                   last_name: str,
                   currency_id: int,
                   time_format_is_24h: bool = False,
                   ui_theme_id: int = 1,
                   middle_name:str = None,
                   nickname:str = None,
                   nickname_preferred: bool = None,
                   last_login: datetime = None,
                   audit: bool = False,
                   created_by_user_id: int = None,
                   audit_details: Optional[str] = None,
                   commit: bool = True,
                   id: int = None):
    """Create and return a new Bootstrap User for DB initialization."""

    bootstrap_user_settings = user_settings(id=id,
                                            currency_id=currency_id,
                                            time_format_is_24h=time_format_is_24h,
                                            ui_theme_id=ui_theme_id,
                                            audit=audit,
                                            created_by_user_id=created_by_user_id,
                                            audit_details=audit_details,
                                            commit=False)

    ## They already get added in the create method
    # model.db.session.add(bootstrap_user_settings)

    # Flush to get id for this entity for the User
    model.db.session.flush()

    bootstrap_user = model.User(id=id,
                                password_hash=password_hash, 
                                first_name=first_name,
                                middle_name=middle_name,
                                last_name=last_name,
                                nickname=nickname,
                                nickname_preferred=nickname_preferred,
                                user_settings_id=bootstrap_user_settings.id,
                                last_login=last_login)


    # Add user to the session for flush
    model.db.session.add(bootstrap_user)


    ## BOOTSTRAP USER WILL NEVER GET AN AUDIT IN IT'S INITIALIZATION
    # # Flush to get id for this entity for the AuditEntry
    # model.db.session.flush()

    # user_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                #    auditable_entity_type=model.CLASS_TO_ENUM_MAP['User'],
                                #    related_entity_id=user.id,
                                #    created_by_user_id=created_by_user_id,
                                #    details=audit_details)

    # # Add the user_audit_entry to the session
    # model.db.session.add(user_audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return bootstrap_user, bootstrap_user_settings




def user(password_hash: str,
         first_name: str,
         last_name: str,
         currency_id: int,
         created_by_user_id: int,
         time_format_is_24h: bool = False,
         audit_details: Optional[str] = None,
         ui_theme_id: int = 1,
         middle_name: str = None,
         nickname: str = None,
         nickname_preferred: bool = None,
         last_login: datetime = None,
         commit: bool = True):
    """Create and return a User entry."""

    new_user_settings, user_settings_audit_entry = user_settings(currency_id=currency_id,
                                                                 time_format_is_24h=time_format_is_24h,
                                                                 ui_theme_id=ui_theme_id,
                                                                 created_by_user_id=created_by_user_id,
                                                                 audit_details=audit_details,
                                                                 commit=False)

    ## Always add to the session
    ## They already get added in the create method
    # model.db.session.add(user_settings, user_settings_audit_entry)

    # Flush to get id for this entity for the AuditEntry & User
    model.db.session.flush()

    user = model.User(password_hash=password_hash, 
                      first_name=first_name,
                      middle_name=middle_name,
                      last_name=last_name,
                      nickname=nickname,
                      nickname_preferred=nickname_preferred,
                      user_settings_id=new_user_settings.id,
                      last_login=last_login)


    # Add user to the session for flush
    model.db.session.add(user)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()


    user_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                   auditable_entity_type=model.CLASS_TO_ENUM_MAP['User'],
                                   related_entity_id=user.id,
                                   created_by_user_id=created_by_user_id,
                                   audit_details=audit_details)

    # Add the user_audit_entry to the session
    model.db.session.add(user_audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return user, user_audit_entry, new_user_settings, user_settings_audit_entry




def phone_number(phoneable_entity_type: model.PhoneableEntityTypes,
                 entity_id: int,
                 phone_type: model.PhoneType,
                 is_cell: bool,
                 country_code: int,
                 area_code: int,
                 phone_number: int,
                 created_by_user_id: int,
                 audit_details: Optional[str] = None,
                 extension: int = None,
                 is_verified: bool = False,
                 is_primary: bool = False,
                 commit: bool = True):
    """Create and return a Phone Number entry."""

    phone_number = model.PhoneNumber(phoneable_entity_type=phoneable_entity_type,
                                     entity_id=entity_id,
                                     phone_type=phone_type,
                                     is_cell=is_cell,
                                     country_code=country_code,
                                     area_code=area_code,
                                     phone_number=phone_number,
                                     extension=extension,
                                     is_verified=is_verified,
                                     is_primary=is_primary)

    # Add phone_number to the session for flush
    model.db.session.add(phone_number)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    phone_number_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                           auditable_entity_type=model.CLASS_TO_ENUM_MAP['PhoneNumber'],
                                           related_entity_id=phone_number.id,
                                           created_by_user_id=created_by_user_id,
                                           audit_details=audit_details)

    # Add the user_audit_entry to the session
    model.db.session.add(phone_number_audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return phone_number, phone_number_audit_entry




def email_address(emailable_entity_type: model.EmailableEntityTypes,
                  entity_id: int,
                  email_type: model.EmailType,
                  email_address: str,
                  created_by_user_id: int,
                  audit_details: Optional[str] = None,
                  is_verified: bool = False, 
                  is_primary: bool = None, 
                  is_shared: bool = None,
                  commit: bool = True):
    """Create and return a Email Address entry."""
    
    email_address = model.EmailAddress(emailable_entity_type=emailable_entity_type,
                                       entity_id=entity_id,
                                       email_type=email_type,
                                       email_address=email_address,
                                       is_verified=is_verified,
                                       is_primary=is_primary,
                                       is_shared=is_shared)

    # Add email_address to the session for flush
    model.db.session.add(email_address)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    email_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                    auditable_entity_type=model.CLASS_TO_ENUM_MAP['EmailAddress'],
                                    related_entity_id=email_address.id,
                                    created_by_user_id=created_by_user_id,
                                    audit_details=audit_details)

    # Add the user_audit_entry to the session
    model.db.session.add(email_audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return email_address, email_audit_entry




def file_attachment(attachable_entity_type: model.AttachableEntityTypes,
                    entity_id: int,
                    file_path: str, 
                    file_type: model.FileType,
                    file_category: model.FileCategory,
                    created_by_user_id: int,
                    audit_details: Optional[str] = None,
                    image_size: model.ImageSize = None,
                    commit: bool = True):
    """Create and return a File Attachment entry."""
    
    file_attachment = model.FileAttachment(attachable_entity_type=attachable_entity_type,
                                           entity_id=entity_id,
                                           file_path=file_path,
                                           file_type=file_type,
                                           file_category=file_category,
                                           image_size=image_size)

    # Add file_attachment to the session for flush
    model.db.session.add(file_attachment)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    file_attachment_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                              auditable_entity_type=model.CLASS_TO_ENUM_MAP['FileAttachment'],
                                              related_entity_id=file_attachment.id,
                                              created_by_user_id=created_by_user_id,
                                              audit_details=audit_details)

    # Add the user_audit_entry to the session
    model.db.session.add(file_attachment_audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return file_attachment, file_attachment_audit_entry




def user_role(user_id: int,
              role_id: int,
              created_by_user_id: int,
              audit_details: Optional[str] = None,
              commit: bool = True):
    """Create and return a User Role entry."""

    user_role = model.UserRole(user_id=user_id,
                               role_id=role_id)
    
    # Add user_role to the session for flush
    model.db.session.add(user_role)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    user_role_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                        auditable_entity_type=model.CLASS_TO_ENUM_MAP['UserRole'],
                                        related_entity_id=user_role.user_id,
                                        related_composite_id=user_role.role_id,
                                        created_by_user_id=created_by_user_id,
                                        audit_details=audit_details)

    # Add the audit_entry to the session
    model.db.session.add(user_role_audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return user_role, user_role_audit_entry




def role(name: str,
         description: str,
         created_by_user_id: int,
         audit_details: Optional[str] = None,
         commit: bool = True):
    """Create and return a Role entry."""

    role = model.Role(name=name,
                      description=description)
    
    # Add role to the session for flush
    model.db.session.add(role)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    role_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                        auditable_entity_type=model.CLASS_TO_ENUM_MAP['Role'],
                                        related_entity_id=role.id,
                                        created_by_user_id=created_by_user_id,
                                        audit_details=audit_details)

    # Add the audit_entry to the session
    model.db.session.add(role_audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return role, role_audit_entry




def role_permission(role_id: int,
                    permission_id: int,
                    created_by_user_id: int,
                    audit_details: Optional[str] = None,
                    commit: bool = True):
    """Create and return a Role Permission entry."""
    
    role_permission = model.RolePermission(role_id=role_id,
                                           permission_id=permission_id)
    
    # Add role_permission to the session for flush
    model.db.session.add(role_permission)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    role_permission_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                              auditable_entity_type=model.CLASS_TO_ENUM_MAP['RolePermission'],
                                              related_entity_id=role_permission.role_id,
                                              related_composite_id=role_permission.permission_id,
                                              created_by_user_id=created_by_user_id,
                                              audit_details=audit_details)

    # Add the audit_entry to the session
    model.db.session.add(role_permission_audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return role_permission, role_permission_audit_entry




def permission(name: str,
                description: str,
                created_by_user_id: int,
                audit_details: Optional[str] = None,
                commit: bool = True):
    """Create and return a Permission entry."""
    
    permission = model.Permission(name=name,
                                  description=description)

    # Add permission to the session for flush
    model.db.session.add(permission)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    permission_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                         auditable_entity_type=model.CLASS_TO_ENUM_MAP['Permission'],
                                         related_entity_id=permission.id,
                                         created_by_user_id=created_by_user_id,
                                         audit_details=audit_details)

    # Add audit_entry to the session
    model.db.session.add(permission_audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return permission, permission_audit_entry




def address(name: str,
            type: model.AddressType,
            street: str,
            city: str,
            state_id: int,
            zip: str,
            country_id: int,
            created_by_user_id: int,
            audit_details: Optional[str] = None,
            commit: bool = True):
    """Create and return a Address entry."""


    address = model.Address(name=name,
                            type=type,
                            street=street,
                            city=city,
                            state_id=state_id,
                            zip=zip,
                            country_id=country_id)
    
    # Add address to the session for flush
    model.db.session.add(address)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    address_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                      auditable_entity_type=model.CLASS_TO_ENUM_MAP['Address'],
                                      related_entity_id=address.id,
                                      created_by_user_id=created_by_user_id,
                                      audit_details=audit_details)

    # Add the audit_entry to the session
    model.db.session.add(address_audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return address, address_audit_entry




def area(name: str,
         created_by_user_id: int,
         parent_area_id: Optional[int] = None,
         audit_details: Optional[str] = None,
         latitude: Optional[float] = None,
         longitude: Optional[float] = None,
         address_id: Optional[int] = None,
         commit: bool = True):
    """Create and return an Area entry."""

    area = model.Area(parent_area_id=parent_area_id,
                      name=name,
                      latitude=latitude,
                      longitude=longitude,
                      address_id=address_id)
    
    # Add area to the session for flush
    model.db.session.add(area)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    area_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                   auditable_entity_type=model.CLASS_TO_ENUM_MAP['Area'],
                                   related_entity_id=area.id,
                                   created_by_user_id=created_by_user_id,
                                   audit_details=audit_details)

    # Add the audit_entry to the session
    model.db.session.add(area_audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return area, area_audit_entry




def manufacturer(name: str,
                 created_by_user_id: int,
                 audit_details: Optional[str] = None,
                 manufacturer_area_id: Optional[int] = None,
                 website: Optional[str] = None,
                 commit: bool = True):
    """Create and return a Manufacturer entry."""

    manufacturer = model.Manufacturer(name=name,
                                      manufacturer_area_id=manufacturer_area_id,
                                      website=website)
    
    # Add manufacturer to the session for flush
    model.db.session.add(manufacturer)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    manufacturer_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                           auditable_entity_type=model.CLASS_TO_ENUM_MAP['Manufacturer'],
                                           related_entity_id=manufacturer.id,
                                           created_by_user_id=created_by_user_id,
                                           audit_details=audit_details)

    # Add audit_entry to the session
    model.db.session.add(manufacturer_audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return manufacturer, manufacturer_audit_entry




def category(name: str,
             color_id: int,
             created_by_user_id: int,
             parent_category_id: Optional[int] = None,
             audit_details: Optional[str] = None,
             commit: bool = True):
    """Create and return a Category entry."""

    category = model.Category(parent_category_id=parent_category_id,
                              name=name,
                              color_id=color_id)
    
    # Add category to the session for flush
    model.db.session.add(category)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    category_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                       auditable_entity_type=model.CLASS_TO_ENUM_MAP['Category'],
                                       related_entity_id=category.id,
                                       created_by_user_id=created_by_user_id,
                                       audit_details=audit_details)

    # Add the audit_entry to the session
    model.db.session.add(category_audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return category, category_audit_entry




def asset(manufacturer_id: int,
          model_name: str,
          inventory_number: int,
          created_by_user_id: int,
          model_number: Optional[int] = None,
          category_id: Optional[int] = None,
          storage_area_id: Optional[int] = None,
          purchase_date: Optional[datetime] = None,
          purchase_price_id: Optional[int] = None,
          msrp_id: Optional[int] = None,
          residual_value_id: Optional[int] = None,
          parent_asset_id: Optional[int] = None,
          is_kit_root: bool = False,
          is_attachment: bool = False,
          serial_number: Optional[int] = None,
          description: Optional[str] = None,
          is_available: bool = True,
          online_item_page: Optional[str] = None,
          warranty_starts: Optional[datetime] = None,
          warranty_ends: Optional[datetime] = None,
          audit_details: Optional[str] = None,
          commit: bool = True):
    """Create and return an Asset entry."""

    asset = model.Asset(manufacturer_id=manufacturer_id,
                        model_number=model_number,
                        model_name=model_name,
                        category_id=category_id,
                        storage_area_id=storage_area_id,
                        purchase_date=purchase_date,
                        purchase_price_id=purchase_price_id,
                        msrp_id=msrp_id,
                        residual_value_id=residual_value_id,
                        parent_asset_id=parent_asset_id,
                        is_kit_root=is_kit_root,
                        is_attachment=is_attachment,
                        serial_number=serial_number,
                        inventory_number=inventory_number,
                        description=description,
                        is_available=is_available,
                        online_item_page=online_item_page,
                        warranty_starts=warranty_starts,
                        warranty_ends=warranty_ends)
    
    # Add asset to the session for flush
    model.db.session.add(asset)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    asset_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                    auditable_entity_type=model.CLASS_TO_ENUM_MAP['Asset'],
                                    related_entity_id=asset.id,
                                    created_by_user_id=created_by_user_id,
                                    audit_details=audit_details)

    # Add the audit_entry to the session
    model.db.session.add(asset_audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return asset, asset_audit_entry




def asset_tag(asset_id: int,
              code_type: model.AssetCodeType,
              data: str,
              created_by_user_id: int,
              audit_details: Optional[str] = None,
              commit: bool = True):
    """Create and return a Asset Tag entry."""
    
    asset_tag = model.AssetTag(asset_id=asset_id,
                               code_type=code_type,
                               data=data)

    # Add comment to the session for flush
    model.db.session.add(asset_tag)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    asset_tag_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                        auditable_entity_type=model.CLASS_TO_ENUM_MAP['AssetTag'],
                                        related_entity_id=asset_tag.id,
                                        created_by_user_id=created_by_user_id,
                                        audit_details=audit_details)

    # Add the user_audit_entry to the session
    model.db.session.add(asset_tag_audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return asset_tag, asset_tag_audit_entry




def asset_location_log(asset_id: int,
                       latitude: int,
                       longitude: int,
                       created_by_user_id: int,
                       audit_details: Optional[str] = None,
                       commit: bool = True):
    """Create and return an Asset Location Log entry."""
    
    asset_location_log = model.AssetLocationLog(asset_id=asset_id,
                                                latitude=latitude,
                                                longitude=longitude)

    # Add comment to the session for flush
    model.db.session.add(asset_location_log)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    asset_location_log_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                                 auditable_entity_type=model.CLASS_TO_ENUM_MAP['AssetLocationLog'],
                                                 related_entity_id=asset_location_log.id,
                                                 created_by_user_id=created_by_user_id,
                                                 audit_details=audit_details)

    # Add the user_audit_entry to the session
    model.db.session.add(asset_location_log_audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return asset_location_log, asset_location_log_audit_entry




def flag(name: str,
         color_id: int,
         created_by_user_id: int,
         description: Optional[str] = None,
         makes_unavailable: bool = False,
         audit_details: Optional[str] = None,
         commit: bool = True):
    """Create and return a Flag entry."""
    
    flag = model.Flag(name=name,
                      description=description,
                      color_id=color_id,
                      makes_unavailable=makes_unavailable)

    # Add comment to the session for flush
    model.db.session.add(flag)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    flag_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                   auditable_entity_type=model.CLASS_TO_ENUM_MAP['Flag'],
                                   related_entity_id=flag.id,
                                   created_by_user_id=created_by_user_id,
                                   audit_details=audit_details)

    # Add the user_audit_entry to the session
    model.db.session.add(flag_audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return flag, flag_audit_entry




def asset_flag(asset_id: int,
               flag_id: int,
               created_by_user_id: int,
               audit_details: Optional[str] = None,
               commit: bool = True):
    """Create and return an Asset Flag entry."""
    
    asset_flag = model.AssetFlag(asset_id=asset_id,
                                 flag_id=flag_id)
    
    # Add role_permission to the session for flush
    model.db.session.add(asset_flag)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    asset_flag_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                         auditable_entity_type=model.CLASS_TO_ENUM_MAP['AssetFlag'],
                                         related_entity_id=asset_flag.asset_id,
                                         related_composite_id=asset_flag.flag_id,
                                         created_by_user_id=created_by_user_id,
                                         audit_details=audit_details)

    # Add the audit_entry to the session
    model.db.session.add(asset_flag_audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return asset_flag, asset_flag_audit_entry




def custom_property(name: str,
                    data_type: model.CustomPropertyDataType,
                    created_by_user_id: int,
                    prefix: Optional[str] = None,
                    suffix: Optional[str] = None,
                    audit_details: Optional[str] = None,
                    commit: bool = True):
    """Create and return a Custom Property entry."""
    
    custom_property = model.CustomProperty(name=name,
                                           prefix=prefix,
                                           suffix=suffix,
                                           data_type=data_type)

    # Add comment to the session for flush
    model.db.session.add(custom_property)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    custom_property_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                              auditable_entity_type=model.CLASS_TO_ENUM_MAP['CustomProperty'],
                                              related_entity_id=custom_property.id,
                                              created_by_user_id=created_by_user_id,
                                              audit_details=audit_details)

    # Add the user_audit_entry to the session
    model.db.session.add(custom_property_audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return custom_property, custom_property_audit_entry




def asset_custom_property(asset_id: int,
                          custom_property_id: int,
                          data_value: str,
                          created_by_user_id: int,
                          audit_details: Optional[str] = None,
                          commit: bool = True):
    """Create and return an Asset Custom Property entry."""
    
    asset_custom_property = model.AssetCustomProperty(asset_id=asset_id,
                                                      custom_property_id=custom_property_id,
                                                      data_value=data_value)
    
    # Add role_permission to the session for flush
    model.db.session.add(asset_custom_property)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    asset_custom_property_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                                    auditable_entity_type=model.CLASS_TO_ENUM_MAP['AssetCustomProperty'],
                                                    related_entity_id=asset_custom_property.asset_id,
                                                    related_composite_id=asset_custom_property.custom_property_id,
                                                    created_by_user_id=created_by_user_id,
                                                    audit_details=audit_details)

    # Add the audit_entry to the session
    model.db.session.add(asset_custom_property_audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return asset_custom_property, asset_custom_property_audit_entry




def reservation(reserved_for: int,
                area_id: int,
                created_by_user_id: int,
                planned_checkout_time: Optional[datetime] = None,
                planned_checkin_time: Optional[datetime] = None,
                checkout_time: Optional[datetime] = None,
                checkin_time: Optional[datetime] = None,
                is_indefinite: bool = False,
                audit_details: Optional[str] = None,
                commit: bool = True):
    """Create and return a Reservation entry."""
    
    reservation = model.Reservation(reserved_for=reserved_for,
                                    area_id=area_id,
                                    planned_checkout_time=planned_checkout_time,
                                    planned_checkin_time=planned_checkin_time,
                                    checkout_time=checkout_time,
                                    checkin_time=checkin_time,
                                    is_indefinite=is_indefinite)

    # Add comment to the session for flush
    model.db.session.add(reservation)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    reservation_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                          auditable_entity_type=model.CLASS_TO_ENUM_MAP['Reservation'],
                                          related_entity_id=reservation.id,
                                          created_by_user_id=created_by_user_id,
                                          audit_details=audit_details)

    # Add the user_audit_entry to the session
    model.db.session.add(reservation_audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return reservation, reservation_audit_entry




def reservation_asset(reservation_id: int,
                      asset_id: int,
                      created_by_user_id: int,
                      audit_details: Optional[str] = None,
                      commit: bool = True):
    """Create and return a Reservation Asset entry."""
    
    reservation_asset = model.ReservationAsset(reservation_id=reservation_id,
                                               asset_id=asset_id)
    
    # Add role_permission to the session for flush
    model.db.session.add(reservation_asset)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    reservation_asset_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                                auditable_entity_type=model.CLASS_TO_ENUM_MAP['ReservationAsset'],
                                                related_entity_id=reservation_asset.reservation_id,
                                                related_composite_id=reservation_asset.asset_id,
                                                created_by_user_id=created_by_user_id,
                                                audit_details=audit_details)

    # Add the audit_entry to the session
    model.db.session.add(reservation_asset_audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return reservation_asset, reservation_asset_audit_entry




def comment(commentable_entity_type: model.CommentableEntityTypes, #Type hint
            entity_id: int,
            comment_data: str,
            created_by_user_id: int,
            parent_comment_id: Optional[int] = None,
            audit_details: Optional[str] = None,
            commit: bool = True):
    """Create and return a Comment entry."""
    
    comment = model.Comment(parent_comment_id=parent_comment_id,
                            commentable_entity_type=commentable_entity_type,
                            entity_id=entity_id,
                            comment_data=comment_data)

    # Add comment to the session for flush
    model.db.session.add(comment)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    comment_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                      auditable_entity_type=model.CLASS_TO_ENUM_MAP['Comment'],
                                      related_entity_id=comment.id,
                                      created_by_user_id=created_by_user_id,
                                      audit_details=audit_details)

    # Add the user_audit_entry to the session
    model.db.session.add(comment_audit_entry)

    # Commit only if commit=True
    if commit:
        model.db.session.commit()

    return comment, comment_audit_entry




def reaction(user_id: int,
             comment_id: int,
             reaction_type: model.ReactionType,
             created_by_user_id: int,
             audit_details: Optional[str] = None,
             commit: bool = True):
    """Create and return a Reaction entry."""

    reaction = model.Reaction(user_id=user_id,
                              role_id=comment_id,
                              reaction_type=reaction_type)
    
    # Add reaction to the session for flush
    model.db.session.add(reaction)
    # Flush to get id for this entity for the AuditEntry
    model.db.session.flush()

    reaction_audit_entry = audit_entry(operation_type=model.OperationType.CREATE.value,
                                       auditable_entity_type=model.CLASS_TO_ENUM_MAP['Reaction'],
                                       related_entity_id=reaction.id,
                                       created_by_user_id=created_by_user_id,
                                       audit_details=audit_details)

    # Add the audit_entry to the session
    model.db.session.add(reaction_audit_entry)
    
    # Commit only if commit=True
    if commit:
        model.db.session.commit()
    
    return reaction, reaction_audit_entry