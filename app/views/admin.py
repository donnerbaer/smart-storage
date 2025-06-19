from flask import Blueprint, render_template
from flask import redirect, url_for, request
from flask_login import login_required, current_user
from flask_babel import gettext as _
from app import db
from app.user.model import User
from app.forms import GroupCreateForm, GroupUpdateForm
from app.resource.auth.model import Role, Group, Permission
from app.utils.decorators import check_permissions


admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates/admin')


@admin_bp.route('/', methods=['GET'])
@login_required
@check_permissions([
                'admin.backend.access'
            ])
def admin_view():
    """Render the admin dashboard."""
    return render_template('admin/site.index.html', current_user=current_user)


### * Roles Management ###


@admin_bp.route('/roles', methods=['GET'])
@login_required
@check_permissions([
                'admin.backend.access',
                'admin.roles.read'
            ])
def roles_view():
    """Render the roles management page."""
    roles = db.session.query(Role).all()
    return render_template('admin/site.roles.html', current_user=current_user, roles=roles)


@admin_bp.route('/roles', methods=['POST'])
@login_required
@check_permissions([
                'admin.backend.access',
                'admin.roles.create'
            ])
def role_post():
    """Create a new role."""
    redirect(url_for('admin.roles_view'))


@admin_bp.route('/roles/<int:role_id>', methods=['GET'])
@login_required
@check_permissions([
                'admin.backend.access',
                'admin.role.read'
            ])
def role_view(role_id):
    role = Role.query.get_or_404(role_id)
    return render_template('admin/site.role.html', current_user=current_user, role=role)


@admin_bp.route('/roles/<int:role_id>/update', methods=['GET'])
@login_required
@check_permissions([
                'admin.backend.access',
                'admin.role.update'
            ])
def update_role(role_id):
    role = Role.query.get_or_404(role_id)
    # Logic to update the role
    return render_template('admin/site.role.update.html', current_user=current_user, role=role)


@admin_bp.route('/roles/<int:role_id>/update', methods=['POST'])
@login_required
@check_permissions([
                'admin.backend.access',
                'admin.role.update'
            ])
def update_role_post(role_id):
    role = Role.query.get_or_404(role_id)
    # Logic to update the role
    return redirect(url_for('admin.role_view', role_id=role.id))


@admin_bp.route('/roles/<int:role_id>/delete', methods=['GET'])
@login_required
@check_permissions([
                'admin.backend.access',
                'admin.role.delete'
            ])
def delete_role(role_id: int):
    """Delete a role by its ID."""
    role = Role.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    return redirect(url_for('admin.roles_view'))


### * Groups Management ###


@admin_bp.route('/groups', methods=['GET'])
@login_required
@check_permissions([
                'admin.backend.access',
                'admin.groups.read'
            ])
def groups_view():
    groups = db.session.query(Group).all()
    form_create_group = GroupCreateForm(request.form)
    return render_template('admin/site.groups.html', current_user=current_user, groups=groups, form_create_group=form_create_group)


@admin_bp.route('/groups', methods=['POST'])
@login_required
@check_permissions([
                'admin.backend.access',
                'admin.group.create'
            ])
def create_group():
    """Create a new group."""
    form = GroupCreateForm(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('admin.groups_view'))
    
    if not Group.query.filter_by(name=form.name.data).first():
        new_group = Group(
                    name=form.name.data,
                    description=form.description.data if form.description.data and form.description != '' else None
                    )
        db.session.add(new_group)
        db.session.commit()
    return redirect(url_for('admin.groups_view'))


@admin_bp.route('/groups/<int:group_id>', methods=['GET'])
@login_required
@check_permissions([
                'admin.backend.access',
                'admin.group.read'
            ])
def group_view(group_id):
    group = Group.query.get_or_404(group_id)
    form_update_group = GroupUpdateForm(obj=group)
    return render_template('admin/site.group.html',
                           current_user=current_user,
                           group=group,
                           form_update_group=form_update_group)



@admin_bp.route('/groups/<int:group_id>', methods=['POST'])
@login_required
@check_permissions([
                'admin.backend.access',
                'admin.group.update'
            ])
def update_group(group_id: int):
    """Render the group update page."""
    group = Group.query.get_or_404(group_id)
    form = GroupUpdateForm(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('admin.group_view', group_id=group_id))
    if not Group.query.filter_by(name=form.name.data).first():
        group.name = form.name.data
        group.description = form.description.data if form.description.data and form.description != '' else None
        db.session.add(group)
        db.session.commit()

    return redirect(url_for('admin.group_view', group_id=group.id))


@admin_bp.route('/groups/<int:group_id>/delete', methods=['GET'])
@login_required
@check_permissions([
                'admin.backend.access',
                'admin.group.delete'
            ])
def delete_group(group_id: int):
    """Delete a group by its ID."""
    group = Group.query.get_or_404(group_id)
    db.session.delete(group)
    db.session.commit()
    return redirect(url_for('admin.groups_view'))


@admin_bp.route('/groups/<int:group_id>/add_role/<int:role_id>', methods=['GET'])
@login_required
@check_permissions([
                'admin.backend.access',
                'admin.group.update'
            ])
def add_role_to_group(group_id: int, role_id: int):
    """Add a role to a group."""
    group = Group.query.get_or_404(group_id)
    role = Role.query.get_or_404(role_id)
    group.add_role(role)
    return redirect(url_for('admin.group_view', group_id=group.id))


@admin_bp.route('/groups/<int:group_id>/remove_role/<int:role_id>', methods=['GET'])
@login_required
@check_permissions([
                'admin.backend.access',
                'admin.group.update'
            ])
def remove_role_from_group(group_id: int, role_id: int):
    """Remove a role from a group."""
    group = Group.query.get_or_404(group_id)
    role = Role.query.get_or_404(role_id)
    group.remove_role(role)
    return redirect(url_for('admin.group_view', group_id=group.id))


@admin_bp.route('/groups/<int:group_id>/add_user/<int:user_id>', methods=['GET'])
@login_required
@check_permissions([
                'admin.backend.access',
                'admin.group.update'
            ])
def add_user_to_group(group_id: int, user_id: int):
    """Add a user to a group."""
    group = Group.query.get_or_404(group_id)
    user = User.query.get_or_404(user_id)
    if user not in group.users:
        group.users.append(user)
        db.session.commit()
    return redirect(url_for('admin.group_view', group_id=group.id))


@admin_bp.route('/groups/<int:group_id>/remove_user/<int:user_id>', methods=['GET'])
@login_required
@check_permissions([
                'admin.backend.access',
                'admin.membership.remove'
            ])
def remove_user_from_group(group_id: int, user_id: int):
    """Remove a user from a group."""
    group = Group.query.get_or_404(group_id)
    user = User.query.get_or_404(user_id)
    if user in group.users:
        group.users.remove(user)
        db.session.commit()
    return redirect(url_for('admin.group_view', group_id=group.id))

