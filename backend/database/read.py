"Read methods for DB Entities"
from database import model
from database import crud

from database.permissions import has_permission, PermissionsType
from tools import utils

from typing import Optional, List, Dict
from sqlalchemy import desc
from sqlalchemy.orm import joinedload, aliased


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
        """Fetch and return a reservation by ID, or None if no match is found."""

        query, latest_audit = crud.Utils.get_query_with_audit_join(model.Reservation,
                                                                   model.AuditableEntityTypes.RESERVATION.value)
        
        query = query.options(joinedload('area'))

        query = query.filter_by(id=reservation_id)
        
        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value):
            if not include_archived:
                query = query.filter(latest_audit.is_archived == False)
        else:
            query = query.filter(latest_audit.is_archived == False)

        return query.first()


    @staticmethod
    def by_ids(requesting_user_id: int, 
               reservation_ids: List[int], 
               include_archived: bool = False, 
               just_archived: bool = False):
        """Fetch and return reservations by a list of IDs, or None if no match is found."""
        
        if include_archived and just_archived:
            raise ValueError("Both flags cannot be True.")

        query, latest_audit = crud.Utils.get_query_with_audit_join(model.Reservation,
                                                                   model.AuditableEntityTypes.RESERVATION.value)
        query = query.options(joinedload('area'))
        query = query.filter(model.Reservation.id.in_(reservation_ids))
        
        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value):
            if just_archived:
                query = query.filter(latest_audit.is_archived == True)
            elif not include_archived:
                query = query.filter(latest_audit.is_archived == False)
        else:
            if just_archived:
                return None
            query = query.filter(latest_audit.is_archived == False)

        reservations = query.all()
        return reservations if reservations else None
    

    @staticmethod
    def by_user_id(requesting_user_id: int,
                   user_id: int,
                   include_archived: bool = False,
                   just_archived: bool = False):
        """Fetch and return reservations by a user ID, or None if no match is found."""

        if include_archived and just_archived:
            raise ValueError("Both flags cannot be True.")
            
        query, latest_audit = crud.Utils.get_query_with_audit_join(model.Reservation,
                                                                   model.AuditableEntityTypes.RESERVATION.value)
        
        query = query.options(joinedload('area'))

        query = query.filter(model.Reservation.user_id == user_id)
        
        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value):
            if just_archived:
                query = query.filter(latest_audit.is_archived == True)
            elif not include_archived:
                query = query.filter(latest_audit.is_archived == False)
        else:
            if just_archived:
                return None
            query = query.filter(latest_audit.is_archived == False)
        
        reservations = query.all()
        return reservations if reservations else None


    @staticmethod
    def all(requesting_user_id: int,
            include_archived: bool = False,
            just_archived: bool = False):
        """Fetch and return all entries from the Reservation table, or None if the table is empty."""

        if include_archived and just_archived:
            raise ValueError("Both flags cannot be True.")
            
        query, latest_audit = crud.Utils.get_query_with_audit_join(model.Reservation,
                                                                   model.AuditableEntityTypes.RESERVATION.value)
        
        query = query.options(joinedload('area'))

        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value):
            if just_archived:
                query = query.filter(latest_audit.is_archived == True)
            elif not include_archived:
                query = query.filter(latest_audit.is_archived == False)
        else:
            if just_archived:
                return None
            query = query.filter(latest_audit.is_archived == False)
        
        reservations = query.all()
        return reservations if reservations else None



