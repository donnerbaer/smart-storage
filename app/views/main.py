""" This module handles the main views of the application, including the index, dashboard, and error pages."""

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_babel import gettext as _
from app import db
from app.forms import ItemCreateForm
from app.resource.item.model import Item


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """ Render the index page
    
    Returns:
        Rendered template for the index page.
    """
    return render_template('site.index.html', current_user=current_user)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """ Render the dashboard page.
    
    Returns:
        Rendered template for the dashboard page.
    """
    return render_template('site.dashboard.html', current_user=current_user)


@main_bp.app_errorhandler(404)
def page_not_found(e):
    """ Render the 404 error page.

    Args:
        e: The error that occurred.

    Returns:
        Rendered template for the 404 error page.
    """
    return render_template('error/404.html', current_user=current_user), 404


@main_bp.app_errorhandler(500)
def internal_server_error(e):
    """ Render the 500 error page.
    
    Args:
        e: The error that occurred.

    Returns:
        Rendered template for the 500 error page.
    """
    return render_template('error/500.html', current_user=current_user), 500


@main_bp.route('/catalog')
@login_required
def catalog():
    """ Render the catalog page.
    
    Returns:
        Rendered template for the catalog page with a list of items.
    """
    items = db.session.query(Item).all()
    form = ItemCreateForm()
    return render_template('site.catalog.html',
                           current_user=current_user,
                           items=items,
                           form=form
                           )
