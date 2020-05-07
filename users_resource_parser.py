from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('nickname', required=True)
parser.add_argument('email', required=True)
parser.add_argument('hashed_password', required=True)
parser.add_argument('access_level', required=True, type=int)
parser.add_argument('photo_url', required=False)
parser.add_argument('id', required=False, type=int)