from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from Module1 import db
from Module1.auth.forms import AdminRegisterForm, CreateAssignmentForm 
from Module1.model import User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')

@admin_bp.route('/admin/manage_users', methods=['GET', 'POST'])
@login_required
def manage_users():
    form = AdminRegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, admin=form.admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Пользователь создан успешно')
        return redirect(url_for('admin.manage_users'))
    return render_template('admin/manage_users.html', form=form)

@admin_bp.route('/admin/create_assignment', methods=['GET', 'POST'])
@login_required
def create_assignment():
    form = CreateAssignmentForm()
    if form.validate_on_submit():
        # Логика создания задания
        flash('Задание создано успешно')
        return redirect(url_for('admin.create_assignment'))
    return render_template('admin/create_assignment.html', form=form)
