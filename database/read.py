"Read methods for DB Entities"

import model
import crud

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


def audit_entries_all(requesting_user_id: int):
    """Fetch and return all entries from the AuditEntry table, or None if the table is empty."""
    
    # Check if requesting user has access to view all of the audits at once.
    if has_permission(requesting_user_id, PermissionsType.CAN_VIEW_ALL_AUDITS.value):
        audit_entries = model.db.session.query(model.AuditEntry).all()
        return audit_entries if audit_entries else None
    return






def reservation_by_id(requesting_user_id: int,
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


def reservations_by_ids(requesting_user_id: int, 
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



def reservations_all(requesting_user_id: int,
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