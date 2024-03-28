from flask_login import UserMixin
from . import db

# class User(UserMixin, db.Model)

class User(UserMixin, db.Model):
    __tablename__  = 'users'
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    name = db.Column(db.String(1000))

    #role_id = db.Column(db.Integer, db.ForeignKey())