"""Permissions related logic."""
from seed_database import populate_permissions
permission_id_mapping = populate_permissions()

def has_permission(user_id, permission_name):
    # Logic to check if a user with user_id has the permission named permission_name
    pass
