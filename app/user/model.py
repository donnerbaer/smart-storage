""" This module handles the Models for the application.
    It defines the User model for storing user information and authentication.
"""

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """ User model for storing user information """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    image_filename = db.Column(db.String(256), nullable=True)  # For user profile image

    def set_password(self, password) -> None:
        """ Set the user's password by hashing it. 

        Args:
            password (str): The plaintext password to be hashed and stored.

        Returns:
            None
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """ Check if the provided password matches the stored password hash.

        Args:
            password (str): The plaintext password to check against the stored hash.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission_name: str) -> bool:
        """ Check if the user has a specific permission.
        This method checks if the user belongs to any group that has the specified permission.
        This is done by iterating through the user's groups and their roles to find the permission.

        Args:
            permission_name (str): The name of the permission to check.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        for group in self.groups:
            for role in group.roles:
                if any(permission.name == permission_name for permission in role.permissions):
                    return True
        return False
