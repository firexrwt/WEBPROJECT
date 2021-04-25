import os
from flask import Flask, render_template, redirect, url_for
from api.data import _MainForm, _MapForms, _RatingsForm
from MapCompiler import Compile_Map
from api import api_resource
from flask_restful import Api
import requests

app = Flask(__name__)
sec_key = os.urandom(32)
app.config['SECRET_KEY'] = sec_key
api = Api(app)

api.add_resource(api_resource.RateResource, '/api/comment/<int:rate_id>')
api.add_resource(api_resource.RateListResource, '/api/comment')


@app.route('/', methods=['POST', 'GET'])
def main_page():
    form = _MainForm.MainForm()
    if form.validate_on_submit():
        if form.map_redirect.data:
            return redirect(url_for("map_compiler"))
        if form.comment_redirect.data:
            return redirect(url_for("review"))
    return render_template('mainpage.html', title='Главная страница', form=form)


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


@app.route('/review')
def review():
    form = _RatingsForm.RatingForm()
    if form.validate_on_submit():
        if form.submit.data:
            requests.post('http://127.0.0.1:8080/api/comment', json={
                'rating': form.rating.data,
                'comment_top': form.short_comment.data,
                'comment_bottom': form.about.data
            })
    print(requests.get('http://127.0.0.1:8080/api/comment').json())
    return render_template('review.html', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')