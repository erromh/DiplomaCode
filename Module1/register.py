from flask import Flask, render_template, redirect, url_for, request, flash
from flask_user import UserManager, UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'  # Секретный ключ для защиты сессий и токенов

# Конфигурация Flask-User
class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

user_manager = UserManager(app, User)

# Маршрут для страницы регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            flash('Email and password are required', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email is already in use', 'error')
        else:
            user = User(email=email, password=password)
            # Здесь должна быть логика сохранения нового пользователя в базу данных
            flash('Registration successful', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
