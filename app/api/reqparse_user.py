from flask_restful import reqparse


# Парсер для API
parser_user = reqparse.RequestParser()
parser_user.add_argument('username', required=True)
parser_user.add_argument('email', required=True)
parser_user.add_argument('position', required=True, type=bool)
parser_user.add_argument('hashed_password', required=True)
parser_user.add_argument('user_id', required=True, type=int)
