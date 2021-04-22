import flask
from flask_restful import Api, abort, reqparse, Resource
from .data import db_session, ratings


app = flask.Flask(__name__)
api = Api(app)


def abort_if_empty(com_id):
    db_sess = db_session.create_session()
    comment = db_sess.query(ratings.Rating).get(com_id)
    if not comment:
        abort(404, message='Комменатарий не найден')


parser = reqparse.RequestParser()
parser.add_argument('comment_top')