import sys
from io import BytesIO
import requests
from PIL import Image


def get_size_parms(json_response, address_ll):
    org_point = address_ll
    print("Введите размеры [1] Например 0.008 -- >")
    delta1 = input()
    print("Введите размеры [2] Например 0.008 -- >")
    delta2 = input()
    map_params = {
        "ll": address_ll,
        "spn": ",".join([delta1, delta2]),
        "l": "map",
        "pt": "{},pm2dgl".format(org_point)
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    return response


toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]

toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

address_ll = ",".join([toponym_longitude, toponym_lattitude])
response = get_size_parms(json_response, address_ll)

Image.open(BytesIO(
    response.content)).show()
