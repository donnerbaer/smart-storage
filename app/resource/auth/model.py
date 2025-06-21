""" This module defines the Auth model for the database. """

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


    def add_permission(self, permission):
        """ Add a permission to the role. """
        self.permissions.append(permission)
        db.session.commit()

    def remove_permission(self, permission):
        """ Remove a permission from the role. """
        self.permissions.remove(permission)
        db.session.commit()

    def has_permission(self, permission_name):
        """ Check if the role has a specific permission by name. """
        return any(permission.name == permission_name for permission in self.permissions)

    def add_role(self, role):
        """ Add a role to the group. """
        if not self.has_role(role.name):
            self.roles.append(role)
            db.session.commit()

    def remove_role(self, role):
        """ Remove a role from the group. """
        if self.has_role(role.name):
            self.roles.remove(role)
            db.session.commit()

    def has_role(self, role_name):
        """ Check if the group has a specific role by name. """
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
        """ Add a role to the group. """
        if not self.has_role(role.name):
            self.roles.append(role)
            db.session.commit()

    def remove_role(self, role: Role) -> None:
        """ Remove a role from the group. """
        if self.has_role(role.name):
            self.roles.remove(role)
            db.session.commit()

    def create(self, name: str) -> 'Group':
        """ Create a new group with the given name. """
        if not self.is_group_exists(name):
            new_group = Group(name=name)
            db.session.add(new_group)
            db.session.commit()
            return new_group
        return None
    
    def is_group_exists(self, name: str) -> bool:
        """ Check if a group with the given name already exists. """
        return db.session.query(Group).filter_by(name=name).first() is not None

    def delete(self) -> None:
        """ Delete the group from the database. """
        db.session.delete(self)
        db.session.commit()
