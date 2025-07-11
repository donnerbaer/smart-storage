""" Flask-WTF forms. """

from typing import List
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FileField, MultipleFileField, \
                    BooleanField, HiddenField, SelectField, RadioField, TextAreaField, \
                    IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange
from flask_babel import lazy_gettext as _l, gettext as _
from app.user.model import User
from app.resource.auth.model import Role, Permission
from app.resource.category.model import Category, CategoryColor
from app.resource.item.model import Item


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
    confirm_password = PasswordField(_l('Confirm Password'), validators=[Optional(), EqualTo('new_password')])
    submit = SubmitField(_l('Save Changes'))


class SearchForm(FlaskForm):
    """Form for searching items."""
    query = StringField(_l('Search'), validators=[DataRequired(), Length(max=4095)])
    submit = SubmitField(_l('Search'))


class ItemCreateForm(FlaskForm):
    """Form for creating a new item."""
    name = StringField(_l('Item Name'), validators=[DataRequired(), Length(max=100)])
    description = TextAreaField(_l('Description'), validators=[Optional(), Length(max=500)])
    images = MultipleFileField(_l('Images'), validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    storage_location = StringField(_l('Storage Location'), validators=[Optional(), Length(max=100)])
    submit = SubmitField(_l('Create Item'))


def build_item_form(
        categories: List[Category],
        users: List[User],
        item: Item = None,
        submit_text: str = _l('Submit')
    ) -> FlaskForm:
    """ Builds a dynamic form for item creation or update.

    This function creates a FlaskForm subclass with fields for item attributes,
    including categories and users. It can be used for both creating a new item
    and updating an existing one.

    Args:
        categories (list): A list of Category objects to create category fields.
        users (list): A list of User objects to populate the owner field.
        item (Item): An optional Item object to pre-fill the form for updates.
        submit_text (str): The text for the submit button.

    Returns:
        FlaskForm: A dynamically created form class with fields for item attributes.
    """

    fields: dict = {
        'id': HiddenField(_l('Item ID'), validators=[Optional()]),
        'name': StringField(_l('Item Name'), validators=[DataRequired(), Length(max=100)]),
        'description': TextAreaField(_l('Description'), validators=[Optional(), Length(max=500)]),
        'images': MultipleFileField(_l('Images'), validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])]),
        'owner': SelectField(_l('Owner'), choices=[], coerce=int, validators=[Optional()]),
        'storage_location': StringField(_l('Storage Location'), validators=[Optional()]),
        'quantity': IntegerField(_l('Quantity'), default=1, validators=[Optional(), NumberRange(min=0, message=_l('Quantity must be at least 0'))]),
        'submit': SubmitField(submit_text)
    }
    for category in categories:
        fields[f'category_{category.id}'] = BooleanField(category.name, default=False)

    DynamicItemUpdateForm = type('DynamicItemUpdateForm', (FlaskForm,), fields)

    class _Form(DynamicItemUpdateForm):
        """ Dynamically generated form for item creation or update.

        This form contains fields for item attributes, including categories and users(owner selection).
        It can be used for both creating a new item and updating an existing one.

        Args:
            categories (list): A list of Category objects to create category fields.
            users (list): A list of User objects to populate the owner field.
            item (Item): An optional Item object to pre-fill the form for updates.
            submit_text (str): The text for the submit button.
        """
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            owner_choices = [(0, _l('-- No Owner --'))] + [(user.id, user.username) for user in users]
            self.owner.choices = owner_choices

            if item:
                self.id.data = item.id
                self.name.data = item.name
                self.description.data = item.description
                self.storage_location.data = item.storage_location_id
                self.quantity.data = item.get_current_stock() if item.get_current_stock() is not None else 1
                self.owner.data = item.owner.id if item.owner else 0
                # Category marked as checked if item has it
                if hasattr(item, "categories"):
                    for category in categories:
                        field_name = f'category_{category.id}'
                        if category in item.categories:
                            getattr(self, field_name).data = True
                        else:
                            getattr(self, field_name).data = False

            else:
                for category in categories:
                    field_name = f'category_{category.id}'
                    if hasattr(self, field_name):
                        getattr(self, field_name).data = False
                self.owner.data = 0

    return _Form()