class ReservationAsset:

    @staticmethod
    def by_reservation_id(requesting_user_id: int, 
                          reservation_id: int,
                          include_archived: bool = False):
        """Fetch and return all ReservationAsset entries that match the given reservation ID, or none if empty."""
        
        # Initialize the query with a join to the audit table
        query, latest_audit = crud.Utils.get_query_with_audit_join(model.ReservationAsset,
                                                                   model.AuditableEntityTypes.RESERVATION_ASSET.value)
        
        # Add joins for Asset and Reservation relationships to pull related data in one SQL call
        query = query.options(joinedload('asset'), joinedload('reservation'))
        
        # Filter the query to only include records that match the specified reservation ID
        query = query.filter_by(reservation_id=reservation_id)
        
        # Check permissions to view archived assets and reservations
        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_ASSETS.value) and has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value):
            # If "include_archived" is False, filter out archived records
            if not include_archived:
                query = query.filter(latest_audit.is_archived == False)
        else:
            # If user doesn't have permissions, filter out archived records by default
            query = query.filter(latest_audit.is_archived == False)

        # Execute the query and fetch all results
        reservation_assets = query.all()
        
        # Return the results if available, otherwise return None
        return reservation_assets if reservation_assets else None


    @staticmethod
    def by_asset_id(requesting_user_id: int, 
                    asset_id: int,
                    include_archived: bool = False):
        """Retrieve all ReservationAsset entries that match the given asset ID, or none if empty."""

        query, latest_audit = crud.Utils.get_query_with_audit_join(model.ReservationAsset,
                                                                   model.AuditableEntityTypes.RESERVATION_ASSET.value)
        
        query = query.options(joinedload('asset'), joinedload('reservation'))

        query = query.filter_by(asset_id=asset_id)

        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_ASSETS.value) and has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value):
            if not include_archived:
                query = query.filter(latest_audit.is_archived == False)
        else:
            query = query.filter(latest_audit.is_archived == False)

        reservation_assets = query.all()
        return reservation_assets if reservation_assets else None


    @staticmethod
    def by_ids(requesting_user_id: int, 
            reservation_ids: List[int], 
            asset_ids: List[int], 
            include_archived: bool = False):
        """Retrieve all ReservationAsset entries that match the given list of reservation IDs and asset IDs, or none if empty."""
        
        query, latest_audit = crud.Utils.get_query_with_audit_join(model.ReservationAsset,
                                                                   model.AuditableEntityTypes.RESERVATION_ASSET.value)
        
        query = query.options(joinedload('asset'), joinedload('reservation'))

        query = query.filter(model.ReservationAsset.reservation_id.in_(reservation_ids),
                             model.ReservationAsset.asset_id.in_(asset_ids))

        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_ASSETS.value) and has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value):
            if not include_archived:
                query = query.filter(latest_audit.is_archived == False)
        else:
            query = query.filter(latest_audit.is_archived == False)

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
    

    @staticmethod
    def all_ordered() -> Optional[Dict[int, object]]:
        """Fetch and return all entries from the Category table ordered by hierarchy, or None if the table is empty."""
        
        def transform_to_hierarchical(query_result):
            tree = {}
            lookup = {}
            
            for item in query_result:
                id = item.id
                node = item.to_dict()
                node['children'] = []
                lookup[id] = node
                if item.parent_category_id is None:
                    tree[id] = node
                else:
                    lookup[item.parent_category_id]['children'].append(node)
            
            return tree



        query = model.db.session.query(model.Category).all()

        if query:
            return transform_to_hierarchical(query)
        else:
            return None



