"""Models for PARM database."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey, Enum
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy.dialects.postgresql import ENUM

db = SQLAlchemy()


# PostgreSQL ENUMs:
operation_type_enum = ENUM(
    'create', 'update', 'delete', 'archive',
    name='operation_type'
)

currency_iso_code_enum = ENUM(
    'usd', 'cad', 'mxn',
    name='currency_iso_code'
)

country_iso_code_enum = ENUM(
    'us', 'ca', 'mx',
    name='country_iso_code'
)

reservation_status_enum = ENUM(
    'pending', 'approved', 'checked_out', 'completed', 'cancelled', 'denied',
    name='reservation_status'
)

scan_code_type_enum = ENUM(
    'barcode', 'qr', 'nfc', 'bluetooth',
    name='scan_code_type'
)

custom_property_data_type_enum = ENUM(
    'varchar', 'integer', 'decimal', 'real', 'boolean', 'timestamp', 'date',
    name='custom_property_data_type'
)

file_category_enum = ENUM(
    'archive', 'document', 'spreadsheet', 'presentation', 'image', 'video', 'audio',
    name='file_category'
)

file_type_enum = ENUM(
    'jpeg', 'png', 'gif', 'bmp', 'tiff', 'pdf', 'doc', 'docx', 'txt', 'rtf', 'csv', 'xls', 'xlsx',
    'ppt', 'pptx', 'zip', 'rar', 'sevenzip', 'mp3', 'wav', 'mp4', 'avi', 'mkv', 'svg',
    name='file_type'
)

email_type_enum = ENUM(
    'work', 'personal', 'business',
    name='email_type'
)

phone_type_enum = ENUM(
    'mobile', 'work', 'home',
    name='phone_type'
)

address_type_enum = ENUM(
    'home', 'work', 'other',
    name='address_type'
)

attachment_type_enum = ENUM(
    'profile_pic', 'hero_pic', 'thumbnail', 'document_cover', 'avatar', 'banner',
    'logo', 'background', 'icon', 'miscellaneous',
    name='attachment_type'
)

image_size_enum = ENUM(
    '0-original', '1-xsmall', '2-small', '3-medium', '4-large', '5-xlarge', '6-mongo',
    name='image_size'
)

timezone_enum = ENUM(
    'america/new_york', 'america/chicago', 'america/denver', 'america/los_angeles', 'america/phoenix',
    'america/anchorage', 'america/juneau', 'america/honolulu',
    name='timezone'
)

state_codes_enum = ENUM(
    'al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'fl', 'ga', 'hi', 'id', 'il', 'in', 'ia', 'ks',
    'ky', 'la', 'me', 'md', 'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv', 'nh', 'nj', 'nm', 'ny',
    'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv',
    'wi', 'wy',
    name='state_codes'
)

state_names_enum = ENUM(
    'alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware',
    'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky',
    'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi',
    'missouri', 'montana', 'nebraska', 'nevada', 'new_hampshire', 'new_jersey', 'new_mexico',
    'new_york', 'north_carolina', 'north_dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania',
    'rhode_island', 'south_carolina', 'south_dakota', 'tennessee', 'texas', 'utah', 'vermont',
    'virginia', 'washington', 'west_virginia', 'wisconsin', 'wyoming',
    name='state_names'
)





class GlobalSetting(db.Model):
    """Settings and Defaults for the entire app."""

    __tablename__ = "global_settings"

    id = db.Column(db.String(64), primary_key=True, nullable=False)
    default_currency_id = db.Column(currency_iso_code_enum, nullable=False)  # Using the PostgreSQL ENUM type
    time_format_is_24h = db.Column(db.Boolean, nullable=False)
    audit_info_id = db.Column(db.Integer, db.ForeignKey('audit_info.id'))

    audit_info = db.relationship('AuditInfo', backref='global_settings')


    def __repr__(self):
        return f'<id={self.id} currency_settings={self.default_currency_id} time_format_is_24h={self.time_format_is_24h}>'
    


class AuditInfo(db.Model):
    """Audit info for changes."""

    __tablename__ = "audit_info"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    operation_type = db.Column(operation_type_enum, nullable=False)  # Using the PostgreSQL ENUM type
    details = db.Column(String, nullable=True)
    created_by = db.Column(Integer, ForeignKey('users.id'))
    created_at = db.Column(DateTime, default=datetime.utcnow)
    last_edited_by = db.Column(Integer, ForeignKey('users.id'), nullable=True)
    last_edited_at = db.Column(DateTime, default=datetime.utcnow)
    is_archived = db.Column(Boolean, nullable=False, default=False)
    archived_at = db.Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<AuditInfo id={self.id} operation_type={self.operation_type} created_at={self.created_at}>"

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    password_hash = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    middle_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=False)
    nickname = db.Column(db.String, nullable=True)
    nickname_preferred = db.Column(db.Boolean, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    audit_info_id = db.Column(db.Integer, db.ForeignKey('audit_info.id'))

    audit_info = db.relationship('AuditInfo', backref='users')


    def __repr__(self):
        return f'<User id={self.id} first_name={self.first_name} last_name={self.last_name}>'



class Asset(db.Model):
    """An asset."""

    __tablename__ = "assets"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    manufacturer = db.Column(db.String, nullable=False)
    model_number = db.Column(db.String, nullable=True)
    model_name = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable= True)
    storage_area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable= True)
    purchase_date = db.Column(db.DateTime, nullable=True)
    purchase_price_id = db.Column(db.Integer, db.ForeignKey('financial_entries.id'), nullable= True)
    msrp_id = db.Column(db.Integer, db.ForeignKey('financial_entries.id'), nullable= True)
    residual_value_id = db.Column(db.Integer, db.ForeignKey('financial_entries.id'), nullable= True)
    parent_asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable= True)
    is_kit_root = db.Column(Boolean, nullable=False, default=False)
    is_attachment = db.Column(Boolean, nullable=False, default=False)
    serial_number = db.Column(db.String, nullable=True)
    inventory_number = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    is_available = db.Column(Boolean, nullable=False, default=True)
    online_item_page = db.Column(db.String, nullable=True)
    warranty_starts = db.Column(db.DateTime, nullable=True)
    warranty_ends = db.Column(db.DateTime, nullable=True)
    audit_info_id = db.Column(db.Integer, db.ForeignKey('audit_info.id'))

    category = db.relationship('Category', backref= 'assets')
    area = db.relationship('Area', backref= 'assets')
    financial_entry = db.relationship('FinancialEntry', backref= 'assets')
    audit_info = db.relationship('AuditInfo', backref= 'assets')

    def __repr__(self):
        return f'<Asset id={self.id} model_name={self.model_name}>'


class Category(db.Model):
    """A category for assets."""

    __tablename__ = "categories"

    #TODO: Add fields here



class Reservation(db.Model):
    """Areas."""

    __tablename__ = "reservations"

    #TODO: Add fields here

class Area(db.Model):
    """Areas."""

    __tablename__ = "areas"

    #TODO: Add fields here


    

class FinancialEntry(db.Model):
    """Financial Entries."""

    __tablename__ = "financial_entries"

    #TODO: Add fields here





def connect_to_db(flask_app, db_uri="postgresql:///parm", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_appmonicle
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)





# class CurrencyIsoCode(PyEnum):
#     UNITED_STATES = "USD"
#     CANADA =        "CAD"
#     MEXICO =        "MXN"

# class OperationType(PyEnum):
#     CREATE =    "CREATE"
#     UPDATE =    "UPDATE"
#     DELETE =    "DELETE"
#     ARCHIVE =   "ARCHIVE"

# class ReservationStatus(PyEnum):
#     PENDING =       "PENDING"
#     APPROVED =      "APPROVED"
#     CHECKED_OUT =   "CHECKED_OUT"
#     COMPLETED =     "COMPLETED"
#     CANCELLED =     "CANCELLED"
#     DENIED =        "DENIED"

# class ScanCodeType(PyEnum):
#     BARCODE =   "BARCODE"
#     QR =        "QR"
#     NFC =       "NFC"
#     BLUETOOTH = "BLUETOOTH"


# class CustomPropertyDataType(PyEnum):
#     VARCHAR =   "VARCHAR"
#     INTEGER =   "INTEGER"
#     DECIMAL =   "DECIMAL"
#     REAL =      "REAL"
#     BOOLEAN =   "BOOLEAN"
#     TIMESTAMP = "TIMESTAMP"
#     DATE =      "DATE"


# class ScanCodeType(PyEnum):
#     BARCODE =   "BARCODE"
#     QR =        "QR"
#     NFC =       "NFC"
#     BLUETOOTH = "BLUETOOTH"


# class FileCategory(PyEnum):
#     ARCHIVE =       "ARCHIVE"
#     DOCUMENT =      "DOCUMENT"
#     SPREADSHEET =   "SPREADSHEET"
#     PRESENTATION =  "PRESENTATION"
#     IMAGE =         "IMAGE"
#     VIDEO =         "VIDEO"
#     AUDIO =         "AUDIO"


# class FileType(PyEnum):
#     JPEG =      "JPEG"
#     PNG =       "PNG"
#     GIF =       "GIF"
#     BMP =       "BMP"
#     TIFF =      "TIFF"
#     PDF =       "PDF"
#     DOC =       "DOC"
#     DOCX =      "DOCX"
#     TXT =       "TXT"
#     RTF =       "RTF"
#     CSV =       "CSV"
#     XLS =       "XLS"
#     XLSX =      "XLSX"
#     PPT =       "PPT"
#     PPTX =      "PPTX"
#     ZIP =       "ZIP"
#     RAR =       "RAR"
#     SEVENZIP =  "SEVENZIP"
#     MP3 =       "MP3"
#     WAV =       "WAV"
#     MP4 =       "MP4"
#     AVI =       "AVI"
#     MKV =       "MKV"
#     SVG =       "SVG"


# class EmailType(PyEnum):
#     WORK =      "WORK"
#     PERSONAL =  "PERSONAL"
#     BUSINESS =  "BUSINESS"


# class PhoneType(PyEnum):
#     MOBILE =    "MOBILE"
#     WORK =      "WORK"
#     HOME =      "HOME"


# class AddressType(PyEnum):
#     HOME =      "HOME"
#     WORK =      "WORK"
#     OTHER =    "OTHER"


# class AttachmentType(PyEnum):
#     PROFILE_PIC =       "PROFILE_PIC"
#     HERO_PIC =          "HERO_PIC"
#     THUMBNAIL =         "THUMBNAIL"
#     DOCUMENT_COVER =    "DOCUMENT_COVER"
#     AVATAR =            "AVATAR"
#     BANNER =            "BANNER"
#     LOGO =              "LOGO"
#     BACKGROUND =        "BACKGROUND"
#     ICON =              "ICON"
#     MISCELLANEOUS =     "MISCELLANEOUS"


# class ImageSize(PyEnum):

#     ORIGINAL =  "0-original"
#     XSMALL =    "1-xsmall"
#     SMALL =     "2-small"
#     MEDIUM =    "3-medium"
#     LARGE =     "4-large"
#     XLARGE =    "5-xlarge"
#     MONGO =     "6-mongo"


# class CountryIsoCode(PyEnum):
#     UNITED_STATES = "US"
#     CANADA =        "CA"
#     MEXICO =        "MX"


# class Timezone(PyEnum):
#     NEW_YORK =      "America/New_York"
#     CHICAGO =       "America/Chicago"
#     DENVER =        "America/Denver"
#     LOS_ANGELES =   "America/Los_Angeles"
#     PHOENIX =       "America/Phoenix"
#     ANCHORAGE =     "America/Anchorage"
#     JENEAU =        "America/Juneau"
#     HONOLULU =      "America/Honolulu"


# class StateCodes(PyEnum):
#     AL = "AL"
#     AK = "AK"
#     AZ = "AZ"
#     AR = "AR"
#     CA = "CA"
#     CO = "CO"
#     CT = "CT"
#     DE = "DE"
#     FL = "FL"
#     GA = "GA"
#     HI = "HI"
#     ID = "ID"
#     IL = "IL"
#     IN = "IN"
#     IA = "IA"
#     KS = "KS"
#     KY = "KY"
#     LA = "LA"
#     ME = "ME"
#     MD = "MD"
#     MA = "MA"
#     MI = "MI"
#     MN = "MN"
#     MS = "MS"
#     MO = "MO"
#     MT = "MT"
#     NE = "NE"
#     NV = "NV"
#     NH = "NH"
#     NJ = "NJ"
#     NM = "NM"
#     NY = "NY"
#     NC = "NC"
#     ND = "ND"
#     OH = "OH"
#     OK = "OK"
#     OR = "OR"
#     PA = "PA"
#     RI = "RI"
#     SC = "SC"
#     SD = "SD"
#     TN = "TN"
#     TX = "TX"
#     UT = "UT"
#     VT = "VT"
#     VA = "VA"
#     WA = "WA"
#     WV = "WV"
#     WI = "WI"
#     WY = "WY"

# class StateNames(PyEnum):
#     ALABAMA =           "Alabama"
#     ALASKA =            "Alaska"
#     ARIZONA =           "Arizona"
#     ARKANSAS =          "Arkansas"
#     CALIFORNIA =        "California"
#     COLORADO =          "Colorado"
#     CONNECTICUT =       "Connecticut"
#     DELAWARE =          "Delaware"
#     FLORIDA =           "Florida"
#     GEORGIA =           "Georgia"
#     HAWAII =            "Hawaii"
#     IDAHO =             "Idaho"
#     ILLINOIS =          "Illinois"
#     INDIANA =           "Indiana"
#     IOWA =              "Iowa"
#     KANSAS =            "Kansas"
#     KENTUCKY =          "Kentucky"
#     LOUISIANA =         "Louisiana"
#     MAINE =             "Maine"
#     MARYLAND =          "Maryland"
#     MASSACHUSETTS =     "Massachusetts"
#     MICHIGAN =          "Michigan"
#     MINNESOTA =         "Minnesota"
#     MISSISSIPPI =       "Mississippi"
#     MISSOURI =          "Missouri"
#     MONTANA =           "Montana"
#     NEBRASKA =          "Nebraska"
#     NEVADA =            "Nevada"
#     NEW_HAMPSHIRE =     "New Hampshire"
#     NEW_JERSEY =        "New Jersey"
#     NEW_MEXICO =        "New Mexico"
#     NEW_YORK =          "New York"
#     NORTH_CAROLINA =    "North Carolina"
#     NORTH_DAKOTA =      "North Dakota"
#     OHIO =              "Ohio"
#     OKLAHOMA =          "Oklahoma"
#     OREGON =            "Oregon"
#     PENNSYLVANIA =      "Pennsylvania"
#     RHODE_ISLAND =      "Rhode Island"
#     SOUTH_CAROLINA =    "South Carolina"
#     SOUTH_DAKOTA =      "South Dakota"
#     TENNESSEE =         "Tennessee"
#     TEXAS =             "Texas"
#     UTAH =              "Utah"
#     VERMONT =           "Vermont"
#     VIRGINIA =          "Virginia"
#     WASHINGTON =        "Washington"
#     WEST_VIRGINIA =     "West Virginia"
#     WISCONSIN =         "Wisconsin"
#     WYOMING =           "Wyoming"