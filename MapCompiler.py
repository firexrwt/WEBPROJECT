import requests


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