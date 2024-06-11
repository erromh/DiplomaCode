# admin_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import csv
from Module1.model import db, User, LoginLog


admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('main.login'))
    users = User.query.all()
    return render_template('main/admin_dashboard.html', users=users)

@admin.route('/admin/create_user', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        return redirect(url_for('main.login'))
    
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin') == 'on'
    
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), is_admin=is_admin)
    db.session.add(new_user)
    db.session.commit()
    
    flash('User created successfully')
    return redirect(url_for('admin.admin_dashboard'))

@admin.route('/admin/delete_user/<id>')
@login_required
def delete_user(id):
    if not current_user.is_admin:
        return redirect(url_for('main.login'))
    
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully')
    return redirect(url_for('admin.admin_dashboard'))

@admin.route('/admin/edit_user/<id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if not current_user.is_admin:
        return redirect(url_for('main.login'))
    
    user = User.query.get(id)
    
    if request.method == 'POST':
        user.email = request.form.get('email')
        user.name = request.form.get('name')
        user.is_admin = request.form.get('is_admin') == 'on'
        db.session.commit()
        
        flash('User updated successfully')
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('main/edit_user.html', user=user)

@admin.route('/admin/import_users', methods=['POST'])
@login_required
def import_users():
    if not current_user.is_admin:
        return redirect(url_for('main.login'))
    
    file = request.files['file']
    if file.filename.endswith('.csv'):
        stream = file.stream
        csv_file = csv.reader(stream, delimiter=',')
        for row in csv_file:
            email, name, password, is_admin = row
            new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), is_admin=is_admin.lower() == 'true')
            db.session.add(new_user)
        db.session.commit()
        
        flash('Users imported successfully')
    else:
        flash('Invalid file format')
    
    return redirect(url_for('admin.admin_dashboard'))

@admin.route('/admin/login_logs')
@login_required
def login_logs():
    if not current_user.is_admin:
        return redirect(url_for('main.login'))
    
    logs = LoginLog.query.all()
    return render_template('main/login_logs.html', logs=logs)
