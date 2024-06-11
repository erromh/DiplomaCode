from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_migrate import Migrate
from config import Config

bcrypt = Bcrypt()
db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Необходимо войти для просмотра этой страницы.'
mail = Mail()
bootstrap = Bootstrap()

app = Flask(__name__)

def create_app(config=Config):
    app.config.from_object(config)
    bcrypt.init_app(app)
    login.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    migrate = Migrate(app, db)

    from Module1.main.routes import main
    app.register_blueprint(main)

    from Module1.auth.routes import auth
    app.register_blueprint(auth)

    return app

