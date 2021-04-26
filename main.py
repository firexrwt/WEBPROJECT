import os
import datetime
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, user_logged_in, current_user
from review_db.data import _MainForm, _MapForms, _RatingsForm, _RegisterForm, _LoginForm
from MapCompiler import Compile_Map
from review_db.data import review_session, ratings, users

app = Flask(__name__)
sec_key = os.urandom(32)
app.config['SECRET_KEY'] = sec_key
log_manager = LoginManager()
log_manager.init_app(app)


@app.route('/', methods=['POST', 'GET'])
@app.route('/main_page', methods=['POST', 'GET'])
def main_page():
    form = _MainForm.MainForm()
    session = review_session.create_session()
    rate_list = list(map(lambda x: int(str(x)[1]), session.query(ratings.Rating.rating).all()))

    if rate_list:
        median = sum(rate_list) / len(rate_list)
    else:
        median = 0
    if form.validate_on_submit():
        if form.map_redirect.data:
            return redirect(url_for("map_compiler"))
        if form.comment_redirect.data:
            if current_user.is_authenticated:
                return redirect(url_for("review"))
            return redirect(url_for('login'))
    return render_template('mainpage.html', title='Главная страница',
                           form=form, median=median)


@app.route('/map_compiler', methods=['POST', 'GET'])
def map_compiler():
    form = _MapForms.MapForm()
    country_name = form.country.data
    session = review_session.create_session()
    img_src = None
    message = ''
    flag = False
    comms = session.query(ratings.Rating).all()
    if form.return_to_main.data:
        return redirect(url_for('main_page'))
    if country_name:
        compile = Compile_Map(country_name)
        if compile['Status'] == 'OK':
            flag = form.submit.data
            img_src = os.path.relpath(os.path.abspath(f'static/img/{country_name}.png'),
                                      os.path.abspath('templates/map_compiler.html'))
        else:
            message = 'Пожалуйста введите локацию повторно'
    return render_template('map_compiler.html', form=form, title='Поиск страны', flag=flag, img_src=img_src,
                           comments=comms, message=message)


@app.route('/review', methods=['POST', 'GET'])
def review():
        form = _RatingsForm.RatingForm()
        if form.submit.data:
            session = review_session.create_session()
            comment = ratings.Rating(
                comment_top=form.short_comment.data,
                comment_bottom=form.about.data,
                rating=int(form.rating.data),
                post_date=datetime.datetime.now(),
                user=session.query(users.User).filter(users.User.nickname == current_user.nickname).first()
            )
            session.add(comment)
            session.commit()
            return redirect(url_for('main_page'))
        return render_template('review.html', form=form, title='Оставьте комментарий')


@log_manager.user_loader
def load_user(user_id):
    db_sess = review_session.create_session()
    return db_sess.query(users.User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = _RegisterForm.RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = review_session.create_session()
        if db_sess.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if db_sess.query(users.User).filter(users.User.nickname == form.nickname.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Этот ник занят")
        user = users.User(
            name=form.name.data,
            nickname=form.nickname.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = _LoginForm.LoginForm()
    if form.validate_on_submit():
        db_sess = review_session.create_session()
        user = db_sess.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    review_session.global_init('review_db/db/db_file.sqlite')
    app.run(port=8080, host='127.0.0.1')
