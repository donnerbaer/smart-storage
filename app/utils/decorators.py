""" Decorators for Flask routes to manage user access and permissions. """
# app/utils/decorators.py

from typing import List
from flask import redirect, url_for, abort
from flask_login import current_user
from functools import wraps
from app.resource.auth.model import Group, Role, Permission

def anonymous_required(f):
    """ Decorator to restrict access to anonymous users only. """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """ Check if the user is authenticated. If so, redirect to the main page. """
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


def check_permissions(required_permissions: List[str]):
    """Decorator to check if the user has the required permissions."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                print("User is not authenticated.")
                return redirect(url_for('auth.login'))

            for required_permission in required_permissions:
                if not current_user.has_permission(required_permission):
                    print(f"User {current_user.username} does not have permission: {required_permission}")
                    abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator
