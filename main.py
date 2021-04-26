import os
import datetime
from flask import Flask, render_template, redirect, url_for
from api.data import _MainForm, _MapForms, _RatingsForm
from MapCompiler import Compile_Map
from api.data import db_session, ratings

app = Flask(__name__)
sec_key = os.urandom(32)
app.config['SECRET_KEY'] = sec_key


@app.route('/', methods=['POST', 'GET'])
def main_page():
    form = _MainForm.MainForm()
    session = db_session.create_session()
    rate_list = list(map(lambda x: int(str(x)[1]),session.query(ratings.Rating.rating).all()))
    comms = session.query(ratings.Rating).all()
    if rate_list:
        median = sum(rate_list) / len(rate_list)
    if form.validate_on_submit():
        if form.map_redirect.data:
            return redirect(url_for("map_compiler"))
        if form.comment_redirect.data:
            return redirect(url_for("review"))
    return render_template('mainpage.html', title='Главная страница',
                           form=form, median=median, comments=comms)


@app.route('/map_compiler', methods=['POST', 'GET'])
def map_compiler():
    form = _MapForms.MapForm()
    country_name = form.country.data
    img_src = None
    flag = False
    if country_name:
        Compile_Map(country_name)
        flag = form.submit.data
        img_src = os.path.relpath(os.path.abspath(f'static/img/{country_name}.png'), \
                                  os.path.abspath('templates/map_compiler.html'))
    return render_template('map_compiler.html', form=form, title='Поиск страны', flag=flag, img_src=img_src)


@app.route('/review', methods=['POST', 'GET'])
def review():
    form = _RatingsForm.RatingForm()
    if form.submit.data:
        session = db_session.create_session()
        comment = ratings.Rating(
            comment_top=form.short_comment.data,
            comment_bottom=form.about.data,
            rating=int(form.rating.data),
            post_date=datetime.datetime.now()
        )
        session.add(comment)
        session.commit()
    return render_template('review.html', form=form)


if __name__ == '__main__':
    db_session.global_init('api/db/db_file.sqlite')
    app.run(port=8080, host='127.0.0.1')
