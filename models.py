
from datetime import datetime
from ext import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()

class User(db.Model, BaseModel, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    role = db.Column(db.String)

    def __init__(self, username, email, password, role = "Guest"):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role

    def is_admin(self):
        return self.role == "Admin"

    def check_password(self, password):
        return check_password_hash(password, self.password)


class Concert(db.Model, BaseModel):
    __tablename__ = 'concerts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    datetime = db.Column(db.DateTime)
    img = db.Column(db.String)
    info = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_name = db.Column(db.String)

    user = db.relationship('User', backref='concerts')

    def __init__(self, name, datetime, img, info, user_id, user_name):
        self.name = name
        self.datetime = datetime
        self.img = img
        self.info = info
        self.user_id = user_id
        self.user_name = user_name if user_name else User.query.get(user_id).username


class Article(db.Model, BaseModel):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    img = db.Column(db.String)
    text = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_name = db.Column(db.String)
    created_at = db.Column(db.String)

    user = db.relationship('User', backref='articles')

    def __init__(self, title, img, text, user_id, user_name,created_at):
        self.title = title
        self.img = img
        self.text = text
        self.user_id = user_id
        self.user_name = user_name if user_name else User.query.get(user_id).username
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)