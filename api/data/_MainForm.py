from flask_wtf import FlaskForm
from wtforms import SubmitField


class MainForm(FlaskForm):
    map_redirect = SubmitField('Перейти к картам')
    comment_redirect = SubmitField('Оставить коментарий')