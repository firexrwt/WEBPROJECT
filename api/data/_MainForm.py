from flask_wtf import FlaskForm
from wtforms import SubmitField


class MainForm(FlaskForm):
    map_redirect = SubmitField(label='Перейти к картам')
    comment_redirect = SubmitField(label='Оставить коментарий')