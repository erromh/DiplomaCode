from flask import Flask, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_user
from flask_user import login_required, UserManager, UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key' 

# Конфигурация Flask-User
class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id

user_manager = UserManager(app, User)

# Маршрут для страницы входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
