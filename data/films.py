import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Films(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'films'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    photo_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    film_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    score = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    country = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    duration = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    show = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.Integer, default=datetime.datetime.utcnow())