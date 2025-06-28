""" Flask-WTF forms. """

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FileField, MultipleFileField, \
                    BooleanField, HiddenField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from flask_babel import lazy_gettext as _l
from app.user.model import User
from app.resource.auth.model import Role


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
    submit = SubmitField(_l('Registrate'))


class UserUpdateForm(FlaskForm):
    """Form for updating user profile."""
    username = StringField(_l('Username'), validators=[Optional(), Length(min=3, max=64)])
    email = StringField(_l('Email'), validators=[Optional(), Email(), Length(min=6, max=120)])
    first_name = StringField(_l('First Name'), validators=[Optional(), Length(max=64)])
    last_name = StringField(_l('Last Name'), validators=[Optional(), Length(max=64)])
    image = FileField(_l('Profile Image Filename'), validators=[Optional()])  # For user profile image
    delete_image = BooleanField(_l('Delete Profile Image'), default=False, validators=[Optional()])
    old_password = PasswordField(_l('Old Password'), validators=[DataRequired(), Length(min=8)])
    new_password = PasswordField(_l('New Password'), validators=[Optional(), Length(min=8)])
    confirm_password = PasswordField(_l('Confirm Password'), validators=[Optional(), EqualTo('password')])
    submit = SubmitField(_l('Save Changes'))


class SearchForm(FlaskForm):
    """Form for searching items."""
    query = StringField(_l('Search'), validators=[DataRequired(), Length(max=4095)])
    submit = SubmitField(_l('Search'))


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
    storage_location = HiddenField(_l('Storage Location'), validators=[Optional(), Length(max=100)])
    owner = SelectField(_l('Owner'), choices=[], coerce=int, validators=[Optional()])
    submit = SubmitField(_l('Save Changes'))


class ItemImageUpdateForm(FlaskForm):
    """Form for updating item images."""
    images = MultipleFileField('Images', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    image_descriptions = StringField(_l('Image Descriptions (comma separated)'), validators=[Optional(), Length(max=1000)])
    delete_images = BooleanField(_l('Delete Selected Images'), default=False, validators=[Optional()])
    submit = SubmitField(_l('Update Images'))


class StorageCreateForm(FlaskForm):
    """Form for creating a new storage location."""
    name = StringField(_l('Storage Name'), validators=[DataRequired(), Length(max=100)])
    description = StringField(_l('Description'), validators=[Optional(), Length(max=500)])
    images = MultipleFileField('Storage Images', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    submit = SubmitField(_l('Create Storage'))


class StorageUpdateForm(FlaskForm):
    """Form for creating a new storage location."""
    name = StringField(_l('Storage Name'), validators=[DataRequired(), Length(max=100)])
    description = StringField(_l('Description'), validators=[Optional(), Length(max=500)])
    images = MultipleFileField('Storage Images', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    storage_location = HiddenField(_l('Parent Storage Location'), validators=[Optional(), Length(max=100)])
    submit = SubmitField(_l('Update Storage'))


class RoleCreateForm(FlaskForm):
    """Form for creating a new role."""
    name = StringField(_l('Role Name'), validators=[DataRequired(), Length(max=50)])
    description = StringField(_l('Description'), validators=[Optional(), Length(max=255)])
    submit = SubmitField(_l('Create Role'))

# TODO: add possible permissions choices dynamically based on the application context
class RoleUpdateForm(FlaskForm):
    """Form for updating an existing role."""
    name = StringField(_l('Role Name'), validators=[DataRequired(), Length(max=50)])
    description = StringField(_l('Description'), validators=[Optional(), Length(max=255)])
    permissions = SelectField(_l('Permissions'), choices=[], coerce=int, multiple=True, validators=[Optional()])
    submit = SubmitField(_l('Update Role'))


class GroupCreateForm(FlaskForm):
    """Form for creating a new group."""
    name = StringField(_l('Group Name'), validators=[DataRequired(), Length(max=50)])
    description = StringField(_l('Description'), validators=[Optional(), Length(max=255)])
    submit = SubmitField(_l('Create Group'))


class GroupUpdateForm(FlaskForm):
    """Form for updating an existing group."""
    name = StringField(_l('Group Name'), validators=[DataRequired(), Length(max=50)])
    description = StringField(_l('Description'), validators=[Optional(), Length(max=255)])
    submit = SubmitField(_l('Update Group'))


class GroupMembershipForm(FlaskForm):
    """Form for managing group membership."""
    user = SelectField(_l('Choose an user'), choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField(_l('Add to Group'))

    def __init__(self, group_id=None, *args, **kwargs):
        """Initialize the form with dynamic user choices.
        Args:
            group_id (int): The ID of the group to filter users.
        """
        super().__init__(*args, **kwargs)
        choices = [(0, _l('-- Please Choose --'))]
        if group_id:
            users = User.query.filter(~User.groups.any(id=group_id)).all()
        else:
            users = User.query.all()
        choices += [(user.id, user.username) for user in users]
        self.user.choices = choices


class GroupAssignRoleForm(FlaskForm):
    """Form for assigning roles to a group."""
    role = SelectField(_l('Choose a role'), choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField(_l('Assign Role'))

    def __init__(self, group_id=None, *args, **kwargs):
        """Initialize the form with dynamic role choices.
        Args:
            group_id (int): The ID of the group to filter roles.
        """
        super().__init__(*args, **kwargs)
        choices = [(0, _l('-- Please Choose --'))]
        if group_id:
            roles = Role.query.filter(~Role.groups.any(id=group_id)).all()
        else:
            roles = Role.query.all()
        choices += [(role.id, role.name) for role in roles]
        self.role.choices = choices