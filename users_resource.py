from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.users import Users
from users_resource_parser import parser
from security.const import TOKEN


def abort_if_users_not_found(users_id):
    session = db_session.create_session()
    users = session.query(Users).get(users_id)
    if not users:
        abort(404, message=f"Users {users_id} not found")


def abort_if_token_not_match(token):
    if TOKEN != token:
        abort(404, message=f"Token does not match")


def errors_if_wrong_data(arg, users_id=0):
    message = ""
    session = db_session.create_session()
    users = session.query(Users).filter(Users.email == arg['email'], Users.id != users_id)
    if users:
        message = "Данная почта занята\n"
    users = session.query(Users).filter(Users.nickname == arg['nickname'], Users.id != users_id)
    if users:
        message += "Данный логин занят"
    return message


class UsersResource(Resource):
    def get(self, token, users_id):
        abort_if_token_not_match(token)
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(Users).get(users_id)
        return jsonify({'users': users.to_dict(
            only=('id', 'nickname', 'email', 'hashed_password', 'access_level', 'photo_url'))})

    def delete(self, token, users_id):
        abort_if_token_not_match(token)
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        session.query(Users).filter(Users.id == users_id).delete()
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, token, users_id):
        abort_if_token_not_match(token)
        abort_if_users_not_found(users_id)
        args = parser.parse_args()
        if errors_if_wrong_data(args, users_id) != "":
            return jsonify({"errors": errors_if_wrong_data(args, users_id)})
        session = db_session.create_session()
        users = session.query(Users).get(users_id)
        users.nickname = args['nickname']
        users.email = args['email']
        users.hashed_password = args['hashed_password']
        users.access_level = args['access_level']
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self, token):
        abort_if_token_not_match(token)
        session = db_session.create_session()
        users = session.query(Users).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'nickname', 'email', 'hashed_password', 'access_level', 'photo_url')) for item in users]})

    def post(self, token):
        abort_if_token_not_match(token)
        args = parser.parse_args()
        if errors_if_wrong_data(args) != "":
            return jsonify({"errors": errors_if_wrong_data(args)})
        session = db_session.create_session()
        users = Users(
            nickname=args['nickname'],
            email=args['email'],
            hashed_password=args['hashed_password'],
            access_level=args['access_level']
        )
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})
