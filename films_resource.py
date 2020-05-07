from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.films import Films
from films_resource_parser import parser
from security.const import TOKEN


def abort_if_films_not_found(films_id):
    session = db_session.create_session()
    films = session.query(Films).get(films_id)
    if not films:
        abort(404, message=f"Films {films_id} not found")


def abort_if_token_not_match(token):
    if TOKEN != token:
        abort(404, message=f"Token does not match")


def errors_if_wrong_data(args):
    genres = [
        'вестерн', 'биография', 'боевик', 'военный', 'детектив', 'драма', 'документальный',
        'история', 'комедия', 'криминал', 'мелодрама', 'музыка', 'мультфильм', 'приключения',
        'семейный', 'спорт', 'триллер', 'ужасы', 'фэнтези', 'фантастика'
    ]
    message = ""
    splitted = str.split(args['genre'], ", ")
    for tag in splitted:
        if tag not in genres:
            message = "Не правильно написаны жанры. Жанры вводит в нижнем регистре. Пример: жанр, жанр, жанр"
    return message


class FilmsResource(Resource):
    def get(self, token, films_id):
        abort_if_token_not_match(token)
        abort_if_films_not_found(films_id)
        session = db_session.create_session()
        films = session.query(Films).get(films_id)
        return jsonify({'films': films.to_dict(
            only=('id', 'title', 'year', 'country', 'genre',
                  'age', 'description', 'show', 'film_url', 'photo_url', 'score'))})

    def delete(self, token, films_id):
        abort_if_token_not_match(token)
        abort_if_films_not_found(films_id)
        session = db_session.create_session()
        session.query(Films).filter(Films.id == films_id).delete()
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, token, films_id):
        abort_if_token_not_match(token)
        abort_if_films_not_found(films_id)
        args = parser.parse_args()
        if errors_if_wrong_data(args) != "":
            return jsonify({"errors": errors_if_wrong_data(args)})
        session = db_session.create_session()
        films = session.query(Films).get(films_id)
        films.title = args['title']
        films.year = args['year']
        films.country = args['country']
        films.genre = args['genre']
        films.age = args['age']
        films.description = args['description']
        films.show = args['show']
        films.film_url = args['film_url']
        films.photo_url = args['photo_url']
        films.score = args['score']
        session.commit()
        return jsonify({'success': 'OK'})


class FilmsListResource(Resource):
    def get(self, token):
        abort_if_token_not_match(token)
        session = db_session.create_session()
        films = session.query(Films).all()
        return jsonify({'films': [item.to_dict(
            only=('id', 'title', 'year', 'country', 'genre',
                  'age', 'description', 'show', 'film_url', 'photo_url', 'score', 'duration')) for item in films]})

    def post(self, token):
        abort_if_token_not_match(token)
        args = parser.parse_args()
        if errors_if_wrong_data(args) != "":
            return jsonify({"errors": errors_if_wrong_data(args)})
        session = db_session.create_session()
        films = Films(
            title=args['title'],
            year=args['year'],
            country=args['country'],
            genre=args['genre'],
            age=args['age'],
            description=args['description'],
            show=args['show'],
            film_url=args['film_url'],
            photo_url=args['photo_url'],
            score=args['score']
        )
        session.add(films)
        session.commit()
        return jsonify({'success': 'OK'})
