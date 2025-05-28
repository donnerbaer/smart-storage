""" This module handles the Configuration settings for the Flask application.
    It loads environment variables and sets up the database URI, secret key, and other settings.
"""

import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    """ Configuration class for the Flask application. """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_BINDS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['de', 'en']
    BABEL_DEFAULT_LOCALE = 'en'