class ItemUpdateForm(FlaskForm):
    """Form for updating an existing item."""
    id = StringField(_l('Item ID'), render_kw={'readonly': True}, validators=[DataRequired()])
    name = StringField(_l('Item Name'), validators=[DataRequired(), Length(max=100)])
    description = TextAreaField(_l('Description'), validators=[Optional(), Length(max=500)])
    images = MultipleFileField(_l('Add Images'), validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    storage_location = HiddenField(_l('Storage Location'), validators=[Optional(), Length(max=100)])
    owner = SelectField(_l('Owner'), choices=[], coerce=int, validators=[Optional()])
    submit = SubmitField(_l('Save Changes'))


class ItemImageUpdateForm(FlaskForm):
    """Form for updating item images."""
    images = MultipleFileField(_l('Images'), validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    image_descriptions = StringField(_l('Image Descriptions (comma separated)'), validators=[Optional(), Length(max=1000)])
    delete_images = BooleanField(_l('Delete Selected Images'), default=False, validators=[Optional()])
    submit = SubmitField(_l('Update Images'))


class StorageCreateForm(FlaskForm):
    """Form for creating a new storage location."""
    name = StringField(_l('Storage Name'), validators=[DataRequired(), Length(max=100)])
    description = TextAreaField(_l('Description'), validators=[Optional(), Length(max=500)])
    images = MultipleFileField(_l('Storage Images'), validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    submit = SubmitField(_l('Create Storage'))


class StorageUpdateForm(FlaskForm):
    """Form for creating a new storage location."""
    name = StringField(_l('Storage Name'), validators=[DataRequired(), Length(max=100)])
    description = TextAreaField(_l('Description'), validators=[Optional(), Length(max=500)])
    images = MultipleFileField(_l('Storage Images'), validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    storage_location = HiddenField(_l('Parent Storage Location'), validators=[Optional(), Length(max=100)])
    submit = SubmitField(_l('Update Storage'))


class RoleCreateForm(FlaskForm):
    """Form for creating a new role."""
    name = StringField(_l('Role Name'), validators=[DataRequired(), Length(max=50)])
    description = TextAreaField(_l('Description'), validators=[Optional(), Length(max=255)])
    submit = SubmitField(_l('Create Role'))


class RoleUpdateForm(FlaskForm):
    """Form for updating an existing role."""
    name = StringField(_l('Role Name'), validators=[DataRequired(), Length(max=50)])
    description = TextAreaField(_l('Description'), validators=[Optional(), Length(max=255)])
    submit = SubmitField(_l('Update Role'))


class GroupCreateForm(FlaskForm):
    """Form for creating a new group."""
    name = StringField(_l('Group Name'), validators=[DataRequired(), Length(max=50)])
    description = TextAreaField(_l('Description'), validators=[Optional(), Length(max=255)])
    submit = SubmitField(_l('Create Group'))


class GroupUpdateForm(FlaskForm):
    """Form for updating an existing group."""
    name = StringField(_l('Group Name'), validators=[DataRequired(), Length(max=50)])
    description = TextAreaField(_l('Description'), validators=[Optional(), Length(max=255)])
    submit = SubmitField(_l('Update Group'))


def build_role_permission_form(role: Role, permissions: List[Permission]) -> FlaskForm:
    """ Builds a dynamic form for role permissions.
    
    This function creates a FlaskForm subclass with radio fields for each permission
    associated with a role. Each permission can be set to 'Allow' or 'Deny'.

    Args:
        role (Role): The role for which permissions are being managed.
        permissions (list): A list of Permission objects to create fields for.
    """
    class DynamicRolePermissionForm(FlaskForm):
        """Dynamically generated form for role permissions.
        
        This form contains radio fields for each permission, allowing the user
        to set permissions for the specified role.

        Attributes:
            submit (SubmitField): A submit button to update permissions.
        """
        submit = SubmitField(_l('Update Permissions'))

    # Dynamically add fields for each permission
    for perm in permissions:
        field_name = f'perm_{perm.id}'
        default_value = 'allow' if perm in role.permissions else 'deny'

        field = RadioField(
            label=perm.name,
            choices=[
                ('allow', _l('Allow')),
                ('deny', _l('Deny'))
            ],
            default=default_value
        )

        # Set the name attribute for the field, which is used in the template.
        setattr(DynamicRolePermissionForm, field_name, field)

    return DynamicRolePermissionForm()


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


class CategoryCreateForm(FlaskForm):
    """Form for creating a new category."""
    name = StringField(_l('Category Name'), validators=[DataRequired(), Length(max=100)])
    color = SelectField(_l('Choose Color'), choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField(_l('Create Category'))

    def __init__(self, *args, **kwargs):
        """Initialize the form with dynamic user choices.
        """
        super().__init__(*args, **kwargs)
        category_colors = CategoryColor.query.all()
        choices = [(category_color.id, category_color.name, category_color.color) for category_color in category_colors]
        self.color.choices = choices


class CategoryUpdateForm(FlaskForm):
    """Form for creating a new category."""
    name = StringField(_l('Category Name'), validators=[DataRequired(), Length(max=100)])
    color = SelectField(_l('Choose Color'), choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField(_l('Update Category'))

    def __init__(self, *args, **kwargs):
        """Initialize the form with dynamic user choices.
        """
        super().__init__(*args, **kwargs)
        category_colors = CategoryColor.query.all()
        choices = [(category_color.id, category_color.name, category_color.color) for category_color in category_colors]
        self.color.choices = choices
