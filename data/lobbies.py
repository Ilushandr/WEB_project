import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Lobby(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Lobbies'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, unique=True)
    users = sqlalchemy.Column(sqlalchemy.String, nullable=True)