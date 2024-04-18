from flask_login import UserMixin
from .import db
from .import login_manager

class User(UserMixin, db.Model):
    __tablename__  = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    name = db.Column(db.String(1000))

@login_manager.user_loader
def load__user(user_id):
    return User.query.get(int(user_id))