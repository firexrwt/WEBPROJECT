from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class RatingForm(FlaskForm):
    rating = SelectField(label='Ваша оценка от 1 до 5', choices=[(i, f'{i}') for i in range(1, 6)], default=(5, '5'))
    short_comment = StringField('Ваш комментарий', validators=[DataRequired()])
    about = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Оставить комментарий')