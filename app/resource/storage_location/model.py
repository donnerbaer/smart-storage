""" This module defines the StorageLocation model for the database. """
from app import db

class StorageLocation(db.Model):
    __tablename__ = 'storage_location'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('storage_location.id'), nullable=True)
    parent = db.relationship('StorageLocation', remote_side=[id], backref='children')
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<StorageLocation #{self.id} {self.name}>"

    def get_root(self):
        current = self
        while current.parent is not None:
            current = current.parent
        return current


class StorageLocationImage(db.Model):
    __tablename__ = 'storage_location_image'

    id = db.Column(db.Integer, primary_key=True)
    storage_location_id = db.Column(db.Integer, db.ForeignKey('storage_location.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    storage_location = db.relationship('StorageLocation', backref='images')

    def __repr__(self):
        return f"<StorageLocationImage {self.filename}>"
