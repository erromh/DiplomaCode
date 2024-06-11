from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from Module1 import bcrypt, db
from Module1.auth.forms import LoginForm, RegisterForm, SendResetPasswordRequestForm, ResetPasswordForm, AdminRegisterForm
from Module1.auth.email import send_password_reset_email
from Module1.model import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Password incorrect', category='danger')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have logged out now.', category='info')
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        role = form.role.data
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Регистрация', form=form)

@auth.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    form = AdminRegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_password, role='admin')
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register_admin.html', form=form)

@auth.route('/send_reset_password_request', methods=['GET', 'POST'])
def send_reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = SendResetPasswordRequestForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/send_reset_password_request.html', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm(request.form)
    if form.validate_on_submit():
        user = User.verify_reset_password_token(token)
        user.password = bcrypt.generate_password_hash(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

