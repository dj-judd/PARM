"Read methods for DB Entities"

import model
import crud

from permissions import has_permission, PermissionsType
from backend_tools import utils

from typing import Optional, List
from sqlalchemy import desc
from sqlalchemy.orm import aliased


class GlobalSettings:

    @staticmethod
    def entry():
        """Fetch and return the first entry from the global_settings table, or None if no entry exists."""
        
        global_settings = model.db.session.query(model.GlobalSettings).first()
        return global_settings if global_settings else None




class AuditEntry:

    @staticmethod
    def by_id(requesting_user_id: int,
                        audit_entry_id: int):
        """Fetch and return an AuditEntry by its id, or None if no matching entry is found."""
        
        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_AUDITS.value):
            audit_entry = model.db.session.query(model.AuditEntry).filter_by(id=audit_entry_id).first()

            return audit_entry if audit_entry else None

        return PermissionError()


    @staticmethod
    def by_ids(requesting_user_id: int,
                            audit_entry_ids: List[int]):
        """Fetch and return a list of AuditEntries by their ids, or None if no matching entry is found."""
        
        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_AUDITS.value):
            audit_entries = model.db.session.query(model.AuditEntry).filter(model.AuditEntry.id.in_(audit_entry_ids)).all()
            
            return audit_entries if audit_entries else None

        return PermissionError()


    @staticmethod
    def most_recent_for_entity(requesting_user_id: int,
                                        auditable_entity_type: model.AuditableEntityTypes,
                                        related_entity_id: int):
        """Fetch and return the most recent AuditEntry for a specific entity type and id, or None if no matching entry is found."""
        
        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_AUDITS.value):
            most_recent_entry = model.db.session.query(model.AuditEntry).filter_by(auditable_entity_type=auditable_entity_type,
                                                                                    related_entity_id=related_entity_id
                                        ).order_by(desc(model.AuditEntry.created_at)).first()
            
            return most_recent_entry if most_recent_entry else None
        
        return PermissionError()


    @staticmethod
    def all(requesting_user_id: int):
        """Fetch and return all entries from the AuditEntry table, or None if the table is empty."""
        
        # Check if requesting user has access to view all of the audits at once.
        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ALL_AUDITS.value):
            audit_entries = model.db.session.query(model.AuditEntry).all()

            return audit_entries if audit_entries else None
        
        return PermissionError()




class Reservation:

    @staticmethod
    def by_id(requesting_user_id: int,
              reservation_id: int,
              include_archived: bool = False):
        """
        Fetch and return a reservation by ID, or None if no match is found.
        """

        # Use the utility function to create a query with an outer join on the AuditEntry table.
        query, latest_audit = crud.Utils.get_query_with_audit_join(model.db.session,
                                                                model.Reservation,
                                                                model.AuditableEntityTypes.RESERVATION.value)

        # Further filter the query by reservation ID and sort it by the latest audit entry.
        query = query.filter_by(id=reservation_id).order_by(latest_audit.created_at.desc()).first()

        # Check if the user has permission to view archived reservations.
        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value):
            # Return the query result if either "include_archived" is True or the reservation is not archived.
            return query if include_archived or latest_audit.is_archived == False else None

        # Return the query result only if the reservation is not archived.
        return query if latest_audit.is_archived == False else None


    @staticmethod
    def by_ids(requesting_user_id: int, 
               reservation_ids: List[int], 
               include_archived: bool = False, 
               just_archived: bool = False):
        """
        Fetch and return reservations by a list of IDs, or None if no match is found.
        """

        # Raise error if both flags are True
        if include_archived and just_archived:
            raise ValueError("Both flags cannot be True.")

        # Use the utility function to create a query with an outer join on the AuditEntry table.
        query, latest_audit = crud.Utils.get_query_with_audit_join(model.db.session, 
                                                                model.Reservation, 
                                                                model.AuditableEntityTypes.RESERVATION.value)

        # Further filter the query by a list of reservation IDs and make it distinct by Reservation ID.
        query = query.filter(model.Reservation.id.in_(reservation_ids)).distinct(model.Reservation.id)
        
        # Check if the user has permission to view archived reservations.
        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value):
            # Use the utility function to filter the query based on the archived status flags.
            query = crud.Utils.filter_by_archived_status(query, latest_audit, include_archived, just_archived)
        else:
            # User does not have permission to view archived, so ensure only non-archived are shown
            if just_archived:
                return None
            query = query.filter(latest_audit.is_archived == False)
        
        # Execute the query and fetch all the results.
        reservations = query.all()

        # Return the query results or None if the result is empty.
        return reservations if reservations else None
    

    @staticmethod
    def by_user_id(requesting_user_id: int,
                   user_id: int,
                   include_archived: bool = False,
                   just_archived: bool = False):
        """
        Fetch and return reservations by a user ID, or None if no match is found.
        """

        # Raise error if both flags are True
        if include_archived and just_archived:
            raise ValueError("Both flags cannot be True.")

        # Use the utility function to create a query with an outer join on the AuditEntry table.
        query, latest_audit = crud.Utils.get_query_with_audit_join(model.db.session,
                                                                model.Reservation,
                                                                model.AuditableEntityTypes.RESERVATION.value)
        
        # Further filter the query by user ID
        query = query.filter(model.Reservation.user_id == user_id)

        # Check if the user has permission to view archived reservations.
        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value):
            query = crud.Utils.filter_by_archived_status(query, latest_audit, include_archived, just_archived)
        else:
            if just_archived:
                return None
            query = query.filter(latest_audit.is_archived == False)

        reservations = query.all()

        # Return the query results or None if the result is empty.
        return reservations if reservations else None


    @staticmethod
    def all(requesting_user_id: int,
            include_archived: bool = False,
            just_archived: bool = False):
        """Fetch and return all entries from the Reservation table, or None if the table is empty."""

        # Raise error if both flags are True
        if include_archived and just_archived:
            raise ValueError("Both flags cannot be True.")

        # Use the utility function to create a query with an outer join on the AuditEntry table.
        query, latest_audit = crud.Utils.get_query_with_audit_join(model.db.session,
                                                                model.Reservation,
                                                                model.AuditableEntityTypes.RESERVATION.value)

        # Use the utility function to filter the query based on the archived status flags.
        query = crud.Utils.filter_by_archived_status(query, latest_audit, include_archived, just_archived)

        # Check permissions and execute query
        if not has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value) and just_archived:
            return None  # No permission to view only archived

        reservations = query.all()

        # Return results or None if empty
        return reservations if reservations else None



