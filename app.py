
from flask import Flask, render_template, request, redirect, url_for

# https://codepen.io/joshsorosky/pen/gaaBoB

app = Flask(__name__, template_folder = 'Module1 (administration)/Register')
app._static_folder = 'Module1 (administration)/static'

registered_users = []

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    # Проверка на совпадение паролей
    if password != confirm_password:
        return "Пароли не совпадают. Попробуйте еще раз."

    # добавление пользователя в список
    registered_users.append({'username': username, 'email': email, 'password': password})

    return f"Регистрация успешна! Добро пожаловать, {username}."

if __name__ == '__main__':
    app.run(debug=True)
