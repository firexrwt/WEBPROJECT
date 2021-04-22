from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class RatingForm(FlaskForm):
    rating = IntegerField('Ваша оценка от 1 до 10', validators=DataRequired)
    short_comment = StringField('Ваш комментарий')
    about = TextAreaField()
    submit = SubmitField('Оставить комментарий')