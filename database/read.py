"Read methods for DB Entities"

import model
from permissions import has_permission, PermissionsType
from backend_utils import utils

from typing import Optional, List
from sqlalchemy import desc
from sqlalchemy.orm import aliased

# READ


def global_settings():
    """Fetch and return the first entry from the global_settings table, or None if no entry exists."""
    
    global_settings = model.db.session.query(model.GlobalSettings).first()
    return global_settings if global_settings else None




def audit_entry_by_id(audit_entry_id: int):
    """Fetch and return an AuditEntry by its id, or None if no matching entry is found."""
    
    audit_entry = model.db.session.query(model.AuditEntry).filter_by(id=audit_entry_id).first()
    return audit_entry if audit_entry else None


def audit_entries_by_ids(audit_entry_ids: List[int]):
    """Fetch and return a list of AuditEntries by their ids, or None if no matching entry is found."""
    
    audit_entries = model.db.session.query(model.AuditEntry).filter(model.AuditEntry.id.in_(audit_entry_ids)).all()
    return audit_entries if audit_entries else None


def audit_entry_most_recent_for_entity(auditable_entity_type: model.AuditableEntityTypes,
                                        related_entity_id: int):
    """Fetch and return the most recent AuditEntry for a specific entity type and id, or None if no matching entry is found."""
    
    most_recent_entry = model.db.session.query(model.AuditEntry).filter_by(auditable_entity_type=auditable_entity_type,
                                                                            related_entity_id=related_entity_id
                                ).order_by(desc(model.AuditEntry.created_at)).first()
    return most_recent_entry if most_recent_entry else None


def audit_entries_all():
    """Fetch and return all entries from the AuditEntry table, or None if the table is empty."""
    
    audit_entries = model.db.session.query(model.AuditEntry).all()
    return audit_entries if audit_entries else None






def reservation_by_id(requesting_user_id: int,
                        reservation_id: int,
                        include_archived: bool = False):
    """Fetch and return a Reservation by its id, or None if no matching entry is found."""
    
    # Alias for the AuditEntry table
    latest_audit = aliased(model.AuditEntry)
    
    # Base query for the specified reservation ID and outer join on AuditEntry
    query = model.db.session.query(model.Reservation).\
        filter_by(id=reservation_id).\
        outerjoin(latest_audit,
                and_(latest_audit.auditable_entity_type == model.AuditableEntityTypes.RESERVATION.value,
                    latest_audit.related_entity_id == model.Reservation.id)).\
        order_by(latest_audit.created_at.desc()).\
        first()

    # Check permission and filter by archived status if needed
    if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value):
        if include_archived or latest_audit.is_archived == False:
            return query
    elif latest_audit.is_archived == False:
        return query

    # Return None if conditions not met
    return None
    

def reservations_by_ids(requesting_user_id: int,
                        reservation_ids: List[int],
                        include_archived: bool = False,
                        just_archived: bool = False):
    """Fetch and return a list of Reservations by their ids, or None if no matching entry is found."""
    
    # Raise error if both flags are True
    if include_archived and just_archived:
        raise ValueError("Both flags cannot be True.")

    # Alias for the AuditEntry table
    latest_audit = aliased(model.AuditEntry)

    # Base query filtering by given reservation IDs and outer join on AuditEntry
    query = model.db.session.query(model.Reservation).\
        filter(model.Reservation.id.in_(reservation_ids)).\
        outerjoin(latest_audit,
                and_(latest_audit.auditable_entity_type == model.AuditableEntityTypes.RESERVATION.value,
                    latest_audit.related_entity_id == model.Reservation.id)).\
        order_by(latest_audit.created_at.desc()).\
        distinct(model.Reservation.id)

    # Check permissions and filter query based on flags
    if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value):
        if include_archived:
            reservations = query.all()
        elif just_archived:
            reservations = query.filter(latest_audit.is_archived == True).all()
        else:
            reservations = query.filter(latest_audit.is_archived == False).all()
    else:
        if just_archived:
            return None  # No permission to view only archived
        reservations = query.filter(latest_audit.is_archived == False).all()

    # Return results or None if empty
    return reservations if reservations else None



def reservations_all(requesting_user_id: int,
                        include_archived: bool = False,
                        just_archived: bool = False):
    """Fetch and return all entries from the Reservation table, or None if the table is empty."""

    # Raise error if both flags are True
    if include_archived and just_archived:
        raise ValueError("Both flags cannot be True.")

    # Alias for AuditEntry table
    latest_audit = aliased(model.AuditEntry)

    # Base query with outer join on AuditEntry
    query = model.db.session.query(model.Reservation).\
        outerjoin(latest_audit,
                and_(latest_audit.auditable_entity_type == model.AuditableEntityTypes.RESERVATION.value,
                    latest_audit.related_entity_id == model.Reservation.id)).\
        order_by(latest_audit.created_at.desc()).\
        distinct(model.Reservation.id)

    # Check permissions and filter query based on flags
    if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ARCHIVED_RESERVATIONS.value):
        if include_archived:
            reservations = query.all()
        elif just_archived:
            reservations = query.filter(latest_audit.is_archived == True).all()
        else:
            reservations = query.filter(latest_audit.is_archived == False).all()
    else:
        if just_archived:
            return None  # No permission to view only archived
        reservations = query.filter(latest_audit.is_archived == False).all()

    # Return results or None if empty
    return reservations if reservations else None