from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Маршрут для страницы управления пользователями
@app.route('/admin/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        if request.form['action'] == 'create':
            username = request.form['username']
            email = request.form['email']
            if User.query.filter_by(username=username).first() is not None:
                flash('Username already exists', 'error')
            elif User.query.filter_by(email=email).first() is not None:
                flash('Email already exists', 'error')
            else:
                new_user = User(username=username, email=email)
                db.session.add(new_user)
                db.session.commit()
                flash('User created successfully', 'success')
        elif request.form['action'] == 'delete':
            user_id = request.form['user_id']
            user = User.query.get(user_id)
            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully', 'success')
        elif request.form['action'] == 'edit':
            user_id = request.form['user_id']
            user = User.query.get(user_id)
            user.username = request.form['new_username']
            user.email = request.form['new_email']
            db.session.commit()
            flash('User updated successfully', 'success')

    users = User.query.all()
    return render_template('manage_users.html', users=users)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
