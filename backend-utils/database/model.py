"""Models for PARM database."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import String, Integer, Boolean, Column, ForeignKey, SmallInteger, DateTime, Index
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declarative_base


# Create a Flask-SQLAlchemy instance to handle database interactions
db = SQLAlchemy()
# # Get the underlying engine from the Flask-SQLAlchemy instance for direct manipulation
# engine = db.engine


# Python Enum
class OperationType(PyEnum):  # Use the PyEnum alias here
    CREATE =    "CREATE"
    UPDATE =    "UPDATE"
    DELETE =    "DELETE"
    ARCHIVE =   "ARCHIVE"

# PostgreSQL ENUMs:
operation_type_enum = ENUM(
    *[e.value for e in OperationType],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='operation_type'
)



# Python Enum
class AuditableEntityTypes(PyEnum):  # Using the PyEnum alias here
    GLOBAL_SETTINGS =        "GLOBAL_SETTINGS"
    UI_THEME =               "UI_THEME"
    RESERVATION =            "RESERVATION"
    RESERVATION_ASSET =      "RESERVATION_ASSET"
    ASSET_TAG =              "ASSET_TAG"
    COMMENT =                "COMMENT"
    REACTION =               "REACTION"
    CATEGORY =               "CATEGORY"
    COLOR =                  "COLOR"
    CUSTOM_PROPERTY =        "CUSTOM_PROPERTY"
    ASSET_CUSTOM_PROPERTY =  "ASSET_CUSTOM_PROPERTY"
    ASSET =                  "ASSET"
    MANUFACTURER =           "MANUFACTURER"
    ASSET_FLAG =             "ASSET_FLAG"
    FLAG =                   "FLAG"
    CURRENCY =               "CURRENCY"
    FINANCIAL_ENTRY =        "FINANCIAL_ENTRY"
    ASSET_LOCATION_LOG =     "ASSET_LOCATION_LOG"
    FILE_ATTACHMENT =        "FILE_ATTACHMENT"
    EMAIL_ADDRESS =          "EMAIL_ADDRESS"
    PHONE_NUMBER =           "PHONE_NUMBER"
    USER_SETTINGS =          "USER_SETTINGS"
    USER =                   "USER"
    USER_ROLE =              "USER_ROLE"
    ROLE =                   "ROLE"
    PERMISSION =             "PERMISSION"
    ROLE_PERMISSION =        "ROLE_PERMISSION"
    AREA =                   "AREA"
    ADDRESS =                "ADDRESS"

# PostgreSQL ENUM
auditable_entity_types_enum = ENUM(
    *[e.value for e in AuditableEntityTypes],  # Use the PyEnum values to define the PostgreSQL ENUM
    name='auditable_entity_types'
)



# Python Enum
class CurrencyIsoCode(PyEnum):
    UNITED_STATES = "USD"
    CANADA =        "CAD"
    MEXICO =        "MXN"

# PostgreSQL ENUMs:
currency_iso_code_enum = ENUM(
    *[e.value for e in CurrencyIsoCode],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='currency_iso_code'
)



# Python Enum
class CountryIsoCode(PyEnum):
    UNITED_STATES = "US"
    CANADA =        "CA"
    MEXICO =        "MX"

# PostgreSQL ENUMs:
country_iso_code_enum = ENUM(
    *[e.value for e in CountryIsoCode],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='country_iso_code'
)



# Python Enum
class CountryName(PyEnum):
    UNITED_STATES = "United States"
    CANADA =        "Canada"
    MEXICO =        "Mexico"

# PostgreSQL ENUMs:
country_names_enum = ENUM(
    *[e.value for e in CountryName],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='country_iso_code'
)



# TODO: Look at this. Should it be split out to a separate list "approvals"?
# Python Enum
class ReservationStatus(PyEnum):
    PENDING =       "PENDING"
    APPROVED =      "APPROVED"
    CHECKED_OUT =   "CHECKED_OUT"
    COMPLETED =     "COMPLETED"
    CANCELLED =     "CANCELLED"
    DENIED =        "DENIED"

# PostgreSQL ENUMs:
reservation_status_enum = ENUM(
    *[e.value for e in ReservationStatus],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='reservation_status'
)



# Python Enum
class ScanCodeType(PyEnum):
    BARCODE =   "BARCODE"
    QR =        "QR"
    NFC =       "NFC"
    BLUETOOTH = "BLUETOOTH"

# PostgreSQL ENUMs:
asset_code_type_enum = ENUM(
    *[e.value for e in ScanCodeType],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='asset_code_type'
)



# Python Enum
class CustomPropertyDataType(PyEnum):
    VARCHAR =   "VARCHAR"
    INTEGER =   "INTEGER"
    NUMERIC =   "NUMERIC"
    REAL =      "REAL"
    BOOLEAN =   "BOOLEAN"
    TIMESTAMP = "TIMESTAMP"
    DATE =      "DATE"

# PostgreSQL ENUMs:
custom_property_data_type_enum = ENUM(
    *[e.value for e in CustomPropertyDataType],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='custom_property_data_type'
)



# Python Enum
class AttachableEntityTypes(PyEnum):  # Using the PyEnum alias here
    ASSET =   "ASSET"
    MANUFACTURER =   "MANUFACTURER"
    USER =    "USER"
    AREA =    "AREA"
    FLAG =    "FLAG"

# PostgreSQL ENUM
attachable_entity_types_enum = ENUM(
    *[e.value for e in AttachableEntityTypes],  # Use the PyEnum values to define the PostgreSQL ENUM
    name='attachable_entity_types'
)



# Python Enum
class FileCategory(PyEnum):
    ARCHIVE =       "ARCHIVE"
    DOCUMENT =      "DOCUMENT"
    SPREADSHEET =   "SPREADSHEET"
    PRESENTATION =  "PRESENTATION"
    IMAGE =         "IMAGE"
    VIDEO =         "VIDEO"
    AUDIO =         "AUDIO"

# PostgreSQL ENUMs:
file_category_enum = ENUM(
    *[e.value for e in FileCategory],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='file_category'
)



# Python Enum
class FileType(PyEnum):
    JPEG =      "JPEG"
    PNG =       "PNG"
    GIF =       "GIF"
    BMP =       "BMP"
    TIFF =      "TIFF"
    SVG =       "SVG"
    PDF =       "PDF"
    DOC =       "DOC"
    DOCX =      "DOCX"
    TXT =       "TXT"
    RTF =       "RTF"
    CSV =       "CSV"
    XLS =       "XLS"
    XLSX =      "XLSX"
    PPT =       "PPT"
    PPTX =      "PPTX"
    ZIP =       "ZIP"
    RAR =       "RAR"
    SEVENZIP =  "SEVENZIP"
    MP3 =       "MP3"
    WAV =       "WAV"
    MP4 =       "MP4"
    AVI =       "AVI"
    MKV =       "MKV"

# PostgreSQL ENUMs:
file_type_enum = ENUM(
    *[e.value for e in FileType],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='file_type'
)



# Python Enum
class ImageSize(PyEnum):

    ORIGINAL =  "0-original"
    XSMALL =    "1-xsmall"
    SMALL =     "2-small"
    MEDIUM =    "3-medium"
    LARGE =     "4-large"
    XLARGE =    "5-xlarge"
    MONGO =     "6-mongo"

# PostgreSQL ENUMs:
image_size_enum = ENUM(
    *[e.value for e in ImageSize],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='image_size'
)


# Python Enum
class EmailableEntityTypes(PyEnum):
    USER =         "USER"
    MANUFACTURER = "MANUFACTURER"
    AREA =         "AREA"

# PostgreSQL ENUMs:
emailable_entity_types_enum = ENUM(
    *[e.value for e in EmailableEntityTypes],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='emailable_entity_types'
)


# Python Enum
class EmailOwnerTypes(PyEnum):  # Using the PyEnum alias here
    USER =    "USER"
    COMPANY = "COMPANY"

# PostgreSQL ENUM
email_owner_types_enum = ENUM(
    *[e.value for e in EmailOwnerTypes],  # Use the PyEnum values to define the PostgreSQL ENUM
    name='email_owner_types'
)



# Python Enum
class EmailType(PyEnum):
    PERSONAL =  "PERSONAL"
    WORK =      "WORK"
    BUSINESS =  "BUSINESS"

# PostgreSQL ENUMs:
email_type_enum = ENUM(
    *[e.value for e in EmailType],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='email_type'
)


# Python Enum
class PhoneableEntityTypes(PyEnum):
    USER =         "USER"
    MANUFACTURER = "MANUFACTURER"
    AREA =         "AREA"

# PostgreSQL ENUMs:
phoneable_entity_types_enum = ENUM(
    *[e.value for e in PhoneableEntityTypes],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='phonable_entity_types'
)


# Python Enum
class PhoneOwnerTypes(PyEnum):  # Using the PyEnum alias here
    USER =    "USER"
    COMPANY = "COMPANY"

# PostgreSQL ENUM
phone_owner_types_enum = ENUM(
    *[e.value for e in PhoneOwnerTypes],  # Use the PyEnum values to define the PostgreSQL ENUM
    name='phone_owner_types'
)



class PhoneType(PyEnum):
    PERSONAL =  "PERSONAL"
    WORK =      "WORK"
    OTHER =     "OTHER"

# PostgreSQL ENUMs:
phone_type_enum = ENUM(
    *[e.value for e in PhoneType],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='phone_type'
)



# Python Enum
class AddressType(PyEnum):
    RESIDENTIAL =   "RESIDENTIAL"
    BUSINESS =      "BUSINESS"
    OTHER =         "OTHER"

# PostgreSQL ENUMs:
address_type_enum = ENUM(
    *[e.value for e in AddressType],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='address_type'
)



# Python Enum
class RelatedEntityType(PyEnum):
    COMMENT =       "COMMENT"
    ASSET =         "ASSET"
    RESERVATION =   "RESERVATION"
    AREA =          "AREA"

# PostgreSQL ENUMs:
related_entity_type_enum = ENUM(
    *[e.value for e in RelatedEntityType],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='related_entity_type'
)



# Python Enum
class CommentableEntityTypes(PyEnum):  # Using the PyEnum alias here
    COMMENT =       "COMMENT"
    ASSET =         "ASSET"
    RESERVATION =   "RESERVATION"
    AREA =          "AREA"
    FLAG =          "FLAG"

# PostgreSQL ENUM
commentable_entity_types_enum = ENUM(
    *[e.value for e in CommentableEntityTypes],  # Use the PyEnum values to define the PostgreSQL ENUM
    name='commentable_entity_types'
)



# Python Enum
class ReactionType(PyEnum):
    THUMBS_UP = "👍️"
    MAD =       "🤬"
    DEAD =      "💀"

# PostgreSQL ENUMs:
reaction_type_enum = ENUM(
    *[e.value for e in ReactionType],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='reaction_type'
)



# Python Enum
class TimezoneIdentifier(PyEnum):
    UTC =           "Universal Coordinated Time"
    NEW_YORK =      "America/New_York"
    CHICAGO =       "America/Chicago"
    DENVER =        "America/Denver"
    LOS_ANGELES =   "America/Los_Angeles"
    PHOENIX =       "America/Phoenix"
    ANCHORAGE =     "America/Anchorage"
    JUNEAU =        "America/Juneau"
    HONOLULU =      "America/Honolulu"

# PostgreSQL ENUMs:
timezone_identifier_enum = ENUM(
    *[e.value for e in TimezoneIdentifier],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='timezone_identifier'
)



# Python Enum
class TimezoneAbbreviation(PyEnum):
    UTC =       "UTC"
    EASTERN =   "EST"
    CENTRAL =   "CST"
    MOUNTAIN =  "MST"
    PACIFIC =   "PST"
    ALASKAN =   "AKST"
    HAWIIAN =   "HST"

# PostgreSQL ENUMs:
timezone_abbreviation_enum = ENUM(
    *[e.value for e in TimezoneAbbreviation],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='timezone_abbreviation'
)



# Python Enum
class StateCodes(PyEnum):
    AL = "AL"
    AK = "AK"
    AZ = "AZ"
    AR = "AR"
    CA = "CA"
    CO = "CO"
    CT = "CT"
    DE = "DE"
    FL = "FL"
    GA = "GA"
    HI = "HI"
    ID = "ID"
    IL = "IL"
    IN = "IN"
    IA = "IA"
    KS = "KS"
    KY = "KY"
    LA = "LA"
    ME = "ME"
    MD = "MD"
    MA = "MA"
    MI = "MI"
    MN = "MN"
    MS = "MS"
    MO = "MO"
    MT = "MT"
    NE = "NE"
    NV = "NV"
    NH = "NH"
    NJ = "NJ"
    NM = "NM"
    NY = "NY"
    NC = "NC"
    ND = "ND"
    OH = "OH"
    OK = "OK"
    OR = "OR"
    PA = "PA"
    RI = "RI"
    SC = "SC"
    SD = "SD"
    TN = "TN"
    TX = "TX"
    UT = "UT"
    VT = "VT"
    VA = "VA"
    WA = "WA"
    WV = "WV"
    WI = "WI"
    WY = "WY"

# PostgreSQL ENUMs:
state_codes_enum = ENUM(
    *[e.value for e in StateCodes],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='state_codes'
)



# Python Enum
class StateNames(PyEnum):
    ALABAMA =           "Alabama"
    ALASKA =            "Alaska"
    ARIZONA =           "Arizona"
    ARKANSAS =          "Arkansas"
    CALIFORNIA =        "California"
    COLORADO =          "Colorado"
    CONNECTICUT =       "Connecticut"
    DELAWARE =          "Delaware"
    FLORIDA =           "Florida"
    GEORGIA =           "Georgia"
    HAWAII =            "Hawaii"
    IDAHO =             "Idaho"
    ILLINOIS =          "Illinois"
    INDIANA =           "Indiana"
    IOWA =              "Iowa"
    KANSAS =            "Kansas"
    KENTUCKY =          "Kentucky"
    LOUISIANA =         "Louisiana"
    MAINE =             "Maine"
    MARYLAND =          "Maryland"
    MASSACHUSETTS =     "Massachusetts"
    MICHIGAN =          "Michigan"
    MINNESOTA =         "Minnesota"
    MISSISSIPPI =       "Mississippi"
    MISSOURI =          "Missouri"
    MONTANA =           "Montana"
    NEBRASKA =          "Nebraska"
    NEVADA =            "Nevada"
    NEW_HAMPSHIRE =     "New Hampshire"
    NEW_JERSEY =        "New Jersey"
    NEW_MEXICO =        "New Mexico"
    NEW_YORK =          "New York"
    NORTH_CAROLINA =    "North Carolina"
    NORTH_DAKOTA =      "North Dakota"
    OHIO =              "Ohio"
    OKLAHOMA =          "Oklahoma"
    OREGON =            "Oregon"
    PENNSYLVANIA =      "Pennsylvania"
    RHODE_ISLAND =      "Rhode Island"
    SOUTH_CAROLINA =    "South Carolina"
    SOUTH_DAKOTA =      "South Dakota"
    TENNESSEE =         "Tennessee"
    TEXAS =             "Texas"
    UTAH =              "Utah"
    VERMONT =           "Vermont"
    VIRGINIA =          "Virginia"
    WASHINGTON =        "Washington"
    WEST_VIRGINIA =     "West Virginia"
    WISCONSIN =         "Wisconsin"
    WYOMING =           "Wyoming"

# PostgreSQL ENUMs:
state_names_enum = ENUM(
    *[e.value for e in StateNames],   # Use the PythonEnum(PyEnum) values to define the PostgreSQL ENUM
    name='state_names'
)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CLASS_TO_ENUM_MAP = {
    # Auditable Classes
    'GlobalSettings': 'GLOBAL_SETTINGS',
    'UiTheme': 'UI_THEME',
    'Reservation': 'RESERVATION',
    'ReservationAsset': 'RESERVATION_ASSET',
    'AssetTag': 'ASSET_TAG',
    'Comment': 'COMMENT',
    'Reaction': 'REACTION',
    'Category': 'CATEGORY',
    'Color': 'COLOR',
    'CustomProperty': 'CUSTOM_PROPERTY',
    'AssetCustomProperty': 'ASSET_CUSTOM_PROPERTY',
    'Asset': 'ASSET',
    'Manufacturer': 'MANUFACTURER',
    'AssetFlag': 'ASSET_FLAG',
    'Flag': 'FLAG',
    'Currency': 'CURRENCY',
    'FinancialEntry': 'FINANCIAL_ENTRY',
    'AssetLocationLog': 'ASSET_LOCATION_LOG',
    'FileAttachment': 'FILE_ATTACHMENT',
    'EmailAddress': 'EMAIL_ADDRESS',
    'PhoneNumber': 'PHONE_NUMBER',
    'UserSettings': 'USER_SETTINGS',
    'User': 'USER',
    'UserRole': 'USER_ROLE',
    'Role': 'ROLE',
    'Permission': 'PERMISSION',
    'RolePermission': 'ROLE_PERMISSION',
    'Area': 'AREA',
    'Address': 'ADDRESS'
    }

# Get Audit Type Base Class for auditable model classes
class AuditableBase(db.Model):
    __abstract__ = True  # Make sure SQLAlchemy knows this is an abstract base class




    def get_audit_type(self):
        class_name = self.__class__.__name__
        return CLASS_TO_ENUM_MAP.get(class_name, class_name.upper())

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



class GlobalSettings(AuditableBase):
    """Settings and Defaults for the entire app."""

    __tablename__ = "global_settings"

    deployment_fingerprint = db.Column(db.String(64), primary_key=True, nullable=False)
    default_currency_id = db.Column(db.SmallInteger, db.ForeignKey('currencies.id'), nullable=False)

    # Relationship for easier ORM-based lookups
    default_currency = db.relationship("Currency")

    def __repr__(self):
        return f'<GlobalSettings fingerprint={self.deployment_fingerprint} currency_settings={self.default_currency_id}>'


    

class AuditEntry(db.Model):
    """Audit info for changes."""

    __tablename__ = "audit_entries"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    operation_type = db.Column(operation_type_enum, nullable=False)  
    auditable_entity_type = db.Column(auditable_entity_types_enum, nullable=False)  
    related_entity_id = db.Column(db.Integer, nullable=True)
    related_entity_hash = db.Column(db.String(64), nullable=True)  
    related_composite_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    last_edited_by = db.Column(db.Integer, ForeignKey('users.id'), nullable=True)
    last_edited_at = db.Column(db.DateTime, nullable=False)
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    archived_at = db.Column(db.DateTime, nullable=True)

    creator = db.relationship('User', foreign_keys=[created_by])
    edited_by_user = db.relationship('User', foreign_keys=[last_edited_by])

    __table_args__ = (
        Index('idx_related_entity_type', 'auditable_entity_type'),
        Index('idx_related_entity_id', 'related_entity_id'),
        Index('idx_related_entity_hash', 'related_entity_hash'),
        Index('idx_related_composite_id', 'related_composite_id'),
        Index('idx_related_entity_type_id', 'auditable_entity_type', 'related_entity_id'),
        Index('idx_related_entity_type_composite_id', 'auditable_entity_type', 'related_composite_id'),
        Index('idx_created_by', 'created_by'),
        Index('idx_is_archived', 'is_archived')
    )

    def __repr__(self):
        return f'<AuditEntry id={self.id} operation_type={self.operation_type} auditable_entity_type={self.auditable_entity_type} related_entity_id={self.related_entity_id}>'



class Reservation(AuditableBase):
    """Reservations."""

    __tablename__ = "reservations"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    reserved_for = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    planned_checkout_time = db.Column(db.DateTime, nullable=True)
    planned_checkin_time = db.Column(db.DateTime, nullable=True)
    checkout_time = db.Column(db.DateTime, nullable=True)
    checkin_time = db.Column(db.DateTime, nullable=True)
    is_indefinite = db.Column(db.Boolean, nullable=False, default=False)

    __table_args__ = (
        Index('idx_area_id', 'area_id'),
        Index('idx_reserved_for', 'reserved_for'),
        Index('idx_planned_checkout_time', 'planned_checkout_time'),
        Index('idx_planned_checkin_time', 'planned_checkin_time'),
    )

    def __repr__(self):
        return f"<Reservation id={self.id} reserved_for={self.reserved_for} area_id={self.area_id}>"



class ReservationAsset(AuditableBase):
    """Reservation Assets."""

    __tablename__ = "reservation_assets"

    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'), primary_key=True, nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), primary_key=True, nullable=False)
    
    reservation = db.relationship('Reservation', backref='asset_relationships')
    asset = db.relationship('Asset', backref='reservation_relationships')

    __table_args__ = (
        Index('idx_reservation_id', 'reservation_id'),
        Index('idx_asset_id', 'asset_id'),
        Index('idx_reservation_asset', 'reservation_id', 'asset_id'),
    )
    
    def __repr__(self):
        return f"<ReservationAsset reservation_id={self.reservation_id} asset_id={self.asset_id}>"



class AssetTag(AuditableBase):
    """Some form of scannable tag that is attached to an asset."""

    __tablename__ = "asset_tags"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    code_type = db.Column(asset_code_type_enum, nullable=False)
    data = db.Column(db.String(3072), nullable=False)

    asset = db.relationship('Asset', backref='tags')

    __table_args__ = (
        Index('idx_asset_id', 'asset_id'),
        Index('idx_code_type', 'code_type'),
        Index('idx_asset_id_code_type', 'asset_id', 'code_type'),
    )

    def __repr__(self):
        return f'<AssetTag id={self.id} asset_id={self.asset_id} code_type={self.code_type}>'



class Comment(AuditableBase):
    """Comments."""

    __tablename__ = "comments"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    commentable_entity_type = db.Column(commentable_entity_types_enum, nullable=False)  # Using the PostgreSQL ENUM type
    entity_id = db.Column(db.Integer, nullable=False)
    comment_data = db.Column(db.String(2048), nullable=False)

    # Relationship to represent the parent comment.
    parent = db.relationship('Comment', remote_side=[id], backref=db.backref('nested_comments', lazy='dynamic'))

    __table_args__ = (
        Index('idx_commentable_entity_types', 'commentable_entity_type'),
        Index('idx_related_entity_id', 'entity_id'),
        Index('idx_commentable_entity_type_id', 'commentable_entity_type', 'entity_id'),
        Index('idx_parent_comment_id', 'parent_comment_id'),
        Index('idx_parent_comment_id_id', 'parent_comment_id', 'id')
    )
    
    def __repr__(self):
        return f'<Comment id={self.id} commentable_entity_type={self.commentable_entity_type} entity_id={self.entity_id}>'



class Reaction(AuditableBase):
    """Join Table. Something like an emoji reaction to a comment."""

    __tablename__ = "reactions"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
    reaction_type = db.Column(reaction_type_enum, nullable=False)

    user = db.relationship('User', backref='reactions')
    comment = db.relationship('Comment', backref='reactions')

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_comment_id', 'comment_id'),
        Index('idx_user_comment_reaction', 'user_id', 'comment_id', 'reaction_type')
    )

    def __repr__(self):
        return f"<Reaction user_id={self.user_id} comment_id={self.comment_id}>"



class Category(AuditableBase):
    """A category for assets."""

    __tablename__ = "categories"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    parent_category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    name = db.Column(db.String(64), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'), nullable=False)

    # Relationship to represent the parent category.
    parent = db.relationship('Category', remote_side=[id], backref=db.backref('subcategories', lazy='dynamic'))

    __table_args__ = (
        Index('idx_parent_category_id', 'parent_category_id'),
        Index('idx_name', 'name'),
        Index('idx_parent_category_name', 'parent_category_id', 'name')
    )

    def __repr__(self):
        return f'<Category id={self.id} name={self.name}>'



class Color(AuditableBase):
    """Custom property / field to be added ale-cart to assets."""

    __tablename__ = "colors"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False, unique=True)
    hex_value = db.Column(db.String(7), nullable=False, unique=True)
        
    def __repr__(self):
        return f'<Color id={self.id} name={self.name} hex_value={self.hex_value}>'



class CustomProperty(AuditableBase):
    """Custom property / field to be added ale-cart to assets."""

    __tablename__ = "custom_properties"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False, unique=True)
    prefix = db.Column(db.String(8), nullable=True)
    suffix = db.Column(db.String(8), nullable=True)
    data_type = db.Column(custom_property_data_type_enum, nullable=False)

    __table_args__ = (
        Index('idx_data_type', 'data_type'),
    )

    def __repr__(self):
        return f'<CustomProperty id={self.id} name={self.name} data_type={self.data_type}>'



class AssetCustomProperty(AuditableBase):
    """Join Table. Custom properties associated with assets."""

    __tablename__ = "asset_custom_properties"

    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), primary_key=True, nullable=False)
    custom_property_id = db.Column(db.Integer, db.ForeignKey('custom_properties.id'), primary_key=True, nullable=False)
    data_value = db.Column(db.String(512), nullable=False)

    asset = db.relationship('Asset', backref='associated_custom_properties')
    custom_property = db.relationship('CustomProperty', backref='associated_assets')

    __table_args__ = (
        Index('idx_asset_id', 'asset_id'),
        Index('idx_custom_property_id', 'custom_property_id'),
        Index('idx_asset_custom_property', 'asset_id', 'custom_property_id')
    )

    def __repr__(self):
        return f"<AssetCustomProperty asset_id={self.asset_id} custom_property_id={self.custom_property_id}>"



class Asset(AuditableBase):
    """An asset."""

    __tablename__ = "assets"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    manufacturer_id = db.Column(db.SmallInteger, db.ForeignKey('manufacturers.id'), nullable= False)
    model_number = db.Column(db.String(64), nullable=True)
    model_name = db.Column(db.String(64), nullable=False)
    category_id = db.Column(db.SmallInteger, db.ForeignKey('categories.id'), nullable= True)
    storage_area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable= True)
    purchase_date = db.Column(db.DateTime, nullable=True)
    purchase_price_id = db.Column(db.Integer, db.ForeignKey('financial_entries.id'), nullable= True)
    msrp_id = db.Column(db.Integer, db.ForeignKey('financial_entries.id'), nullable= True)
    residual_value_id = db.Column(db.Integer, db.ForeignKey('financial_entries.id'), nullable= True)
    parent_asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable= True)
    is_kit_root = db.Column(db.Boolean, nullable=False, default=False)
    is_attachment = db.Column(db.Boolean, nullable=False, default=False)
    serial_number = db.Column(db.String(256), nullable=True)
    inventory_number = db.Column(db.SmallInteger, nullable=False) # Unique number for each item within the same brand and model.
    description = db.Column(db.String(512), nullable=True)
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    online_item_page = db.Column(db.String, nullable=True)
    warranty_starts = db.Column(db.DateTime, nullable=True)
    warranty_ends = db.Column(db.DateTime, nullable=True)
    
    manufacturer = db.relationship('Manufacturer', backref= 'assets')
    category = db.relationship('Category', backref= 'assets')
    area = db.relationship('Area', backref= 'assets')
    purchase_price_entry = db.relationship('FinancialEntry', foreign_keys=[purchase_price_id], backref='purchase_price_assets')
    msrp_entry = db.relationship('FinancialEntry', foreign_keys=[msrp_id], backref='msrp_assets')
    residual_value_entry = db.relationship('FinancialEntry', foreign_keys=[residual_value_id], backref='residual_value_assets')

    __table_args__ = (
        Index('idx_manufacturer_id', 'manufacturer_id'),
        Index('idx_category_id', 'category_id'),
        Index('idx_storage_area_id', 'storage_area_id'),  # New index
        Index('idx_parent_asset_id', 'parent_asset_id'),  # New index
        Index('idx_is_kit_root', 'is_kit_root'),  # New index
        Index('idx_is_attachment', 'is_attachment'),  # New index
        Index('idx_is_available', 'is_available'),  # New index
        Index('idx_inventory_number', 'inventory_number'),  # New index
    )
    
    def __repr__(self):
        return f'<Asset id={self.id} model_name={self.model_name}>'



class Manufacturer(AuditableBase):
    """Brand/Manufacturer/Company"""

    __tablename__ = "manufacturers"

    id = db.Column(db.SmallInteger, autoincrement=True, primary_key=True, nullable=False)  # Changed to SmallInteger
    name = db.Column(db.String(64), nullable=False, unique=True)
    manufacturer_area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=True)
    website = db.Column(db.String(512), nullable=True)

    __table_args__ = (
        Index('idx_manufacturer_area_id', 'manufacturer_area_id'),
        Index('idx_website', 'website'),
    )

    area = db.relationship('Area', backref='manufacturers')
    
    def __repr__(self):
        return f'<Manufacturer id={self.id} name={self.name}>'



class AssetFlag(AuditableBase):
    """Join Table. The connection between a flag and an asset."""

    __tablename__ = "asset_flags"

    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), primary_key=True, nullable=False)
    flag_id = db.Column(db.Integer, db.ForeignKey('flags.id'), primary_key=True, nullable=False)

    __table_args__ = (
        Index('idx_asset_flag', 'asset_id', 'flag_id'),
    )

    asset = db.relationship('Asset', backref='associated_flags')
    flag = db.relationship('Flag', backref='associated_assets')
    
    def __repr__(self):
        return f"<AssetFlag asset_id={self.asset_id} flag_id={self.flag_id}>"




class Flag(AuditableBase):
    """Flags to callout something about an entity."""

    __tablename__ = "flags"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String(512), nullable=True)  # Changed to nullable=True
    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'), nullable=False)
    makes_unavailable = db.Column(db.Boolean, nullable=False, default=False)

    __table_args__ = (
        Index('idx_color_id', 'color_id'),
        Index('idx_makes_unavailable', 'makes_unavailable'),
        Index('idx_name', 'name'),
    )

    color = db.relationship('Color', backref='flags')
    
    def __repr__(self):
        return f'<Flag id={self.id} name={self.name} makes_unavailable={self.makes_unavailable}>'



class Currency(AuditableBase):
    """A currency model representing different global currencies."""

    __tablename__ = "currencies"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)  # Name of the currency
    symbol = db.Column(db.String(8), nullable=False)  # Symbol of the currency
    iso_code = db.Column(currency_iso_code_enum, nullable=False)
    exchange_rate = db.Column(db.Numeric( 10, 5 ), nullable=False)

    __table_args__ = (
        Index('idx_name', 'name'),
        Index('idx_symbol', 'symbol'),
        Index('idx_iso_code', 'iso_code'),
    )

    def __repr__(self):
        return f'<Currency id={self.id} name={self.name} symbol={self.symbol}>'
    


class FinancialEntry(AuditableBase):
    """Track financial entries across the database."""

    __tablename__ = "financial_entries"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=False)
    amount = db.Column(db.Numeric( 10, 2 ), nullable=False)

    __table_args__ = (
        Index('idx_currency_id', 'currency_id'),
        Index('idx_amount', 'amount'),
    )
    
    currency = db.relationship('Currency', backref='financial_entries')
    
    def __repr__(self):
        return f'<FinancialEntry id={self.id} currency_id={self.currency_id} amount={self.amount}>'



class AssetLocationLog(AuditableBase):
    """Logs to keep track everytime an asset is scanned."""

    __tablename__ = "asset_location_logs"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    latitude = db.Column(db.Numeric(9, 6), nullable=True)
    longitude = db.Column(db.Numeric(9, 6), nullable=True)

    __table_args__ = (
        Index('idx_asset_id', 'asset_id'),
        Index('idx_lat_long', 'latitude', 'longitude'),
    )
    
    asset = db.relationship('Asset', backref='location_logs')
      
    def __repr__(self):
        return f'<AssetLocationLog id={self.id} asset_id={self.asset_id} lat={self.latitude} long={self.longitude}>'



class FileAttachment(AuditableBase):
    """Files. Can be images, video, or documents."""

    __tablename__ = "file_attachments"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    attachable_entity_type = db.Column(attachable_entity_types_enum, nullable=False)  # Using the PostgreSQL ENUM type
    entity_id = db.Column(db.Integer, nullable=False)

    file_path = db.Column(db.String, unique=True, nullable=False)  # Path or URL to the actual file
    file_type = db.Column(file_type_enum, nullable=False)
    file_category = db.Column(file_category_enum, nullable=False)
    image_size = db.Column(image_size_enum, nullable=True)

    __table_args__ = (
        Index('idx_attachable_entity_type', 'attachable_entity_type'),
        Index('idx_related_entity_id', 'entity_id'),
        Index('idx_attachable_entity_type_id', 'attachable_entity_type', 'entity_id'),
        Index('idx_file_type', 'file_type'),  # New index
        Index('idx_file_category', 'file_category')  # New index
    )
    
    def __repr__(self):
        return f"<FileAttachment id={self.id} file_type={self.file_type} attachable_entity_type={self.attachable_entity_type} related_entity_id={self.related_entity_id}>"



class EmailAddress(AuditableBase):
    """Email Address."""

    __tablename__ = "email_addresses"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    emailable_entity_type = db.Column(emailable_entity_types_enum, nullable=False)  # Using the PostgreSQL ENUM type
    entity_id = db.Column(db.Integer, nullable=False)

    email_type = db.Column(email_type_enum, nullable=False)
    email_address = db.Column(db.String(64), unique=True, nullable=False)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    is_primary = db.Column(db.Boolean, nullable=True)
    is_shared = db.Column(db.Boolean, nullable=True)

    __table_args__ = (
        Index('idx_email_owner_type', 'emailable_entity_type'),
        Index('idx_related_owner_id', 'entity_id'),
        Index('idx_email_owner_type_id', 'email_type', 'entity_id'),
        Index('idx_is_verified', 'is_verified'),
        Index('idx_email_address', 'email_address')  # New index
    )
    
    def __repr__(self):
        return f"<EmailAddress id={self.id} email_type={self.email_type} email_address={self.email_address}>"



class PhoneNumber(AuditableBase):
    """Phone Number."""

    __tablename__ = "phone_numbers"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    phoneable_entity_type = db.Column(phoneable_entity_types_enum, nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)

    phone_type = db.Column(phone_type_enum, nullable=False)
    is_cell = db.Column(db.Boolean, nullable=False)
    country_code = db.Column(db.SmallInteger, nullable=False)
    area_code = db.Column(db.SmallInteger, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    extension = db.Column(db.SmallInteger, nullable=True)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    is_primary = db.Column(db.Boolean, nullable=False)

    __table_args__ = (
        Index('idx_phone_owner_type', 'phone_type'),
        Index('idx_related_owner_id', 'entity_id'),
        Index('idx_phone_owner_type_id', 'phone_type', 'entity_id'),
        Index('idx_is_verified', 'is_verified'),
        Index('idx_phone_number', 'phone_number')
    )
    
    def __repr__(self):
        return f"<PhoneNumber id={self.id} phone_type={self.phone_type} phone_number={self.phone_number}>"





class UiTheme(AuditableBase):
    """Name and values for UI Themes."""

    __tablename__ = "ui_themes"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String(512), nullable=False)
    primary_color_id = db.Column(db.Integer, db.ForeignKey('colors.id'), nullable=False)
    secondary_color_id = db.Column(db.Integer, db.ForeignKey('colors.id'), nullable=False)
    
    # Specifying the foreign_keys for each relationship
    primary_color_relation = db.relationship('Color', foreign_keys=[primary_color_id], backref='ui_theme_primary')
    secondary_color_relation = db.relationship('Color', foreign_keys=[secondary_color_id], backref='ui_theme_secondary')

    __table_args__ = (
        Index('idx_primary_color_id', 'primary_color_id'),
        Index('idx_secondary_color_id', 'secondary_color_id')
    )
    
    def __repr__(self):
        return f'<UiTheme id={self.id} name={self.name} primary_color_id={self.primary_color_id} secondary_color_id={self.secondary_color_id}>'




class UserSettings(AuditableBase):
    """Settings and Defaults for the entire app."""

    __tablename__ = "user_settings"

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    currency_id = Column(SmallInteger, ForeignKey('currencies.id'), nullable=False)
    time_format_is_24h = Column(Boolean, nullable=False, default=True)
    ui_theme_id = Column(SmallInteger, ForeignKey('ui_themes.id'), nullable=False)

    # Specifying the foreign_keys for each relationship
    currency = db.relationship('Currency', backref='user_settings')
    ui_theme = db.relationship('UiTheme', backref='user_settings')
    
    def __repr__(self):
        return f'<UserSettings id={self.id} currency_id={self.currency_id} time_format_is_24h={self.time_format_is_24h}>'





class User(AuditableBase):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    middle_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=False)
    nickname = db.Column(db.String(64), nullable=True)
    nickname_preferred = db.Column(db.Boolean, nullable=True)
    user_settings_id = db.Column(db.Integer, db.ForeignKey('user_settings.id'), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationship
    user_settings = db.relationship('UserSettings', backref='user')

    # Indexes
    __table_args__ = (
        Index('idx_last_login', 'last_login'),
    )

    def __repr__(self):
        return f'<User id={self.id} first_name={self.first_name} last_name={self.last_name}>'



class UserRole(AuditableBase):
    """Track when a user was assigned a specific role."""

    __tablename__ = "user_roles"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True, nullable=False)

    # Relationships
    user = db.relationship('User', backref='role_relationships')
    role = db.relationship('Role', backref='user_relationships')

    # Indexes
    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_role_id', 'role_id'),
    )

    def __repr__(self):
        return f'<UserRole user_id={self.user_id} role_id={self.role_id}>'



class Role(AuditableBase):
    """Role for user assignment."""

    __tablename__ = "roles"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String(512), nullable=False)
        
    def __repr__(self):
        return f'<Role id={self.id} name={self.name}>'



class Permission(AuditableBase):
    """Permissions for app access and control."""

    __tablename__ = "permissions"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String(512), nullable=False)
        
    def __repr__(self):
        return f'<Permission id={self.id} name={self.name}>'



class RolePermission(AuditableBase):
    """Track when a role was granted a particular permission."""

    __tablename__ = "role_permissions"

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True, nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), primary_key=True, nullable=False)

    # Relationships
    role = db.relationship('Role', backref='permission_relationships')
    permission = db.relationship('Permission', backref='role_relationships')

    # Indexes
    __table_args__ = (
        Index('idx_role_id', 'role_id'),
        Index('idx_permission_id', 'permission_id'),
    )

    def __repr__(self):
        return f'<RolePermission role_id={self.role_id} permission_id={self.permission_id}>'



class Area(AuditableBase):
    """Areas."""

    __tablename__ = "areas"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    parent_area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=True)
    name = db.Column(db.String(64), nullable=False)
    latitude = db.Column(db.Numeric(9, 6), nullable=True)
    longitude = db.Column(db.Numeric(9, 6), nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=True)

    # Relationships
    parent = db.relationship('Area', remote_side=[id], backref=db.backref('nested_areas', lazy='dynamic'))
    address = db.relationship('Address', backref='addresses')

    # Indexes
    __table_args__ = (
        Index('idx_parent_area_id', 'parent_area_id'),
        Index('idx_name', 'name'),
        Index('idx_address_id', 'address_id'),
    )

    def __repr__(self):
        return f'<Area id={self.id} name={self.name}>'

    

class Address(AuditableBase):
    """A street address."""
    
    __tablename__ = "addresses"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)  # The name of the address for the User. IE "Empire State Building"
    type = db.Column(address_type_enum, nullable=False)  # Using the PostgreSQL ENUM type
    street = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    zip = db.Column(db.String(16), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)

    # Relationships
    state = db.relationship('State', backref='addresses')
    country = db.relationship('Country', backref='addresses')

    # Indexes
    __table_args__ = (
        Index('idx_state_id', 'state_id'),
        Index('idx_country_id', 'country_id'),
        Index('idx_type', 'type'),
    )

    def __repr__(self):
        return f'<Address id={self.id} name={self.name} type={self.type}>'



class Country(db.Model):
    """A country from the globe."""
    
    __tablename__ = "countries"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    code = db.Column(country_iso_code_enum, nullable=False)  # Using the PostgreSQL ENUM type
    name = db.Column(country_names_enum, nullable=False)  # Using the PostgreSQL ENUM type
    intl_phone_code = db.Column(db.SmallInteger, nullable=False)  # You'll have to implement length restrictions in the app

    # Indexes
    __table_args__ = (
        Index('idx_code', 'code'),
        Index('idx_intl_phone_code', 'intl_phone_code'),
    )

    def __repr__(self):
        return f'<Country id={self.id} name={self.name} code={self.code}>'



class Timezone(db.Model):
    """A timezone as represented by enums."""
    
    __tablename__ = "timezones"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    identifier = db.Column(timezone_identifier_enum, nullable=False)  # Using the PostgreSQL ENUM type
    abbreviation = db.Column(timezone_abbreviation_enum, nullable=False)  # Using the PostgreSQL ENUM type
    utc_offset_minutes = db.Column(db.SmallInteger, nullable=False)
    has_dst = db.Column(db.Boolean, nullable=False)

    # Indexes
    __table_args__ = (
        Index('idx_identifier', 'identifier'),
        Index('idx_abbreviation', 'abbreviation'),
    )

    def __repr__(self):
        return f'<Timezone id={self.id} identifier={self.identifier}>'



class State(db.Model):
    """A state from the United States."""
    
    __tablename__ = "states"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    code = db.Column(state_codes_enum, nullable=False)  # Using the PostgreSQL ENUM type
    name = db.Column(state_names_enum, nullable=False)  # Using the PostgreSQL ENUM type
    timezone_id = db.Column(db.Integer, db.ForeignKey('timezones.id'), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)

    # Relationships
    timezone = db.relationship('Timezone', backref='states')
    country = db.relationship('Country', backref='states')

    # Indexes
    __table_args__ = (
        Index('idx_timezone_id', 'timezone_id'),
        Index('idx_country_id', 'country_id'),
        Index('idx_code', 'code'),
        Index('idx_name', 'name'),
    )

    def __repr__(self):
        return f'<State id={self.id} name={self.name} code={self.code}>'




def connect_to_db(flask_app, db_uri="postgresql:///parm", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)