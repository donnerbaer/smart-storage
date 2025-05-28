""" Decorators for Flask routes to manage user access and permissions. """
# app/utils/decorators.py

from flask import redirect, url_for
from flask_login import current_user
from functools import wraps

def anonymous_required(f):
    """ Decorator to restrict access to anonymous users only. """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """ Check if the user is authenticated. If so, redirect to the main page. """
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))  # oder wohin du umleiten willst
        return f(*args, **kwargs)
    return decorated_function
