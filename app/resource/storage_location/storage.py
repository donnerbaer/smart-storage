"""Storage Location Hierarchy Management
    This module provides functions to manage and retrieve storage location hierarchies.
"""

from typing import List
from app.resource.storage_location.model import StorageLocation


def get_storage_hierarchy_ids(storage_id) -> List[int]:
    """ Get the storage hierarchy IDs from the root to the current storage location.
    
    Args:
        storage_id (int): The ID of the storage location to start from.
        
    Returns:
        list: A list of storage location IDs representing the hierarchy from root to the current storage location.
    """
    hierarchy = []
    current_id = storage_id
    while current_id:
        hierarchy.insert(0, current_id)  # vorne anfügen für Reihenfolge von oben nach unten
        storage = StorageLocation.query.filter_by(id=current_id).first()
        if storage and storage.parent_id:
            current_id = storage.parent_id
        else:
            break
    return hierarchy


def get_storage_hierarchy(storage_id) -> List[StorageLocation]:
    """Get the storage hierarchy from the root to the current storage location.

    Args:
        storage_id (int): The ID of the storage location to start from.

    Returns:
        list: A list of StorageLocation objects representing the hierarchy from root to the current storage location.
    """
    hierarchy = []
    current_id = storage_id
    while current_id:
        storage = StorageLocation.query.filter_by(id=current_id).first()
        if storage:
            hierarchy.insert(0, storage)  # vorne anfügen für Reihenfolge von oben nach unten
            current_id = storage.parent_id
        else:
            break
    return hierarchy
