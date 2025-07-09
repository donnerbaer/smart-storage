""" This script seeds the database with initial data for permissions, roles, groups, and users. """

from app import create_app, db
from app.resource.auth.model import Permission, Role, Group
from app.resource.category.model import Category, CategoryColor
from app.user.model import User


PERMISSIONS = [
    # * Admin Permissions
    {"name": "admin.backend.access", "description": "Access admin backend"},

    {"name": "admin.roles.read", "description": "Read roles"},
    {"name": "admin.role.read", "description": "Read role"},
    {"name": "admin.role.create", "description": "Create role"},
    {"name": "admin.role.update", "description": "Update role"},
    {"name": "admin.role.delete", "description": "Delete role"},
    {"name": "admin.role.update_permission", "description": "Grant and revoke permissions to role"},

    {"name": "admin.groups.read", "description": "Read groups"},
    {"name": "admin.group.read", "description": "Read group"},
    {"name": "admin.group.create", "description": "Create group"},
    {"name": "admin.group.update", "description": "Update group"},
    {"name": "admin.group.delete", "description": "Delete group"},
    {"name": "admin.group.assign_role", "description": "Assign role to group"},
    {"name": "admin.group.remove_role", "description": "Remove role from group"},

    {"name": "admin.users.read", "description": "Read users"},
    {"name": "admin.user.read", "description": "Read user"},
    {"name": "admin.user.create", "description": "Create user"},
    {"name": "admin.user.update", "description": "Update user"},
    {"name": "admin.user.delete", "description": "Delete user"},
    {"name": "admin.user.password.change", "description": "Change user password"},
    {"name": "admin.membership.assign", "description": "Assign user to group"},
    {"name": "admin.membership.remove", "description": "Remove user from group"},

    {"name": "admin.permissions.grant", "description": "Grant permissions to user"},
    {"name": "admin.permissions.revoke", "description": "Revoke permissions from user"},
    {"name": "admin.permissions.view", "description": "View user permissions"},


    # * Storage Permissions
    {"name": "storages.read", "description": "Read storage locations"},
    {"name": "storage.read", "description": "Read storage location"},
    {"name": "storage.create", "description": "Create storage location"},
    {"name": "storage.update", "description": "Update storage location"},
    {"name": "storage.delete", "description": "Delete storage location"},
    {"name": "storage.assign", "description": "Assign storage to another parent storage"},
    {"name": "storage.reassign", "description": "Reassign storage to another parent storage"},
    {"name": "storage.unassign", "description": "Unassign storage to another parent storage"},


    # * Storage Item Permissions
    {"name": "items.read", "description": "Read items"},
    {"name": "item.read", "description": "Read item"},
    {"name": "item.create", "description": "Create item"},
    {"name": "item.update", "description": "Update item"},
    {"name": "item.delete", "description": "Delete item"},

    {"name": "item.assign.storage", "description": "Assign item to storage"},
    {"name": "item.reassign.storage", "description": "Reassign item to a different storage"},
    {"name": "item.unassign.storage", "description": "Remove storage assignment from item"},

    {"name": "item.assign.user", "description": "Assign item to user"},
    {"name": "item.reassign.user", "description": "Reassign item to a different user"},
    {"name": "item.unassign.user", "description": "Remove user assignment from item"},

    {"name": "item.description.update", "description": "Update item description"},
    {"name": "item.name.update", "description": "Update item name"},
    {"name": "item.image.create", "description": "Add item image"},
    {"name": "item.image.update", "description": "Update item image"},
    {"name": "item.image.delete", "description": "Delete item image"},


    # * Category Permissions
    {"name": "categories.read", "description": "Read categories"},
    {"name": "category.read", "description": "Read category"},
    {"name": "category.create", "description": "Create category"},
    {"name": "category.update", "description": "Update category"},
    {"name": "category.delete", "description": "Delete category"},
]


