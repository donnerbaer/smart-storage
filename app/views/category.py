""" Category views
"""

from flask import Blueprint, render_template, url_for
from flask import request, redirect
from flask_babel import gettext as _
from flask_login import login_required, current_user
from app import db
from app.forms import CategoryCreateForm, CategoryUpdateForm
from app.resource.category.model import Category, CategoryColor
from app.utils.decorators import check_permissions


category_bp = Blueprint('category', __name__)


@category_bp.route('/categories', methods=['GET'])
@login_required
@check_permissions(['categories.read'])
def categories_view():
    """ Render the categories page.
    
    Returns:
        Rendered template for the categories page with a list of all categories.
    """
    categories = db.session.query(Category).all()
    form_category_create = CategoryCreateForm()

    return render_template('site.categories.html',
                            current_user=current_user,
                            categories=categories,
                            form_category_create=form_category_create
                        )


@category_bp.route('/categories', methods=['POST'])
@login_required
@check_permissions(['categories.read'])
def create_category():
    """ Render the categories page.

    Returns:
        Redirect to the categories view after creating a new category.
    """
    form_category_create = CategoryCreateForm(request.form)
    if form_category_create.validate_on_submit():
        new_category = Category(
                            name=form_category_create.name.data,
                            color_id=form_category_create.color.data
                        )
        db.session.add(new_category)
        db.session.commit()

    return redirect(url_for('category.categories_view'))


@category_bp.route('/categories/<int:category_id>', methods=['GET'])
@login_required
@check_permissions(['category.read'])
def category_view(category_id):
    """ Render the category page.

    Args:
        category_id (int): The ID of the category to display.

    Returns:
        Rendered template for the category page.
    """
    category = Category.query.filter_by(id=category_id).first_or_404()
    form_category_update = CategoryUpdateForm(
        name=category.name,
        color=category.color_id,
    )

    return render_template('site.category.html',
                            current_user=current_user,
                            category=category,
                            form_category_update=form_category_update
                        )


@category_bp.route('/categories/<int:category_id>/update', methods=['POST'])
@login_required
@check_permissions(['category.update'])
def update_category(category_id):
    """ Handle the update of a category.

    Args:
        category_id (int): The ID of the category to update.

    Returns:
        Redirect to the category view after updating the category.
    """
    category = Category.query.filter_by(id=category_id).first_or_404()
    form = CategoryUpdateForm(request.form)

    if form.validate_on_submit():
        category.name= form.name.data
        category.color_id = form.color.data or 1
    
        db.session.add(category)
        db.session.commit()

    return redirect(url_for('category.category_view', category_id=category.id))


@category_bp.route('/categories/<int:category_id>/delete', methods=['GET'])
@login_required
@check_permissions(['category.delete'])
def delete_category(category_id):
    """ Handle the deletion of a category.

    Args:
        category_id (int): The ID of the category to delete.

    Returns:
        Redirect to the categories view after deleting the category.
    """
    category = Category.query.filter_by(id=category_id).first_or_404()
    db.session.delete(category)
    db.session.commit()

    return redirect(url_for('category.categories_view'))
