"""Models for PARM database."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey, Enum
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class OperationType(Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    ARCHIVE = "ARCHIVE"

class AuditInfo(db.Model):
    """Audit info for changes."""

    __tablename__ = "audit_info"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    operation_type = db.Column(Enum(OperationType), nullable=False)
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

class Area(db.Model):
    """Areas."""

    __tablename__ = "areas"

    #TODO: Add fields here

class FinancialEntry(db.Model):
    """Financial Entries."""

    __tablename__ = "financial_entries"

    #TODO: Add fields here


def connect_to_db(flask_app, db_uri="postgresql:///parm_assets", echo=True):
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
