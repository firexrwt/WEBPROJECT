import os
from flask import Flask, render_template, redirect, request
from api.data import _MainForm, _MapForms, _RatingsForm
from MapCompiler import Compile_Map

app = Flask(__name__)
sec_key = os.urandom(32)
app.config['SECRET_KEY'] = sec_key


@app.route('/', methods=['POST', 'GET'])
def main_page():
    return render_template('mainpage.html', title='Главная страница')


@app.route('/map_compiler', methods=['POST', 'GET'])
def map_compiler():
    form = _MapForms.MapForm()
    country_name = form.country.data
    if country_name:
        Compile_Map(country_name)
        flag = form.submit.data
        img_src = os.path.abspath('static/img/map.png')
    else:
        flag = False
        img_src = None
    return render_template('map_compiler.html', form=form, title='Поиск страны', flag=flag, img_source=img_src)


@app.route('/review')
def review():
    return render_template('review.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
