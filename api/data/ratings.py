import datetime
import sqlalchemy as sql
from .db_session import SqlAlchemyBase


class Rating(SqlAlchemyBase):
    id = sql.Column(sql.Integer, autoincrement=True, primary_key=True)

    comment_top = sql.Column(sql.String, nullable=True)
    comment_bottom = sql.Column(sql.String, nullable=True)
    rating = sql.Column(sql.Integer, nullable=False)
    post_date = sql.Column(sql.DateTime, default=datetime.datetime)
