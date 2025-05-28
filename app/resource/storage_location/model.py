""" This module defines the StorageLocation model for the database. """
from app import db

class StorageLocation(db.Model):
    __tablename__ = 'storage_location'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    parent_id = db.Column(db.Integer, db.ForeignKey('storage_location.id'), nullable=True)
    parent = db.relationship('StorageLocation', remote_side=[id], backref='children')

    # Convenience: reference to items in this location
    items = db.relationship('Item', backref='location', lazy='dynamic')

    def __repr__(self):
        return f"<StorageLocation {self.name}>"