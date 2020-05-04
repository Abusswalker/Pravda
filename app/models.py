import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin
from app import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=True)
    position = db.Column(db.Boolean, nullable=True)
    email = db.Column(db.String, index=True, unique=True, nullable=True)
    hashed_password = db.Column(db.String, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

    article = db.relationship("Articles", back_populates='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Articles(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String, nullable=True)
    heading = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)
    category = db.Column(db.Integer, nullable=True)

    user = db.relationship('User')

    def __repr__(self):
        return '<Article {}>'.format(self.body)