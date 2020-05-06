from flask_restful import reqparse


# Парсер для API
parser_article = reqparse.RequestParser()
parser_article.add_argument('creator', required=True, type=int)
parser_article.add_argument('title', required=True)
parser_article.add_argument('heading', required=True)
parser_article.add_argument('content', required=True)
parser_article.add_argument('category', required=True, type=int)
parser_article.add_argument('article_id', required=True, type=int)
