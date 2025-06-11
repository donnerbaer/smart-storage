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
from app.forms import ItemCreateForm
from app.resource.item.model import Item, ItemImage
from app.user.model import User



item_bp = Blueprint('item', __name__)


@item_bp.route('/items/<int:item_id>', methods=['GET', 'POST'])
@login_required
def item_view(item_id):
    """ Render the item page.

    Args:
        item_id (int): The ID of the item to display.

    Returns:
        Rendered template for the item page.
    """
    item = Item.query.filter_by(id=item_id).first_or_404()
    qrcode_url = request.url
    return render_template('site.item.html', current_user=current_user, item=item, qrcode_url=qrcode_url)


@item_bp.route('/items/<int:item_id>/delete', methods=['GET'])
@login_required
def delete_item(item_id):
    """ Handle the deletion of an item, including its images.

    Args:
        item_id (int): The ID of the item to delete.

    Returns:
        Redirect to the catalog page after deletion.
    """
    item = db.session.query(Item).filter_by(id=item_id).first_or_404()
    images = db.session.query(ItemImage).filter_by(item_id=item_id).all()
    for image in images:
        image_path = os.path.join('img', 'item', image.filename)
        if os.path.exists(image_path):
            os.remove(image_path)
        db.session.delete(image)
    db.session.delete(item)
    db.session.commit()
    return redirect( url_for('main.catalog') )


@item_bp.route('/items/create', methods=['POST'])
@login_required
def create_item():
    """ Handle the creation of a new item.

    Returns:
        Redirect to the catalog page after item creation.
    """
    form = ItemCreateForm(request.form, meta={'csrf': False})
    form.images.data = request.files.getlist('images')
    if form.validate_on_submit():
        item = Item(
            name=form.name.data,
            description=form.description.data,
            storage_location_id=request.form.get('storage_location_id'),
            barcode=(form.barcode.data if form.barcode.data != '' else None),
        )
        db.session.add(item)
        db.session.commit()
        db.session.flush()
        db.session.refresh(item)

        if form.images.data:
            for image in form.images.data:
                if image and image.filename:
                    ext = image.filename[image.filename.rfind('.'):]
                    unique_name = f"{uuid4()}{ext}"
                    image.save(os.path.join('img', 'item', unique_name))
                    db.session.add(ItemImage(item_id=item.id, filename=unique_name))
            db.session.commit()
    return redirect( url_for('main.catalog') )
