import json

from flask import Flask, request
import requests

app = Flask(__name__)


def Compile_Map(name):
    apikey = '40d1649f-0493-4b70-98ba-98533de7710b'

    req = f'http://geocode-maps.yandex.ru/1.x/?apikey={apikey}&geocode={name}&format=json'
    coord_find = requests.get(req)
    if coord_find:
        jsonresp = coord_find.json()
        jr = jsonresp['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        coords = jr['Point']['pos']
        delta_ld = list(map(float, jr['boundedBy']['Envelope']['lowerCorner'].split()))
        delta_ur = list(map(float, jr['boundedBy']['Envelope']['upperCorner'].split()))
        area = abs(delta_ld[0] - delta_ur[0]) * abs(delta_ur[1] - delta_ld[1])
        c = coords.split()
        print(' '.join(map(str, c)))

    req2 = f'https://static-maps.yandex.ru/1.x/?ll={c[0]},{c[1]}&spn={area ** 0.5},{area ** 0.5}&l=map'
    return requests.get(req2)


@app.route('\post', methods=['POST'])
def get_alice_request():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Привет, какую страну или город ты хочешь увидеть на карте?'
        session_state['user_id'] = {
            'state': 1
        }
        return
    states[session_state[user_id]['state']](user_id, req, res)


states = {
    1: Compile_Map
}
session_state = {}

if __name__ == '__main__':
    app.run()