ROLES = [
    {
        "name": "admin",
        "description": "Administrator role",
        "permissions": [
                "admin.backend.access",

                "admin.roles.read",
                "admin.role.read",
                "admin.role.create",
                "admin.role.update",
                "admin.role.delete",
                "admin.role.update_permission",

                "admin.groups.read",
                "admin.group.read",
                "admin.group.create",
                "admin.group.update",
                "admin.group.delete",
                "admin.group.assign_role",
                "admin.group.remove_role",

                "admin.users.read",
                "admin.user.read",
                "admin.user.create",
                "admin.user.update",
                "admin.user.delete",
                "admin.user.password.change",
                "admin.membership.assign",
                "admin.membership.remove",

                "admin.permissions.grant",
                "admin.permissions.revoke",
                "admin.permissions.view",

                "storages.read",
                "storage.read",
                "storage.create",
                "storage.update",
                "storage.delete",
                "storage.assign",
                "storage.reassign",
                "storage.unassign",

                "items.read",
                "item.read",
                "item.create",
                "item.update",
                "item.delete",

                "item.assign.storage",
                "item.reassign.storage",
                "item.unassign.storage",

                "item.assign.user",
                "item.reassign.user",
                "item.unassign.user",

                "item.description.update",
                "item.name.update",
                "item.image.create",
                "item.image.update",
                "item.image.delete",

                "categories.read",
                "category.read",
                "category.create",
                "category.update",
                "category.delete"
            ]
    },
    {
        "name": "user",
        "description": "Standard user role",
        "permissions": [
                "storages.read",
                "storage.read",
                "storage.create",
                "storage.update",
                "storage.delete",
                "storage.assign",
                "storage.reassign",
                "storage.unassign",

                "items.read",
                "item.read",
                "item.create",
                "item.update",
                "item.delete",

                "item.assign.storage",
                "item.reassign.storage",
                "item.unassign.storage",

                "item.assign.user",
                "item.reassign.user",
                "item.unassign.user",

                "item.description.update",
                "item.name.update",
                "item.image.create",
                "item.image.update",
                "item.image.delete",

                "categories.read",
                "category.read",
                "category.create",
                "category.update",
                "category.delete"
        ]
    }
]

GROUPS = [
    {
        "name": "Admin",
        "description": "Administrative group [DO NOT DELETE]",
        "roles": ["admin"]
    },
    {
        "name": "User",
        "description": "Standard user group [DO NOT DELETE]",
        "roles": ["user"]
    }
]

USERS = [
    {
        "username": "admin",
        "password": "admin",
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@example.org"
        }
]

CATEGORY_COLORS = [
    {"name": "Blue",        "color": "primary"},
    {"name": "Gray",        "color": "secondary"},
    {"name": "Green",       "color": "success"},
    {"name": "Red",         "color": "danger"},
    {"name": "Yellow",      "color": "warning"},
    {"name": "Light Blue",  "color": "info"},
    {"name": "Black",       "color": "dark"}
]

CATEGORIES = [
    {
        "name": "Food",
        "color": "success"
    },
    {
        "name": "Electronics",
        "color": "primary"
    },
    {
        "name": "Clothing",
        "color": "info"
    },
    {
        "name": "Furniture",
        "color": "warning"
    }
]

def seed_permissions():
    for perm_data in PERMISSIONS:
        if not Permission.query.filter_by(name=perm_data["name"]).first():
            p = Permission(**perm_data)
            db.session.add(p)
    db.session.commit()


def seed_roles():
    for role_data in ROLES:
        role = Role.query.filter_by(name=role_data["name"]).first()
        if not role:
            role = Role(name=role_data["name"], description=role_data["description"])
            db.session.add(role)
            db.session.commit()

        # Berechtigungen zuweisen
        for perm_name in role_data["permissions"]:
            perm = Permission.query.filter_by(name=perm_name).first()
            if perm and perm not in role.permissions:
                role.permissions.append(perm)
        db.session.commit()


def seed_groups():
    for group_data in GROUPS:
        group = Group.query.filter_by(name=group_data["name"]).first()
        if not group:
            group = Group(name=group_data["name"], description=group_data["description"])
            db.session.add(group)
            db.session.commit()

        for role_name in group_data["roles"]:
            role = Role.query.filter_by(name=role_name).first()
            if role and role not in group.roles:
                group.roles.append(role)
        db.session.commit()


def seed_users():
    for user_data in USERS:
        user = User.query.filter_by(username=user_data["username"]).first()
        if not user:
            user = User(username=user_data["username"],
                        email=user_data["email"],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name']
                    )
            user.set_password(user_data["password"])
            db.session.add(user)
            db.session.commit()

        admin_group = Group.query.filter_by(name="Admin").first()
        if admin_group and user not in admin_group.users:
            admin_group.users.append(user)
            db.session.commit()


def seed_category_colors():
    for color_data in CATEGORY_COLORS:
        color = CategoryColor.query.filter_by(name=color_data["name"]).first()
        if not color:
            color = CategoryColor(
                        name=color_data["name"],
                        color=color_data["color"]
                    )
            db.session.add(color)
    db.session.commit()


def seed_categories():
    for category_data in CATEGORIES:
        category = Category.query.filter_by(name=category_data["name"]).first()
        if not category:
            category_color = CategoryColor.query.filter_by(color=category_data["color"]).first()
            
            category = Category(
                            name=category_data["name"],
                            color=category_color
                        )
            db.session.add(category)
    db.session.commit()


def run_seeding():
    print("Seeding permissions...")
    seed_permissions()
    print("Seeding roles...")
    seed_roles()
    print("Seeding groups...")
    seed_groups()
    print("Seeding users...")
    seed_users()
    print("Seeding category colors...")
    seed_category_colors()
    print("Seeding categories...")
    seed_categories()
    print("Done.")


app = create_app()

with app.app_context():
    db.create_all()
    run_seeding()
