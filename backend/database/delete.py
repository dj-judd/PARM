"Delete methods for DB Entities"

from database import model
from database import crud

from database.permissions import has_permission, PermissionsType
from tools import utils

from typing import Optional, List
from sqlalchemy import desc
from sqlalchemy.orm import aliased


class GlobalSettings:
    pass



class AuditEntry:
    pass



class Reservation:
    pass



class ReservationAsset:
    pass



class AssetTag:
    pass



class Comment:
    pass



class Reaction:
    pass



class Category:
    pass



class Color:
    pass



class CustomProperty:
    pass



class AssetCustomProperty:
    pass



class Asset:
    pass



class Manufacturer:
    pass



class AssetFlag:
    pass



class Flag:
    pass



class Currency:
    pass



class FinancialEntry:
    pass



class AssetLocationLog:
    pass



class FileAttachment:
    pass



class EmailAddress:
    pass



class PhoneNumber:
    pass



class UiTheme:
    pass



class UserSettings:
    pass



class User:
    pass



class UserRole:
    pass



class Role:
    pass



class Permission:
    pass



class RolePermission:
    pass



class Area:
    pass



class Address:
    pass



class Country:
    pass



class Timezone:
    pass



class State:
    pass