class Color:
    
    @staticmethod
    def by_id(color_id: int) -> Optional[object]:
        """Fetch and return a Color by its ID, or None if no match is found."""

        return model.db.session.query(model.Color).filter_by(id=color_id).first()

    @staticmethod
    def by_ids(color_ids: List[int]) -> Optional[List[object]]:
        """Fetch and return a list of Colors by their IDs, or None if no match is found."""

        query = model.db.session.query(model.Color).filter(model.Color.id.in_(color_ids)).all()
        return query if query else None

    @staticmethod
    def by_name(color_name: str) -> Optional[object]:
        """Fetch and return a Color by its name, or None if no match is found."""

        return model.db.session.query(model.Color).filter_by(name=color_name).first()

    @staticmethod
    def by_hex_value(hex_value: str) -> Optional[object]:
        """Fetch and return a Color by its hex value, or None if no match is found."""

        return model.db.session.query(model.Color).filter_by(hex_value=hex_value).first()

    @staticmethod
    def all() -> Optional[List[object]]:
        """Fetch and return all entries from the Color table, or None if the table is empty."""

        query = model.db.session.query(model.Color).all()
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
        """Fetch and return an Asset by its ID, or None if no match is found."""

        query, latest_audit = crud.Utils.get_query_with_audit_join(model.Asset,
                                                                   model.AuditableEntityTypes.ASSET.value)
        
        query = query.options(joinedload('manufacturer'),
                              joinedload('category'),
                              joinedload('storage_area'),
                              joinedload('purchase_price_entry'),
                              joinedload('msrp_entry'),
                              joinedload('residual_value_entry'))

        query = query.filter(model.Asset.id == asset_id).order_by(latest_audit.created_at.desc()).first()

        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_ASSETS.value):
            if not include_archived:
                query = query.filter(latest_audit.is_archived == False)
        else:
            query = query.filter(latest_audit.is_archived == False)

        return query


    @staticmethod
    def by_ids(requesting_user_id: int, 
               asset_ids: List[int], 
               include_archived: bool = False, 
               just_archived: bool = False):
        """Fetch and return Assets by a list of IDs, or None if no match is found."""

        if include_archived and just_archived:
            raise ValueError("Both flags cannot be True.")

        query, latest_audit = crud.Utils.get_query_with_audit_join(model.Asset, 
                                                                   model.AuditableEntityTypes.ASSET.value)
        
        query = query.options(joinedload('manufacturer'),
                              joinedload('category'),
                              joinedload('storage_area'),
                              joinedload('purchase_price_entry'),
                              joinedload('msrp_entry'),
                              joinedload('residual_value_entry'))

        query = query.filter(model.Asset.id.in_(asset_ids)).distinct(model.Asset.id)

        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_ASSETS.value):
            if just_archived:
                query = query.filter(latest_audit.is_archived == True)
            elif not include_archived:
                query = query.filter(latest_audit.is_archived == False)
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
        """Fetch and return Assets by their category IDs, or None if no match is found."""

        if include_archived and just_archived:
            raise ValueError("Both flags cannot be True.")

        query, latest_audit = crud.Utils.get_query_with_audit_join(model.Asset,
                                                                   model.AuditableEntityTypes.ASSET.value)
        
        query = query.options(joinedload('manufacturer'),
                            joinedload('category'),
                            joinedload('storage_area'),
                            joinedload('purchase_price_entry'),
                            joinedload('msrp_entry'),
                            joinedload('residual_value_entry'))
        
        query = query.filter(model.Asset.category_id.in_(category_ids))

        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_ASSETS.value):
            if just_archived:
                query = query.filter(latest_audit.is_archived == True)
            elif not include_archived:
                query = query.filter(latest_audit.is_archived == False)
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
        """Fetch and return all Assets, or None if the table is empty."""

        if include_archived and just_archived:
            raise ValueError("Both flags cannot be True.")

        query, latest_audit = crud.Utils.get_query_with_audit_join(model.Asset,
                                                                   model.AuditableEntityTypes.ASSET.value)
        query = query.options(joinedload('manufacturer'),
                            joinedload('category'),
                            joinedload('storage_area'),
                            joinedload('purchase_price_entry'),
                            joinedload('msrp_entry'),
                            joinedload('residual_value_entry'))

        if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_ASSETS.value):
            if just_archived:
                query = query.filter(latest_audit.is_archived == True)
            elif not include_archived:
                query = query.filter(latest_audit.is_archived == False)
        else:
            if just_archived:
                return None
            query = query.filter(latest_audit.is_archived == False)

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
    
    @staticmethod
    def by_id(entry_id: int) -> Optional[object]:
        """Fetch and return a FinancialEntry by its ID, or None if no match is found."""
        return model.db.session.query(model.FinancialEntry).filter_by(id=entry_id).first()

    @staticmethod
    def by_ids(entry_ids: List[int]) -> Optional[List[object]]:
        """Fetch and return a list of FinancialEntries by their IDs, or None if no match is found."""
        query = model.db.session.query(model.FinancialEntry).filter(model.FinancialEntry.id.in_(entry_ids)).all()
        return query if query else None

    @staticmethod
    def by_currency_id(currency_id: int) -> Optional[List[object]]:
        """Fetch and return a list of FinancialEntries by currency ID, or None if no match is found."""
        return model.db.session.query(model.FinancialEntry).filter_by(currency_id=currency_id).all()

    @staticmethod
    def by_amount_range(min_amount: float, max_amount: float) -> Optional[List[object]]:
        """Fetch and return a list of FinancialEntries within a specific amount range, or None if no match is found."""
        query = model.db.session.query(model.FinancialEntry).filter(model.FinancialEntry.amount.between(min_amount, max_amount)).all()
        return query if query else None

    @staticmethod
    def all() -> Optional[List[object]]:
        """Fetch and return all entries from the FinancialEntry table, or None if the table is empty."""
        query = model.db.session.query(model.FinancialEntry).all()
        return query if query else None



class AssetLocationLog:
    pass



