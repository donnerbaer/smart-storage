""" This module defines the Item model for the database. """

from app import db
from app.user.model import User
from app.resource.storage_location.model import StorageLocation



class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    owner_id = db.Column(db.String(100), db.ForeignKey('users.id'), nullable=True)
    barcode = db.Column(db.String(100), nullable=True, unique=True)
    storage_location_id = db.Column(db.Integer, db.ForeignKey('storage_location.id'), nullable=True)

    owner = db.relationship('User', backref='items')
    storage_location = db.relationship('StorageLocation', backref='items')

    def __repr__(self):
        return f"<Item #{self.id} {self.name}>"


class ItemImage(db.Model):
    __tablename__ = 'item_image'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    filename = db.Column(db.String(512), nullable=False)

    item = db.relationship('Item', backref='images')

    def __repr__(self):
        return f"<ItemImage #{self.id} for Item #{self.item_id}>"

class ItemStorageStock(db.Model):
    __tablename__ = 'item_storage_stock'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    storage_location_id = db.Column(db.Integer, db.ForeignKey('storage_location.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    item = db.relationship('Item', backref='stock')
    storage_location = db.relationship('StorageLocation', backref='stock')

    def __repr__(self):
        return f"<ItemStock #{self.id} for Item #{self.item_id} in {self.storage_location_id} with quantity {self.quantity}>"
