from flask import Flask
import request

app = Flask(__name__)


@app.route('/')
def main_page():
    return '<HTML>' \
           '<HEAD>' \
           '<p> На этом сайте вы можете увидеть любой город или страну на карте!</p>' \
           '</HEAD>' \
           '<BODY>' \
           '<form action="map_compiler">' \
           '<button>Ссылка на карту</button>' \
           '</BODY>' \
           '</HTML>'


@app.route('/map_compiler')
def map_compiler():
    return '<HTML>' \
           '<HEAD>' \
           '</HEAD>' \
           '<BODY>' \
           '<form name="test" method="post" action="input1.php">' \
           '<p><b>Вводите свой город(или страну!) сюда ↓</b><br>' \
           '<input type="text" size="40">' \
           '</BODY>' \
           '</HTML>' \
 \
 \
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
