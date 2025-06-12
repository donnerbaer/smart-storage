from app.resource.storage_location.model import StorageLocation

def get_storage_hierarchy(storage_id):
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