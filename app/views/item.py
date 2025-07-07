""" This module handles the item views of the application.
It provides routes for displaying items, creating new items, and managing item images.
"""

import os
from uuid import uuid4
from flask import Blueprint, render_template, url_for
from flask import request, redirect
from flask_babel import gettext as _
from flask_login import login_required, current_user
from app import db
from app.forms import build_item_form
from app.resource.category.model import Category
from app.resource.item.model import Item, ItemImage, ItemStorageStock
from app.resource.storage_location.storage import get_storage_hierarchy_ids, get_storage_hierarchy
from app.user.model import User
from app.utils.decorators import check_permissions


item_bp = Blueprint('item', __name__)


@item_bp.route('/items/<int:item_id>', methods=['GET'])
@login_required
@check_permissions(['items.read'])
def item_view(item_id):
    """ Render the item page.

    Args:
        item_id (int): The ID of the item to display.

    Returns:
        Rendered template for the item page.
    """
    item = Item.query.filter_by(id=item_id).first_or_404()
    users = db.session.query(User).all()
    categories = db.session.query(Category).all()
    qrcode_url = request.url

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
        "quantity_over_time": {
            "title": _("Quantity Over Time"),
            "description": _("This chart shows the quantity of the item over time."),
            "labels": [ stock.format_timestamp() for stock in item.stocks],
            "data": [ stock.quantity for stock in item.stocks ],
            "name": 'quantity_over_time'
        }
    }

    form = build_item_form(
                        item=item,
                        users=users,
                        categories=categories,
                        submit_text=_('Save Changes')
                    )

    # storage_hierarchy requiered for for the breadcrumbs in the item view
    # storage_hierarchy_ids requiered for the select field in the item update form
    return render_template('site.item.html',
                           current_user=current_user,
                           item=item,
                           data=data,
                           qrcode_url=qrcode_url,
                           form=form,
                           categories=categories,
                           getattr=getattr,
                           storage_hierarchy=get_storage_hierarchy(item.storage_location_id),
                           storage_hierarchy_ids=get_storage_hierarchy_ids(item.storage_location_id)
                           )


@item_bp.route('/items/<int:item_id>/delete', methods=['GET'])
@login_required
@check_permissions(['item.delete'])
def delete_item(item_id):
    """ Handle the deletion of an item, including its images.

    Args:
        item_id (int): The ID of the item to delete.

    Returns:
        Redirect to the catalog page after deletion.
    """
    item = db.session.query(Item).filter_by(id=item_id).first_or_404()
    images = db.session.query(ItemImage).filter_by(item_id=item_id).all()
    db.session.query(ItemStorageStock).filter_by(item_id=item_id).delete()
    for image in images:
        image_path = os.path.join('img', 'item', image.filename)
        if os.path.exists(image_path):
            os.remove(image_path)
        db.session.delete(image)
    db.session.delete(item)
    db.session.commit()
    return redirect( url_for('main.catalog') )


@item_bp.route('/items/<int:item_id>/update', methods=['POST'])
@login_required
@check_permissions(['item.update'])
def update_item_post(item_id):
    """ Handle the update of an existing item.

    Args:
        item_id (int): The ID of the item to update.

    Returns:
        Redirect to the item view page after updating.
    """
    item = db.session.query(Item).filter_by(id=item_id).first_or_404()
    users = db.session.query(User).all()
    categories = db.session.query(Category).all()

    form = build_item_form(
                        item=item,
                        users=users,
                        categories=categories,
                        submit_text=_('Save Changes')
                    )
    form.process(request.form)

    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data if form.description.data != '' else None
        item.storage_location_id = form.storage_location.data
        item.owner_id = form.owner.data if form.owner.data > 0 else None

        # Update categories
        item.categories.clear()
        for category in categories:
            if f'category_{category.id}' in request.form:
                item.categories.append(category)

        # Handle image uploads
        form.images.data = request.files.getlist('images')
        if form.images.data:
            for image in form.images.data:
                if image and image.filename:
                    ext = image.filename[image.filename.rfind('.'):]
                    unique_name = f"{uuid4()}{ext}"
                    image.save(os.path.join('img', 'item', unique_name))
                    db.session.add(ItemImage(item_id=item_id, filename=unique_name))

        if item.get_current_stock() != form.quantity.data:
            # Update stock quantity
            item.stocks.append(
                ItemStorageStock(
                    item_id=item.id,
                    quantity=form.quantity.data if form.quantity.data else 1
                )
            )

        db.session.add(item)
        db.session.commit()
    return redirect( url_for('item.item_view', item_id=item_id) )


@item_bp.route('/items', methods=['POST'])
@login_required
@check_permissions(['item.create'])
def create_item():
    """ Handle the creation of a new item.

    Returns:
        Redirect to the catalog page after item creation.
    """
    users = db.session.query(User).all()
    categories = db.session.query(Category).all()

    form = build_item_form(
        item=None,
        users=users,
        categories=categories,
        submit_text=_('Create Item')
    )

    if form.validate_on_submit():
        owner_id = request.form.get('owner')
        item = Item(
            name=form.name.data,
            description=form.description.data if form.description.data != '' else None,
            storage_location_id=form.storage_location.data,
            owner_id=owner_id if owner_id != '0' else None
        )

        quantity = ItemStorageStock(
                item_id=item.id,
                quantity=form.quantity.data if form.quantity.data else 1
            )
        item.stocks.append(quantity)

        db.session.add(item)
        db.session.commit()
        db.session.refresh(item)

        # add categories
        for category in categories:
            if f'category_{category.id}' in request.form:
                item.categories.append(category)
        db.session.add(item)
        db.session.commit()

        form.images.data = request.files.getlist('images')
        if form.images.data:
            for image in form.images.data:
                if image and image.filename:
                    ext = image.filename[image.filename.rfind('.'):]
                    unique_name = f"{uuid4()}{ext}"
                    image.save(os.path.join('img', 'item', unique_name))
                    db.session.add(ItemImage(item_id=item.id, filename=unique_name))
            db.session.commit()
    return redirect(url_for('main.catalog'))
