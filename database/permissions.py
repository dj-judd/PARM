"""Permissions related logic."""

from backend_utils import utils

from typing import Optional
from sqlalchemy.orm import joinedload
from enum import Enum

import model

class PermissionsType(Enum):
    # Assets
    CAN_CREATE_ASSETS = "can_create_assets"
    CAN_VIEW_ASSETS = "can_view_assets"
    CAN_UPDATE_ASSETS = "can_update_assets"
    CAN_DELETE_ASSETS = "can_delete_assets"
    CAN_ARCHIVE_ASSETS = "can_archive_assets"
    CAN_VIEW_ARCHIVED_ASSETS = "can_view_archived_assets"
    
    # Users
    CAN_CREATE_USERS = "can_create_users"
    CAN_VIEW_USERS = "can_view_users"
    CAN_UPDATE_USERS = "can_update_users"
    CAN_DELETE_USERS = "can_delete_users"
    CAN_ARCHIVE_USERS = "can_archive_users"
    CAN_VIEW_ARCHIVED_USERS = "can_view_archived_users"
    CAN_ASSIGN_ROLE_TO_USERS = "can_assign_role_to_users"

    # Roles
    CAN_CREATE_ROLES = "can_create_roles"
    CAN_VIEW_ROLES = "can_view_roles"
    CAN_UPDATE_ROLES = "can_update_roles"
    CAN_DELETE_ROLES = "can_delete_roles"
    CAN_ARCHIVE_ROLES = "can_archive_roles"
    CAN_VIEW_ARCHIVED_ROLES = "can_view_archived_roles"
    CAN_ASSIGN_PERMISSION_TO_ROLES = "can_assign_permission_to_roles"

    # Areas
    CAN_CREATE_AREAS = "can_create_areas"
    CAN_VIEW_AREAS = "can_view_areas"
    CAN_UPDATE_AREAS = "can_update_areas"
    CAN_DELETE_AREAS = "can_delete_areas"
    CAN_ARCHIVE_AREAS = "can_archive_areas"
    CAN_VIEW_ARCHIVED_AREAS = "can_view_archived_areas"
    
    # Reservations
    CAN_CREATE_RESERVATIONS = "can_create_reservations"
    CAN_VIEW_RESERVATIONS = "can_view_reservations"
    CAN_UPDATE_RESERVATIONS = "can_update_reservations"
    CAN_DELETE_RESERVATIONS = "can_delete_reservations"
    CAN_ARCHIVE_RESERVATIONS = "can_archive_reservations"
    CAN_VIEW_ARCHIVED_RESERVATIONS = "can_view_archived_reservations"

    # Comments
    CAN_CREATE_COMMENTS = "can_create_comments"
    CAN_VIEW_COMMENTS = "can_view_comments"
    CAN_UPDATE_COMMENTS = "can_update_comments"
    CAN_DELETE_COMMENTS = "can_delete_comments"
    CAN_ARCHIVE_COMMENTS = "can_archive_comments"
    CAN_VIEW_ARCHIVED_COMMENTS = "can_view_archived_comments"
    
    # Flags
    CAN_FLAG_ISSUES = "can_flag_issues"
    CAN_CLEAR_FLAGS = "can_clear_flags"
    CAN_VIEW_ARCHIVED_FLAGS = "can_view_archived_flags"

    # Audits
    CAN_CREATE_AUDITS = "can_create_audits"
    CAN_VIEW_AUDITS = "can_view_audits"
    CAN_VIEW_ALL_AUDITS = "can_view_all_audits"
    CAN_UPDATE_AUDITS = "can_update_audits"
    CAN_DELETE_AUDITS = "can_delete_audits"


def has_permission(requesting_user_id: int,
                   required_permission: PermissionsType) -> bool:
    # Fetch the user and their roles
    user = model.db.session.query(model.User).options(
        joinedload(model.User.role_relationships)
        .joinedload(model.UserRole.role)
        .joinedload(model.Role.permission_relationships)
        .joinedload(model.RolePermission.permission)
    ).filter_by(id=requesting_user_id).first()

    if not user:
        return False

    for user_role in user.role_relationships:
        for role_permission in user_role.role.permission_relationships:
            if role_permission.permission.name == PermissionsType(required_permission).value:
                return True
                
    return False

def has_ownership(requesting_user_id: int) -> bool:

    # TODO: THIS IS FOR CHECKING IF THEY OWN WHAT THEY ARE TRYING TO CHANGE OR DELETE

    pass

class PermissionError:
    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
        else:
            self.message = f"{utils.RED_BOLD}ERROR:{utils.RESET} Permissions not met."
