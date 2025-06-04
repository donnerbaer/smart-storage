""" This module handles the main views of the application, including the index, dashboard, and error pages."""

import os
from flask import Blueprint, render_template
from flask import request
from flask import jsonify, send_from_directory, redirect
from flask_login import login_required, current_user
from flask_babel import get_locale, gettext as _
from flask_wtf.csrf import generate_csrf
from app.resource.storage_location.model import StorageLocation
from app.resource.item.model import Item
from app.user.model import User
from app import db



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
