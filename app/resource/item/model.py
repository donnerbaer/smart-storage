""" This module defines the Item model for the database. """

from app import db
from app.user.model import User
from app.resource.storage_location.model import StorageLocation



class Item(db.Model):
    """ Represents an item in the storage system.

    Attributes:        
        id (int): Unique identifier for the item.
        name (str): Name of the item.
        description (str): Description of the item.
        owner_id (str): ID of the user who owns the item.
        storage_location_id (int): ID of the storage location where the item is stored.

    Relationships:
        owner (User): The user who owns the item.
        storage_location (StorageLocation): The storage location where the item is stored.
        categories (list): List of categories associated with the item.
    """
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    owner_id = db.Column(db.String(100), db.ForeignKey('users.id'), nullable=True)
    storage_location_id = db.Column(db.Integer, db.ForeignKey('storage_location.id'), nullable=True)

    owner = db.relationship('User', backref='items')
    storage_location = db.relationship('StorageLocation', backref='items')
    categories = db.relationship('Category', secondary='item_category', back_populates='items')

    def __repr__(self):
        return f"<Item #{self.id} {self.name}>"

    def get_current_stock(self) -> int:
        """ Returns the current stock quantity of the item.

        Args:
            None

        Returns:
            int: The current stock quantity of the item, or None if no stock record exists.

        """
        stock = ItemStorageStock.query.filter_by(item_id=self.id).order_by(ItemStorageStock.timestamp.desc()).first()
        return stock.quantity if stock else None

    def get_create_timestamp(self) -> str:
        """ Returns the creation timestamp of the item in a human-readable format.

        Args:
            None

        Returns:
            str: The formatted creation timestamp as a string.
        """
        stock = ItemStorageStock.query.filter_by(item_id=self.id).order_by(ItemStorageStock.timestamp).first()
        return stock.format_timestamp() if stock else "Unknown"

class ItemImage(db.Model):
    """ Represents an image associated with an item.

    Attributes:
        id (int): Unique identifier for the image.
        item_id (int): ID of the item to which the image belongs.
        filename (str): Name of the image file.

    Relationships:
        item (Item): The item associated with the image.
    """
    __tablename__ = 'item_image'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    filename = db.Column(db.String(512), nullable=False)

    item = db.relationship('Item', backref='images')

    def __repr__(self):
        return f"<ItemImage #{self.id} for Item #{self.item_id}>"

class ItemStorageStock(db.Model):
    """ Represents the stock of an item in a specific storage location.

    Attributes:
        id (int): Unique identifier for the stock record.
        item_id (int): ID of the item for which the stock is recorded.
        storage_location_id (int): ID of the storage location where the item is stored.
        quantity (int): Quantity of the item in stock.
        timestamp (datetime): Timestamp of when the stock record was created.

    Relationships:
        item (Item): The item associated with the stock record.
    """
    __tablename__ = 'item_storage_stock'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    storage_location_id = db.Column(db.Integer, db.ForeignKey('storage_location.id'), nullable=True)
    quantity = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    item = db.relationship('Item', backref = 'stocks')

    def __repr__(self):
        return f"<ItemStock #{self.id} for Item #{self.item_id} with quantity {self.quantity}>"

    def format_timestamp(self):
        """ Returns the timestamp in a human-readable format.
        
        Args:
            None

        Returns:
            str: The formatted timestamp as a string.
        """
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