class ReservationAsset:

    @staticmethod
    def by_reservation_id(requesting_user_id: int, 
                          reservation_id: int,
                          include_archived: bool = False):
        """Fetch and return all ReservationAsset entries that match the given reservation ID, or none if empty."""

        query, latest_audit = crud.Utils.get_query_with_audit_join(model.db.session,
                                                                   model.ReservationAsset,
                                                                   model.AuditableEntityTypes.RESERVATION_ASSET.value)
        query = query.filter_by(reservation_id=reservation_id)

        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_ASSETS.value) and has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value):
            query = query if include_archived or latest_audit.is_archived == False else None
        else:
            query = query if latest_audit.is_archived == False else None

        reservation_assets = query.all()
        return reservation_assets if reservation_assets else None

    @staticmethod
    def by_asset_id(requesting_user_id: int, 
                    asset_id: int,
                    include_archived: bool = False):
        """Retrieve all ReservationAsset entries that match the given asset ID, or none if empty."""

        query, latest_audit = crud.Utils.get_query_with_audit_join(model.db.session,
                                                                   model.ReservationAsset,
                                                                   model.AuditableEntityTypes.RESERVATION_ASSET.value)
        query = query.filter_by(asset_id=asset_id)

        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_ASSETS.value) and has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value):
            query = query if include_archived or latest_audit.is_archived == False else None
        else:
            query = query if latest_audit.is_archived == False else None

        reservation_assets = query.all()
        return reservation_assets if reservation_assets else None

    @staticmethod
    def by_ids(requesting_user_id: int, 
               reservation_ids: List[int], 
               asset_ids: List[int], 
               include_archived: bool = False):
        """Retrieve all ReservationAsset entries that match the given list of reservation IDs and asset IDs"""

        query, latest_audit = crud.Utils.get_query_with_audit_join(model.db.session,
                                                                   model.ReservationAsset,
                                                                   model.AuditableEntityTypes.RESERVATION_ASSET.value)
        query = query.filter(
            model.ReservationAsset.reservation_id.in_(reservation_ids),
            model.ReservationAsset.asset_id.in_(asset_ids)
        )

        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_ASSETS.value) and has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value):
            query = query if include_archived or latest_audit.is_archived == False else None
        else:
            query = query if latest_audit.is_archived == False else None

        reservation_assets = query.all()
        return reservation_assets if reservation_assets else None



class AssetTag:
    pass



class Comment:
    pass



class Reaction:
    pass



class Category:
    
    @staticmethod
    def by_id(category_id: int) -> Optional[object]:
        """Fetch and return a Category by its ID, or None if no match is found."""

        return model.db.session.query(model.Category).filter_by(id=category_id).first()

    @staticmethod
    def by_ids(category_ids: List[int]) -> Optional[List[object]]:
        """Fetch and return a list of Categories by their IDs, or None if no match is found."""

        query = model.db.session.query(model.Category).filter(model.Category.id.in_(category_ids)).all()
        return query if query else None

    @staticmethod
    def by_name(category_name: str) -> Optional[object]:
        """Fetch and return a Category by its name, or None if no match is found."""
        
        return model.db.session.query(model.Category).filter_by(name=category_name).first()

    @staticmethod
    def by_parent_id(parent_id: int) -> Optional[List[object]]:
        """Fetch and return all subcategories of a parent category by its ID, or None if no match is found."""

        query = model.db.session.query(model.Category).filter_by(parent_category_id=parent_id).all()
        return query if query else None

    @staticmethod
    def all() -> Optional[List[object]]:
        """Fetch and return all entries from the Category table, or None if the table is empty."""

        query = model.db.session.query(model.Category).all()
        return query if query else None



