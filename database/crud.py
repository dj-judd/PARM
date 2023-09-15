"""CRUD operations."""
import model

import create
import read
import update
import delete
import archive

from typing import Optional, Type, Tuple
from sqlalchemy import and_, desc
from sqlalchemy.orm import Session, Query, aliased

class Utils:
    @staticmethod
    def get_query_with_audit_join(session: Session, 
                                  entity: Type[model.AuditableBase],
                                  auditable_entity_type: model.AuditableEntityTypes) -> Tuple[Query, Type]:
        """Creates a query for the specified entity type with an outer join on AuditEntry."""

        # Create an alias for AuditEntry to keep track of the latest audit for the entity
        latest_audit = aliased(entity.AuditEntry)

        # Initialize the query with the specified entity
        query = model.db.session.query(entity)

        # Perform an outer join with the latest_audit alias
        # Filter the join by auditable entity type and related entity ID
        query = query.outerjoin(latest_audit, and_(latest_audit.auditable_entity_type == auditable_entity_type,
                                                   latest_audit.related_entity_id == entity.id))
        
        # Return both the query and the alias for the latest audit entry
        return query, latest_audit

    @staticmethod
    def filter_by_archived_status(query: Query, 
                                  latest_audit: Type, 
                                  include_archived: bool, 
                                  just_archived: bool) -> Query:
        """
        Filters the given query based on the archived status of the records.
        """
        
        # If both flags are True, the caller should handle it as it's an invalid case.

        # Check if the query should include archived records
        if include_archived:
            return query  # Return the original query unfiltered
        
        # Check if the query should include only archived records
        elif just_archived:
            return query.filter(latest_audit.is_archived == True)  # Return query filtered to include only archived records
        
        # Default: include only non-archived records
        else:
            return query.filter(latest_audit.is_archived == False)  # Return query filtered to exclude archived records
        
    # @staticmethod
    # def audit_entry_most_recent_for_entity(auditable_entity_type: model.AuditableEntityTypes,
    #                                        related_entity_id: int) -> Optional[model.AuditEntry]:
    #     """Fetch and return the most recent AuditEntry for a specific entity type and id, or None if no matching entry is found."""
    #     most_recent_entry = model.db.session.query(model.AuditEntry).filter_by(
    #         auditable_entity_type=auditable_entity_type,
    #         related_entity_id=related_entity_id
    #     ).order_by(desc(model.AuditEntry.created_at)).first()
    #     return most_recent_entry if most_recent_entry else None







if __name__ == '__main__':
    from server import app
    model.connect_to_db(app)