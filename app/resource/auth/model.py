""" This module defines the Auth model for the database. """

from typing import Optional
from app import db


# Association Tables
role_permission = db.Table(
    'role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)

group_role = db.Table(
    'group_role',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

group_user = db.Table(
    'group_user',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)


class Permission(db.Model):
    """ Model representing a permission in the system. """
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Permission #{self.id} {self.name}>"


class Role(db.Model):
    """ Model representing a role in the system. """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    permissions = db.relationship('Permission', secondary='role_permission', backref='roles')

    def __repr__(self):
        return f"<Role #{self.id} {self.name}>"


    def add_permission(self, permission: Permission) -> None:
        """ Add a permission to the role.

        Args:
            permission (Permission): The permission to be added to the role.

        Returns:
            None
        """
        self.permissions.append(permission)
        db.session.commit()

    def remove_permission(self, permission: Permission) -> None:
        """ Remove a permission from the role.

        Args:
            permission (Permission): The permission to be removed from the role.

        Returns:
            None
        """
        self.permissions.remove(permission)
        db.session.commit()

    def has_permission(self, permission_name: str) -> bool:
        """ Check if the role has a specific permission by name.
        This method checks if the role has a permission with the given name.

        Args:
            permission_name (str): The name of the permission to check.

        Returns:
            bool: True if the role has the permission, False otherwise.
        """
        return any(permission.name == permission_name for permission in self.permissions)

    def add_role(self, role: 'Role') -> None:
        """ Add a role to the group.
        This method checks if the role is already associated with the group before adding it.

        Args:
            role (Role): The role to be added to the group.

        Returns:
            None
        """
        if not self.has_role(role.name):
            self.roles.append(role)
            db.session.commit()


    def has_role(self, role_name: str) -> bool:
        """ Check if the group has a specific role by name.
        This method checks if the group has a role with the given name.

        Args:
            role_name (str): The name of the role to check.

        Returns:
            bool: True if the group has the role, False otherwise.
        """
        return any(role.name == role_name for role in self.roles)


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    roles = db.relationship('Role', secondary='group_role', backref='groups')
    users = db.relationship('User', secondary='group_user', backref='groups')

    def __repr__(self):
        return f"<Group #{self.id} {self.name}>"
    
    def add_role(self, role: Role) -> None:
        """ Add a role to the group.
        This method checks if the role is already associated with the group before adding it.

        Args:
            role (Role): The role to be added to the group.

        Returns:
            None    
        """
        if not self.has_role(role.name):
            self.roles.append(role)
            db.session.commit()

    def remove_role(self, role: Role) -> None:
        """ Remove a role from the group. 
        This method checks if the role is associated with the group before removing it.

        Args:
            role (Role): The role to be removed from the group.

        Returns:
            None
        """
        if self.has_role(role.name):
            self.roles.remove(role)
            db.session.commit()
    

    def create(self, name: str) -> Optional['Group']:
        """ Create a new group with the given name.
        This method checks if a group with the same name already exists before creating a new one.

        Args:
            name (str): The name of the group to be created.

        Returns:
            Optional[Group]: The newly created group if it does not already exist, None otherwise.
        """
        if not self.is_group_exists(name):
            new_group = Group(name=name)
            db.session.add(new_group)
            db.session.commit()
            return new_group
        return None
    
    def has_role(self, role_name: str) -> bool:
        """ Check if the group has a specific role by name.

        Args:
            role_name (str): The name of the role to check.

        Returns:
            bool: True if the group has the role, False otherwise.
        """
        return any(role.name == role_name for role in self.roles)
    
    def is_group_exists(self, name: str) -> bool:
        """ Check if a group with the given name already exists.

        Args:
            name (str): The name of the group to check.

        Returns:
            bool: True if a group with the name exists, False otherwise.
        """
        return db.session.query(Group).filter_by(name=name).first() is not None

    def delete(self) -> None:
        """ Delete the group from the database.
        This method removes the group from the database and commits the changes.
        It does not check for any dependencies or associations before deletion, so use with caution.
        """
        db.session.delete(self)
        db.session.commit()
