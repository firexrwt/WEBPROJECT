from django.forms import IntegerField
from flask import Flask
from flask import render_template
import request
import wtforms
from wtforms.validators import DataRequired

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('mainpage.html')



@app.route('/map_compiler')
def map_compiler():
    return render_template('map_compiler.html')


@app.route('/review')
def review():
    return render_template('review.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
