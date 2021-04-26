import sqlalchemy as sql
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from review_db.data.review_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sql.Column(sql.Integer, autoincrement=True, primary_key=True)

    nickname = sql.Column(sql.String, unique=True, nullable=True)
    email = sql.Column(sql.String, unique=True, index=True, nullable=True)
    name = sql.Column(sql.String, nullable=True)
    hash_password = sql.Column(sql.String, nullable=True)
    comment = orm.relation('Rating', back_populates='user')

    def set_password(self, password):
        self.hash_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash_password, password)