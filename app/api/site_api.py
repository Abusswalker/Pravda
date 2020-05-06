from flask import jsonify, abort
from werkzeug.security import generate_password_hash

from app import db
from app.api import bp
from app.models import User, Articles
from app.api.reqparse_user import parser_user
from app.api.reqparse_articles import parser_article
from app.api.auth import token_auth


def abort_if_user_not_found(user_id):
    users = db.session.query(User).get(user_id)
    if not users:
        abort(404, message=f"User {user_id} not found")


def abort_if_article_not_found(article_id):
    articles = db.session.query(Articles).get(article_id)
    if not articles:
        abort(404, message=f"Article {article_id} not found")


def set_password(password):
    return generate_password_hash(password)


# Api для пользователей
@bp.route('/users/<int:user_id>', methods=['GET'])
@token_auth.login_required
def get_user(user_id):
    abort_if_user_not_found(user_id)
    users = db.session.query(User).get(user_id)
    return jsonify({'user': users.to_dict(only=('username', 'position', 'email', 'hashed_password'))})


@bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(user_id):
    abort_if_user_not_found(user_id)
    user = db.session.query(User).get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': 'OK'})


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def post_user():
    args = parser_user.parse_args()
    user = User(
        username=args['username'],
        email=args['email'],
        position=args['position'],
        hashed_password=set_password(args['hashed_password'])
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': 'OK'})


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    users = db.session.query(User).all()
    return jsonify(
        {'users': [item.to_dict(only=('username', 'position', 'email', 'hashed_password')) for item in users]})


# API для новостей
@bp.route('/articles/<int:article_id>', methods=['GET'])
@token_auth.login_required
def get_article(article_id):
    abort_if_article_not_found(article_id)
    article = db.session.query(Articles).get(article_id)
    return jsonify({'article': article.to_dict(only=('creator', 'title', 'heading', 'content', "category"))})


@bp.route('/articles/<int:article_id>', methods=['DELETE'])
@token_auth.login_required
def delete_article(article_id):
    abort_if_article_not_found(article_id)
    article = db.session.query(Articles).get(article_id)
    db.session.delete(article)
    db.session.commit()
    return jsonify({'success': 'OK'})


@bp.route('/articles', methods=['GET'])
@token_auth.login_required
def post_article():
    args = parser_article.parse_args()
    article = Articles(
        creator=args['creator'],
        title=args['title'],
        heading=args['heading'],
        content=args['content'],
        category=args['category'], )
    db.session.add(article)
    db.session.commit()
    return jsonify({'success': 'OK'})


@bp.route('/articles', methods=['GET'])
@token_auth.login_required
def get_articles():
    article = db.session.query(Articles).all()
    return jsonify(
        {'articles': [item.to_dict(only=('creator', 'title', 'heading', 'content', "category")) for item in
                      article]})

