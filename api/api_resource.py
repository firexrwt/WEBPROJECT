from flask import jsonify
from flask_restful import  abort, reqparse, Resource
from .data import db_session, ratings


def abort_if_empty(com_id):
    db_sess = db_session.create_session()
    comment = db_sess.query(ratings.Rating).get(com_id)
    if not comment:
        abort(404, message='Комменатарий не найден')


parser = reqparse.RequestParser()
parser.add_argument('comment_top')
parser.add_argument('comment_bottom')
parser.add_argument('rating')


class RateResource(Resource):
    def get(self, rate_id):
        abort_if_empty(rate_id)
        sess = db_session.create_session()
        rate = sess.query(ratings.Rating).get(rate_id)
        return jsonify({'ratings': rate.to_dict(
            only=('comment_top', 'comment_bottom', 'rating', 'post_date'))})

    def delete(self, rate_id):
        abort_if_empty(rate_id)
        sess = db_session.create_session()
        rate = sess.query(ratings.Rating).get(rate_id)
        sess.delete(rate)
        sess.commit()
        return jsonify({'OK': 'Successful'})


class RateListResource(Resource):
    def get(self):
        sess = db_session.create_session()
        rating_list = sess.query(ratings.Rating).all()
        return jsonify({'ratings': [item.to_dict(
            only=('comment_top', 'comment_bottom', 'rating', 'post_date')) for item in rating_list]})

    def post(self):
        args = parser.parse_args()
        sess = db_session.create_session()

        rate = ratings.Rating(
            comment_top=args['comment_top'],
            comment_bottom=args['comment_bottom'],
            rating=args['rating']
        )
        sess.add(rate)
        sess.commit()
        return jsonify({'OK': 'Successful'})