class Color:
    
    @staticmethod
    def by_id(color_id: int) -> Optional[object]:
        """Fetch and return a Color by its ID, or None if no match is found."""

        return model.db.session.query(model.Manufacturer).filter_by(id=color_id).first()

    @staticmethod
    def by_ids(color_ids: List[int]) -> Optional[List[object]]:
        """Fetch and return a list of Colors by their IDs, or None if no match is found."""

        query = model.db.session.query(model.Manufacturer).filter(model.Manufacturer.id.in_(color_ids)).all()
        return query if query else None

    @staticmethod
    def by_name(color_name: str) -> Optional[object]:
        """Fetch and return a Color by its name, or None if no match is found."""

        return model.db.session.query(model.Manufacturer).filter_by(name=color_name).first()

    @staticmethod
    def by_hex_value(hex_value: str) -> Optional[object]:
        """Fetch and return a Color by its hex value, or None if no match is found."""

        return model.db.session.query(model.Manufacturer).filter_by(hex_value=hex_value).first()

    @staticmethod
    def all() -> Optional[List[object]]:
        """Fetch and return all entries from the Color table, or None if the table is empty."""

        query = model.db.session.query(model.Manufacturer).all()
        return query if query else None



class CustomProperty:
    pass



class AssetCustomProperty:
    pass



class Asset:

    @staticmethod
    def by_id(requesting_user_id: int,
              asset_id: int,
              include_archived: bool = False):
        query, latest_audit = crud.Utils.get_query_with_audit_join(model.db.session,
                                                                model.Asset,
                                                                model.AuditableEntityTypes.ASSET.value)
        query = query.filter_by(id=asset_id).order_by(latest_audit.created_at.desc()).first()

        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_ASSETS.value):
            return query if include_archived or latest_audit.is_archived == False else None

        return query if latest_audit.is_archived == False else None


    @staticmethod
    def by_ids(requesting_user_id: int, 
               asset_ids: List[int], 
               include_archived: bool = False, 
               just_archived: bool = False):

        if include_archived and just_archived:
            raise ValueError("Both flags cannot be True.")

        query, latest_audit = crud.Utils.get_query_with_audit_join(model.db.session, 
                                                                model.Asset, 
                                                                model.AuditableEntityTypes.ASSET.value)
        query = query.filter(model.Asset.id.in_(asset_ids)).distinct(model.Asset.id)

        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_ASSETS.value):
            query = crud.Utils.filter_by_archived_status(query, latest_audit, include_archived, just_archived)
        else:
            if just_archived:
                return None
            query = query.filter(latest_audit.is_archived == False)

        assets = query.all()
        return assets if assets else None


    @staticmethod
    def by_category(requesting_user_id: int, 
                    category_ids: List[int], 
                    include_archived: bool = False, 
                    just_archived: bool = False):

        if include_archived and just_archived:
            raise ValueError("Both flags cannot be True.")

        query, latest_audit = crud.Utils.get_query_with_audit_join(model.db.session,
                                                                   model.Asset,
                                                                   model.AuditableEntityTypes.ASSET.value)
        
        query = query.filter(model.Asset.category_id.in_(category_ids))

        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_ASSETS.value):
            query = crud.Utils.filter_by_archived_status(query, latest_audit, include_archived, just_archived)
        else:
            if just_archived:
                return None
            query = query.filter(latest_audit.is_archived == False)
        
        assets_by_category = query.all()

        return assets_by_category if assets_by_category else None
    

    @staticmethod
    def all(requesting_user_id: int,
            include_archived: bool = False,
            just_archived: bool = False):

        if include_archived and just_archived:
            raise ValueError("Both flags cannot be True.")

        query, latest_audit = crud.Utils.get_query_with_audit_join(model.db.session,
                                                                model.Asset,
                                                                model.AuditableEntityTypes.ASSET.value)
        query = crud.Utils.filter_by_archived_status(query, latest_audit, include_archived, just_archived)

        if not has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_ASSETS.value) and just_archived:
            return None

        assets = query.all()
        return assets if assets else None
    

class Manufacturer:

    @staticmethod
    def by_id(manufacturer_id: int) -> Optional[object]:
        """Fetch and return a Manufacturer by its ID, or None if no match is found."""

        return model.db.session.query(model.Manufacturer).filter_by(id=manufacturer_id).first()


    @staticmethod
    def by_ids(manufacturer_id: List[int]) -> Optional[List[object]]:
        """Fetch and return a list of Manufacturers by their IDs, or None if no match is found."""

        query = model.db.session.query(model.Manufacturer).filter(model.Manufacturer.id.in_(manufacturer_id)).all()
        return query if query else None


    @staticmethod
    def by_name(manufacturer_name: str) -> Optional[object]:
        """Fetch and return a Manufacturer by its name, or None if no matching entry is found."""
        
        manufacturer = model.db.session.query(model.Manufacturer).filter_by(name=manufacturer_name).first()
        return manufacturer if manufacturer else None


    @staticmethod
    def all() -> Optional[List[object]]:
        """Fetch and return all entries from the Manufacturer table, or None if the table is empty."""
        
        query = model.db.session.query(model.Manufacturer).all()
        return query if query else None
    


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