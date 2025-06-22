""" This module handles the main views of the application, including the index, dashboard, and error pages."""

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_babel import gettext as _
from app import db
from app.forms import ItemCreateForm, SearchForm
from app.resource.item.model import Item
from app.resource.storage_location.model import StorageLocation
from app.user.model import User


main_bp = Blueprint('main', __name__)


@main_bp.app_context_processor
def inject_search_form():
    """Injects the search form into the template context.
    
    This allows the search form to be accessible in all templates rendered within this blueprint.
    """
    return {
        'navbar_search_form': SearchForm()
    }


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
    users_count = db.session.query(User).count()
    locations_count = db.session.query(StorageLocation).count()
    items_count = db.session.query(Item).count()
    """ Prepare data for the dashboard.

        The data is structured as follows:
        1. The key is the HTML id of the chart.
        2. The value is a dictionary containing:
        - 'title': The title of the chart.
        - 'description': A description of the chart.
        - 'labels': A list of labels for the chart.
        - 'data': A list of data points for the chart.
        - 'name': The name of the chart.

        If required, you can add more charts by following the same structure.
        The data can be used to render charts using a JavaScript charting library like Chart.js.

        Example:
            {'overall_sum': {
                'title': 'Title of the chart',
                'description': 'Description of the chart',
                'labels': ['Label1', 'Label2', 'Label3'],
                'data': [12, 19, 3],
                'name': 'name of the chart'
            }
    """

    data = {
        "overall_sum": {
            "title": _("Overall Summary"),
            "description": _("This is the overall summary of your storage system."),
            "labels": [_("Users"), _("Locations"), _("Items")],
            "data": [users_count, locations_count, items_count],
            "name": 'overall_sum'
        }
    }
    return render_template('site.dashboard.html',
                           current_user=current_user,
                           data=data
                           )


@main_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search_view():
    """ Render the search page.
    
    Returns:
        Rendered template for the search page.
    """
    form = SearchForm()
    if form.validate_on_submit():
        items = Item.query.filter(Item.name.ilike(f"%{form.query.data}%")).all()
        users = User.query.filter(User.username.ilike(f"%{form.query.data}%")).all()
        storages = StorageLocation.query.filter(StorageLocation.name.ilike(f"%{form.query.data}%")).all()
        return render_template('site.search.result.html',
                               current_user=current_user,
                               items=items,
                               users=users,
                               storages=storages,
                               form=form
                               )

    return render_template('site.search.result.html', current_user=current_user)


@main_bp.app_errorhandler(403)
def page_not_found(e):
    """ Render the 403 error page.

    Args:
        e: The error that occurred.

    Returns:
        Rendered template for the 403 error page.
    """
    return render_template('error/403.html', current_user=current_user), 403


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
