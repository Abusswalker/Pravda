import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin
from app import db, login_manager
from flask_login import UserMixin
import os
from datetime import datetime, timedelta
import base64


class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=True)
    position = db.Column(db.Boolean, nullable=True)
    email = db.Column(db.String, index=True, unique=True, nullable=True)
    hashed_password = db.Column(db.String, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.now)
    image = db.Column(db.String, nullable=True)
    # токены для подтверждения ауентификации в API
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    article = db.relationship("Articles", back_populates='user')
    comment = db.relationship("Comment", back_populates='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    # Получение токена для входа в API
    # API может использовать любой зарегестрированный пользователь
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    # обновление токена
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    # Проверка токена
    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Articles(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String, nullable=True)  # название новости
    heading = db.Column(db.String, nullable=True)   # краткое описание новости
    content = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)
    category = db.Column(db.Integer, nullable=True)
    likes = db.Column(db.Integer, nullable=True)
    dislikes = db.Column(db.Integer, nullable=True)

    user = db.relationship('User')
    comments = db.relationship("Comment", back_populates='article')

    def __repr__(self):
        return '<Article {}>'.format(self.body)


class Comment(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_creator = db.Column(db.Integer, db.ForeignKey("users.username"))
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"))
    content = db.Column(db.String, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.now)

    article = db.relationship("Articles")
    user = db.relationship("User")
