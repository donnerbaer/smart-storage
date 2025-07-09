""" This module defines the Category model for the application. """

from app import db
from app.resource.item.model import Item
from app.resource.storage_location.model import StorageLocation


item_category = db.Table(
    'item_category',
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

storage_category = db.Table(
    'storage_category',
    db.Column('storage_location_id', db.Integer, db.ForeignKey('storage_location.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)


class Category(db.Model):
    """Category groups for items and storage locations.
    
    Attributes:
        id (int): Unique identifier for the category.
        name (str): Name of the category.
        color_id (int): Foreign key to the CategoryColor model, default is 1.
    """
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('category_color.id'), default=1, nullable=False)

    items = db.relationship('Item', secondary=item_category, back_populates='categories')
    storage_locations = db.relationship('StorageLocation', secondary=storage_category, back_populates='categories')
    color = db.relationship('CategoryColor', backref='categories', lazy=True)

    def __repr__(self):
        return f"<Category #{self.id} {self.name}>"


class CategoryColor(db.Model):
    """Color model for categories.
    
    Attributes:
        id (int): Unique identifier for the color.
        name (str): Name of the color.
        color (str): Colornames from bootstrap-framework.
    """
    __tablename__ = 'category_color'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Color #{self.id} {self.name} ({self.color})>"
