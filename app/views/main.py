""" This module handles the main views of the application, including the index, dashboard, and error pages."""

import os
<<<<<<< Updated upstream
from flask import Blueprint, render_template
=======
from uuid import uuid4
from flask import Blueprint, render_template, url_for, flash
>>>>>>> Stashed changes
from flask import request
from flask import jsonify, send_from_directory, redirect
from flask_login import login_required, current_user
from flask_babel import get_locale, gettext as _, lazy_gettext
from flask_wtf.csrf import generate_csrf
from app.resource.storage_location.model import StorageLocation
from app.resource.item.model import Item
from app.user.model import User
from app import db
<<<<<<< Updated upstream
from app.forms import UserUpdateForm

=======
from app.forms import UserUpdateForm, ItemCreateForm, RegistrationForm
>>>>>>> Stashed changes


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """ Render the index page """
    return render_template('site.index.html', current_user=current_user)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """ Render the dashboard page """
    request_url = request.url
    print(f"Request URL: {request_url}")
    return render_template('site.dashboard.html', current_user=current_user)


@main_bp.app_errorhandler(404)
def page_not_found(e):
    """ Render the 404 error page """
    return render_template('error/404.html', current_user=current_user), 404


@main_bp.app_errorhandler(500)
def internal_server_error(e):
    """ Render the 500 error page """
    return render_template('error/500.html', current_user=current_user), 500


@main_bp.route('/items/<int:item_id>', methods=['GET', 'POST'])
@login_required
def show_item(item_id):
    """ Render the item page """
    item = Item.query.filter_by(id=item_id).first_or_404()
    # item = Item.query.filter_by(id=item_id).all_or_404()
    item_dict = {
        'id' : item.id,
        'name': item.name,
        'storage_location': item.storage_location_id,
        'images': [
            f'https://placehold.co/600x400?text=Item+{item_id}.1',
            f'https://placehold.co/600x400?text=Item+{item_id}.2',
            f'https://placehold.co/600x400?text=Item+{item_id}.3'
        ],
        '_links': {
            'self': {'href': request.url, 'method': 'GET', 'title': ''},
        }  
    }
    return render_template('site.item.html', current_user=current_user, item=item_dict)


@main_bp.route('/catalog')
@login_required
def catalog():
    """ Render the catalog page """
    return render_template('site.catalog.html', current_user=current_user)


@main_bp.route('/users', methods=['GET'])
@login_required
def users():
    """ Render the users page """
    users = db.session.query(User).all()
    return render_template('site.users.html', current_user=current_user, users=users)


<<<<<<< Updated upstream
=======
@main_bp.route('/users/create', methods=['GET'])
@login_required
def create_user():
    """ Render the create user page.
    
    Returns:
        Rendered template for the create user page with a form.
    """
    form = RegistrationForm()
    return render_template('site.user.create.html', current_user=current_user, form=form)


@main_bp.route('/users/create', methods=['POST'])
@login_required
def create_user_post():
    """ Handle the creation of a new user, for already logged-in users.
    This function checks if the passwords match, if the username and email are unique,
    and then creates a new user in the database.
    If any validation fails, it flashes an error message and redirects to the users page.
    
    Returns:
        Redirect to the users page after successful creation.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash(lazy_gettext('Passwords do not match'))
            return redirect(url_for('main.users'))
        if db.session.query(User).filter_by(username=form.username.data).first():
            flash(lazy_gettext('Username already exists'))
            return redirect(url_for('main.users'))
        if db.session.query(User).filter_by(email=form.email.data).first():
            flash(lazy_gettext('Email already exists'))
            return redirect(url_for('main.users'))
        user = User(username=form.username.data,
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data
                    )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(lazy_gettext('Registration successful! Please log in.'))
    return redirect(url_for('main.users'))


@main_bp.route('/users/<int:user_id>/delete', methods=['GET'])
@login_required
def delete_user(user_id):
    """ Handle the deletion of a user.
    
    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        Redirect to the users page after deletion.
    """
    user = db.session.query(User).filter_by(id=user_id).first_or_404()
    delete_current_user = False
    if user.id == current_user.id:
        delete_current_user = True
    if user.image_filename and user.image_filename != get_default_user_image():
        image_path = os.path.join('img', 'user', user.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)
    db.session.delete(user)
    db.session.commit()
    if delete_current_user:
        redirect(url_for('auth.logout'))
    return redirect('/users')


>>>>>>> Stashed changes
def is_image_name_valid(image_name):
    """ Check if the image name is not None """
    return image_name is not None and image_name != ""


def get_default_user_image():
    """ Get the default user image """
    return "default_user_image.png"


@main_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
def user(user_id):
    """ Render the users page """
    user = db.session.query(User).filter_by(id=user_id).first_or_404()
    if not is_image_name_valid(user.image_filename):
        user.image_filename = get_default_user_image()
    return render_template('site.user.html', current_user=current_user, user=user)


@main_bp.route('/users/<int:user_id>/update', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    """ Update user information """
    user = db.session.query(User).filter_by(id=user_id).first_or_404()
    form = UserUpdateForm(obj=user)
    
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(f'/users/{user.id}')

    if not is_image_name_valid(user.image_filename):
        user.image_filename = get_default_user_image()

    return render_template('site.user.update.html', current_user=current_user, user=user, form=form)


@main_bp.route('/my-profile', methods=['GET'])
@login_required
def my_profile():
    """ Render the users page """
    user = db.session.query(User).filter_by(id=current_user.id).first_or_404()
    if not is_image_name_valid(user.image_filename):
        user.image_filename = get_default_user_image()
    return render_template('site.user.html', current_user=current_user, user=user)


@main_bp.route('/img/user/<path:filename>')
@login_required
def serve_user_image(filename):
    """Serve an image from the filesystem."""
    image_dir = os.path.join(os.getcwd(), 'img', 'user')
    return send_from_directory(image_dir, filename)


@main_bp.route('/img/item/<path:filename>')
@login_required
def serve_item_image(filename):
    """Serve an image from the filesystem."""
    image_dir = os.path.join(os.getcwd(), 'img', 'item')
    return send_from_directory(image_dir, filename)


@main_bp.route('/img/current_user', methods=['GET'])
@login_required
def serve_current_user_image():
    """Serve the current user's image."""
    user = db.session.query(User).filter_by(id=current_user.id).first_or_404()
    if not is_image_name_valid(user.image_filename):
        user.image_filename = get_default_user_image()
    return redirect(f'/img/user/{user.image_filename}')