class FileAttachment:
    
    @staticmethod
    def image_size_for_entity_id(entity_id: int, attachable_entity_type: model.AttachableEntityTypes, image_size: model.ImageSize) -> Optional[object]:
        """Fetch and return a FileAttachment by its entity ID, attachable entity type, and image size, or None if not found."""
        
        query = model.db.session.query(model.FileAttachment).filter_by(entity_id=entity_id, attachable_entity_type=attachable_entity_type, image_size=image_size).first()
        return query if query else None


    @staticmethod
    def all_for_entity_id(entity_id: int, attachable_entity_type: model.AttachableEntityTypes) -> Optional[List[object]]:
        """Fetch and return all FileAttachments for a given entity ID and attachable entity type, or None if not found."""
        
        query = model.db.session.query(model.FileAttachment).filter_by(entity_id=entity_id, attachable_entity_type=attachable_entity_type).all()
        return query if query else None
    

    @staticmethod
    def all_file_hash_list() -> Optional[List[str]]:
        """Fetch and return all unique file hashes from the FileAttachments table, or None if not found."""
        
        query = model.db.session.query(model.FileAttachment.file_hash).distinct().all()
        return [record.file_hash for record in query] if query else None
    

    @staticmethod
    def all_file_hash_dict() -> Optional[Dict[str, int]]:
        """Fetch and return a dictionary mapping file hashes to their IDs, or None if not found."""
        
        query = model.db.session.query(model.FileAttachment.file_hash, model.FileAttachment.id).all()
        return {record.file_hash: record.id for record in query} if query else None



    # @staticmethod
    # def by_entity_type(entity_type: model.AttachableEntityTypes) -> Optional[List[object]]:
    #     """Fetch and return FileAttachments based on their attachable entity type, or None if not found."""

    #     query = model.db.session.query(model.FileAttachment).filter_by(attachable_entity_type=entity_type).all()
    #     return query if query else None


    # @staticmethod
    # def by_file_type(file_type: model.FileType) -> Optional[List[object]]:
    #     """Fetch and return FileAttachments based on their file type, or None if not found."""

    #     query = model.db.session.query(model.FileAttachment).filter_by(file_type=file_type).all()
    #     return query if query else None


    # @staticmethod
    # def by_file_category(file_category: model.FileCategory) -> Optional[List[object]]:
    #     """Fetch and return FileAttachments based on their file category, or None if not found."""

    #     query = model.db.session.query(model.FileAttachment).filter_by(file_category=file_category).all()
    #     return query if query else None
    





class EmailAddress:
    pass



class PhoneNumber:
    pass



class UiTheme:
    
    @staticmethod
    def by_id(entry_id: int) -> Optional[object]:
        """Fetch and return a UiTheme by its ID, or None if no match is found."""

        return model.db.session.query(model.UiTheme).filter_by(id=entry_id).first()
    
    @staticmethod
    def colors_by_id(entry_id: int) -> Optional[dict]:
        """Fetch the primary and secondary color IDs for a UiTheme by its ID."""

        theme = UiTheme.by_id(entry_id)

        theme_primary_object = Color.by_id(theme.primary_color_id)
        theme_secondary_object = Color.by_id(theme.secondary_color_id)

        theme_primary_hex = theme_primary_object.hex_value
        theme_secondary_hex = theme_secondary_object.hex_value

        if theme:
            return {"primary_color_id": theme_primary_hex,
                    "secondary_color_id": theme_secondary_hex}
        return None



class UserSettings:

    @staticmethod
    def by_id(entry_id: int) -> Optional[object]:
        """Fetch and return a UserSettings by its ID, or None if no match is found."""

        return model.db.session.query(model.UserSettings).filter_by(id=entry_id).first()
    
    @staticmethod
    def by_user_id(user_id: int) -> Optional[object]:
        """Fetch and return UserSettings by user ID, or None if no match is found."""

        return model.db.session.query(model.UserSettings).filter_by(user_id=user_id).first()



class User:
    

    @staticmethod
    def by_email(email_address: str):
        """Fetch and return a User entry that matches the given email address, or None if not found."""

        # Initialize the query
        query = model.db.session.query(model.User)

        # Join EmailAddress table to fetch related email information
        query = query.join(
            model.EmailAddress,
            model.User.id == model.EmailAddress.entity_id
        ).filter(
            model.EmailAddress.email_address == email_address,
            model.EmailAddress.emailable_entity_type == 'USER'  # Replace 'User' with whatever enum or string you use to identify users in email_addresses
        )

        # Execute the query and fetch first result
        user = query.first()

        # Return the result if available, otherwise return None
        return user if user else None





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