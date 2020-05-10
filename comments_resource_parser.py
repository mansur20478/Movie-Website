from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('film_id', required=True, type=int)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('text', required=True)
