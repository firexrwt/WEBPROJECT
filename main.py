import os
from flask import Flask, render_template, Request, redirect, url_for
from api.data import _MainForm, _MapForms, _RatingsForm
from MapCompiler import Compile_Map

app = Flask(__name__)
sec_key = os.urandom(32)
app.config['SECRET_KEY'] = sec_key


@app.route('/', methods=['POST', 'GET'])
def main_page():
    form = _MainForm.MainForm()
    r_url = url_for('main_page')
    if form.validate_on_submit():
        if form.map_redirect.data:
            r_url = url_for('map_compiler')
        elif form.comment_redirect.data:
            r_url = url_for('review')
        return redirect('/review')
    return render_template('mainpage.html', title='Главная страница', form=form, redirect_url=r_url)


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
    return render_template('review.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')