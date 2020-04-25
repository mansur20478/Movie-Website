from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('year', required=True, type=int)
parser.add_argument('country', required=True)
parser.add_argument('genre', required=True)
parser.add_argument('age', required=True)
parser.add_argument('description', required=True)
parser.add_argument('show', required=True, type=bool)
parser.add_argument('film_url', required=True)
parser.add_argument('photo_url', required=True)
parser.add_argument('score', required=True, type=int)
