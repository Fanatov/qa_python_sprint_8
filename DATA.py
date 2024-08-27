import random
import string

import yandex_precode


class Api:
    COURIER_CREATION = f'api/v1/courier'
    COURIER_LOGIN = f'api/v1/courier/login'
    ORDER_CREATION = f'api/v1/orders'
    DELETE_COURIER = f'api/v1/courier/'
    ACCEPT_ORDER = f'/accept/'
    COURIER_ID_PATH = f'?courierId='
    FIND_ORDER_ID = f'/track?t='


class ApiParams:
    NON_EXISTING_COURIER = f'?courierId=0'


class Url:
    MAIN_URL = f'https://qa-scooter.praktikum-services.ru/'


class Colors:
    COLORS = [["", ""], ["BLACK", ""], ["", "GREY"], ["BLACK", "GREY"]]


class Payloads:
    HALF_PAYLOAD_MISSING_LOGIN = {
        "login": '',
        "password": 'thats_password_exist',
        "firstName": 'thats_the_name'
    }

    HALF_PAYLOAD_MISSING_PASSWORD = {
        "login": 'thats_login_exist',
        "password": '',
        "firstName": 'thats_the_name'
    }

    ORDER_CREATION_PAYLOAD = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha"
    }


class Results:
    OK_TRUE = {'ok': True}
    CONFLICT_ALREADY_EXIST = {'code': 409, 'message': 'Этот логин уже используется. Попробуйте другой.'}
    BAD_REQUEST_NOT_ENOUGH_DATA = {'code': 400, 'message': 'Недостаточно данных для создания учетной записи'}
    LOGIN_SUCCESS = 'id'
    ORDER_FIELD = 'orders'
    ORDER_SUCCESS = 'track'
    LOGIN_HALF_EMPTY = {'code': 400, 'message': 'Недостаточно данных для входа'}
    LOGIN_NOT_EXIST = {'code': 404, 'message': 'Учетная запись не найдена'}
    COURIER_NOT_FOUND = {'code': 404, 'message': 'Курьер с идентификатором 0 не найден'}
    DELETING_COURIER_NOT_FOUND = {'code': 404, 'message': 'Курьера с таким id нет.'}
    DELETING_COURIER_EMPTY_ID = {'code': 404, 'message': 'Недостаточно данных для удаления курьера.'}
    ACCEPT_ORDER_NOT_ENOUGH_DATA = {'code': 400, 'message': 'Недостаточно данных для поиска'}
    ACCEPT_ORDER_COURIER_NOT_EXIST = {'code': 404, 'message': 'Курьера с таким id не существует'}
    ACCEPT_ORDER_ORDER_NOT_EXIST = {'code': 404, 'message': 'Заказа с таким id не существует'}


class Codes:
    SUCCESS = 200
    OK = 201
    CONFLICT = 409
    BAD_REQUEST = 400
    NOT_FOUND = 404


class Id:
    id_zero = 0
