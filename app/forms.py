""" Flask-WTF forms. """

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from flask_babel import lazy_gettext as _l


class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    submit = SubmitField(_l('Login'))

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    username = StringField(_l('Username'), validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField(_l('Email'), validators=[DataRequired(), Email(), Length(min=6, max=120)])
    password = PasswordField(_l('Password'), validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(_l('Confirm Password'), validators=[DataRequired(), EqualTo('password')])  # Fix here
    first_name = StringField(_l('First Name'), validators=[Optional(), Length(max=64)])
    last_name = StringField(_l('Last Name'), validators=[Optional(), Length(max=64)])
    submit = SubmitField(_l('Submit'))


class UserUpdateForm(FlaskForm):
    """Form for updating user profile."""
    username = StringField(_l('Username'), validators=[Optional(), Length(min=3, max=64)])
    email = StringField(_l('Email'), validators=[Optional(), Email(), Length(min=6, max=120)])
    first_name = StringField(_l('First Name'), validators=[Optional(), Length(max=64)])
    last_name = StringField(_l('Last Name'), validators=[Optional(), Length(max=64)])
    image = FileField(_l('Profile Image Filename'), validators=[Optional(), Length(max=256)])  # For user profile image
    delete_image = BooleanField(_l('Delete Profile Image'), default=False, validators=[Optional()])
    old_password = PasswordField(_l('Old Password'), validators=[DataRequired(), Length(min=8)])
    new_password = PasswordField(_l('New Password'), validators=[Optional(), Length(min=8)])
    confirm_password = PasswordField(_l('Confirm Password'), validators=[Optional(), EqualTo('password')])  # Fix here
    submit = SubmitField(_l('Update Profile Information'))
