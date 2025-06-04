""" This module defines the Item model for the database. """

from app import db
from app.user.model import User


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    owner_id = db.Column(db.String(100), db.ForeignKey('users.id'), nullable=True)
    barcode = db.Column(db.String(100), nullable=True, unique=True)
    storage_location_id = db.Column(db.Integer, db.ForeignKey('storage_location.id'), nullable=True)

    def __repr__(self):
        return f"<Item #{self.id} {self.name}>"