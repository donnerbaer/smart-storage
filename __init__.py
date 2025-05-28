""" This module initializes the flask csrf protection for the application.
    It sets up the CSRF protection for the application using Flask-WTF.
"""

from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
