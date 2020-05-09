from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.comment import Comments
from comments_resource_parser import parser
from security.const import TOKEN


def abort_if_comment_not_found(comment_id):
    session = db_session.create_session()
    comments = session.query(Comments).get(comment_id)
    if not comments:
        abort(404, message=f"Comment {comment_id} not found")


def abort_if_token_not_match(token):
    if TOKEN != token:
        abort(404, message=f"Token does not match")


class CommentsResource(Resource):
    def get(self, token, comment_id):
        abort_if_token_not_match(token)
        abort_if_comment_not_found(comment_id)
        session = db_session.create_session()
        comment = session.query(Comments).get(comment_id)
        return jsonify({'comments': comment.to_dict(
            only=('id', 'user_id', 'film_id', 'text', 'modified_date'))})

    def delete(self, token, comment_id):
        abort_if_token_not_match(token)
        abort_if_comment_not_found(comment_id)
        session = db_session.create_session()
        session.query(Comments).filter(Comments.id == comment_id).delete()
        session.commit()
        return jsonify({'success': 'OK'})


class CommentsListResource(Resource):
    def get(self, token):
        abort_if_token_not_match(token)
        session = db_session.create_session()
        comments = session.query(Comments).all()
        return jsonify({'comments': [item.to_dict(
            only=('id', 'user_id', 'film_id', 'text', 'modified_date')) for item in comments]})

    def post(self, token):
        abort_if_token_not_match(token)
        args = parser.parse_args()
        session = db_session.create_session()
        comment = Comments(
            text=args['text'],
            user_id=args['user_id'],
            film_id=args['film_id']
        )
        session.add(comment)
        session.commit()
        return jsonify({'success': 'OK'})
