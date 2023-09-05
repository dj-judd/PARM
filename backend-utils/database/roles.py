"""Roles related logic."""
from seed_database import populate_roles
role_id_mapping = populate_roles()

def user_has_role(user_id, role_name):
    # Logic to check if a user with user_id has the role named role_name
    pass

def role_has_permission(role_name, permission_name):
    # Logic to check if a role named role_name has the permission named permission_name
    pass
