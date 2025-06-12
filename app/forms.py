""" Flask-WTF forms. """

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FileField, MultipleFileField, BooleanField, SelectField
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
    confirm_password = PasswordField(_l('Confirm Password'), validators=[DataRequired(), EqualTo('password')])
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
    confirm_password = PasswordField(_l('Confirm Password'), validators=[Optional(), EqualTo('password')])
    submit = SubmitField(_l('Update Profile Information'))


class ItemCreateForm(FlaskForm):
    """Form for creating a new item."""
    name = StringField(_l('Item Name'), validators=[DataRequired(), Length(max=100)])
    description = StringField(_l('Description'), validators=[Optional(), Length(max=500)])
    images = MultipleFileField('Images', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    barcode = StringField(_l('Barcode'), validators=[Optional(), Length(max=64)])
    storage_location = StringField(_l('Storage Location'), validators=[Optional(), Length(max=100)])
    submit = SubmitField(_l('Create Item'))


class ItemUpdateForm(FlaskForm):
    """Form for updating an existing item."""
    id = StringField(_l('Item ID'), render_kw={'readonly': True}, validators=[DataRequired()])
    name = StringField(_l('Item Name'), validators=[DataRequired(), Length(max=100)])
    description = StringField(_l('Description'), validators=[Optional(), Length(max=500)])
    images = MultipleFileField('Add Images', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    barcode = StringField(_l('Barcode'), validators=[Optional(), Length(max=64)])
    storage_location = SelectField(_l('Storage Location'), validators=[Optional(), Length(max=100)])
    submit = SubmitField(_l('Update Item'))


class ItemImageUpdateForm(FlaskForm):
    """Form for updating item images."""
    images = MultipleFileField('Images', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    image_descriptions = StringField(_l('Image Descriptions (comma separated)'), validators=[Optional(), Length(max=1000)])
    delete_images = BooleanField(_l('Delete Selected Images'), default=False, validators=[Optional()])
    submit = SubmitField(_l('Update Images'))