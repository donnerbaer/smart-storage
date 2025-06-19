""" Storage Blueprint for managing storage locations.
This module provides routes to display storage locations and individual storage details.
"""

import os
from uuid import uuid4
from flask import Blueprint, render_template
from flask import request, redirect, url_for
from flask_babel import gettext as _
from flask_login import login_required, current_user
from app import db
from app.forms import StorageCreateForm, StorageUpdateForm
from app.resource.storage_location.model import StorageLocation, StorageLocationImage, \
                                                StorageLocationImage
from app.resource.item.model import ItemStorageStock
from app.resource.storage_location.storage import get_storage_hierarchy, \
                                                get_storage_hierarchy_ids


storage_bp = Blueprint('storage', __name__)


@storage_bp.route('/storages', methods=['GET'])
@login_required
def storages_view():
    """ Render the storages page.
    
    Returns:
        Rendered template for the storages page with a list of storage locations.
    """
    storages = db.session.query(StorageLocation).all()
    form = StorageCreateForm()
    return render_template('site.storages.html',
                           current_user=current_user,
                           storages=storages,
                           form=form
                           )


@storage_bp.route('/storages', methods=['POST'])
@login_required
def create_storage():
    """ Create a new storage location.
    
    Returns:
        Redirects to the storages page after creation.
    """
    form = StorageCreateForm(request.form)
    form.images.data = request.files.getlist('images')
    if form.validate_on_submit():
        storage = StorageLocation(
            name=form.name.data,
            description=form.description.data if form.description.data else None
        )
        db.session.add(storage)
        db.session.merge(storage)

        if form.images.data:
            for image in form.images.data:
                if image and image.filename:
                    ext = image.filename[image.filename.rfind('.'):]
                    unique_name = f"{uuid4()}{ext}"
                    image.save(os.path.join('img', 'storage', unique_name))
                    db.session.add(StorageLocationImage(storage_location_id=storage.id, filename=unique_name))
        db.session.commit()
        return redirect(url_for('storage.storages_view'))
    else:
        return render_template('site.storages.html',
                               current_user=current_user,
                               form=form,
                               error=form.errors
                               )


@storage_bp.route('/storages/<int:storage_id>', methods=['GET'])
@login_required
def storage_view(storage_id):
    """ Render the storage page.
    
    Args:
        storage_id (int): The ID of the storage location to display.

    Returns:
        Rendered template for the storage page.
    """
    storage = db.session.query(StorageLocation).filter_by(id=storage_id).first_or_404()
    qrcode_url = request.url
    form = StorageUpdateForm(
        id=storage_id,
        name=storage.name,
        description=storage.description,
        images=storage.images,
        storage_location=storage.parent_id
    )
    # storage_hierarchy requiered for for the breadcrumbs in the storage view
    # storage_hierarchy_ids requiered for the select field in the storage update form
    return render_template('site.storage.html',
                           current_user=current_user,
                           storage=storage,
                           qrcode_url=qrcode_url,
                           form=form,
                           storage_hierarchy=get_storage_hierarchy(storage.id),
                           storage_hierarchy_ids=get_storage_hierarchy_ids(storage.id)
                           )


@storage_bp.route('/storages/<int:storage_id>/update', methods=['POST'])
@login_required
def update_storage(storage_id):
    """ Update an existing storage location.
    
    Args:
        storage_id (int): The ID of the storage location to update.

    Returns:
        Redirects to the storages page after update.
    """
    storage = db.session.query(StorageLocation).filter_by(id=storage_id).first_or_404()
    form = StorageUpdateForm(request.form)
    form.images.data = request.files.getlist('images')
    if form.validate_on_submit():

        storage.name = form.name.data
        storage.description = form.description.data
        # ! attention: different naming between form and model
        storage.parent_id = form.storage_location.data if form.storage_location.data != '' else None
        if form.images.data:
            for image in form.images.data:
                if image and image.filename:
                    ext = image.filename[image.filename.rfind('.'):]
                    unique_name = f"{uuid4()}{ext}"
                    image.save(os.path.join('img', 'storage', unique_name))
                    db.session.add(StorageLocationImage(storage_location_id=storage.id, filename=unique_name))

        db.session.add(storage)
        db.session.commit()
    return redirect( url_for('storage.storage_view', storage_id=storage_id) )





@storage_bp.route('/storages/<int:storage_id>/delete', methods=['GET'])
@login_required
def delete_storage(storage_id):
    """ Delete a storage location.
    
    Args:
        storage_id (int): The ID of the storage location to delete.

    Returns:
        Redirects to the storages page after deletion.
    """
    storage = db.session.query(StorageLocation).filter_by(id=storage_id).first_or_404()
    
    # remove all images associated with the storage location
    # from the filesystem and database
    images = db.session.query(StorageLocationImage).filter_by(storage_location_id=storage.id).all()
    for image in images:
        image_path = os.path.join('img', 'storage', image.filename)
        if os.path.exists(image_path):
            os.remove(image_path)
        db.session.delete(image)

    # remove all item stocks associated with the storage location
    item_stocks = db.session.query(ItemStorageStock).filter_by(storage_location_id=storage.id).all()
    for stock in item_stocks:
        db.session.delete(stock)

    # remove the storage location itself
    db.session.delete(storage)
    db.session.commit()
    return redirect( url_for('storage.storages_view') )


@storage_bp.route('/api/storages/list/childs/<int:storage_id>', methods=['GET'])
@login_required
def api_get_all_child_storages(storage_id):
    """ Get all storage locations.
    
    Returns:
        List of all storage locations.
    """
    if storage_id == 0:
        storage_id = None
    storages = db.session.query(StorageLocation).filter_by(parent_id=storage_id).all()
    storage_data = []
    for storage in storages:
        storage_data.append(
                {
                    "id": storage.id,
                    "name": storage.name
                }
            )
    return {'storages': storage_data}, 200


@storage_bp.route('/api/storages/list', methods=['GET'])
@login_required
def api_get_all_storages():
    """ Get all storage locations.
    
    Returns:
        List of all storage locations.
    """
    storages = db.session.query(StorageLocation).all()
    storage_data = []
    for storage in storages:
        storage_data.append(
                {
                    "id": storage.id,
                    "name": storage.name
                }
            )
    return {'storages': storage_data}, 200
