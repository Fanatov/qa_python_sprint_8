import allure
import pytest
import requests
import DATA
import yandex_precode


@allure.description('тест ручки "Создание курьера" ')
class TestCourierCreation:
    @allure.title('Создание курьера. успешно')
    def test_courier_creation(self, payload):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_CREATION}', data=payload.RANDOM_PAYLOAD)
        assert response.json() == DATA.Results.OK_TRUE

    @allure.title('Создание курьера. Возвращает верный статус-код ')
    def test_courier_creation_returns_correct_status_code(self, payload):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_CREATION}', data=payload.RANDOM_PAYLOAD)
        assert response.status_code == DATA.Codes.OK

    @allure.title('Создание курьера. Нельзя создать двух одинаковых курьеров')
    def test_unable_create_same_courier(self, static_payloads):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_CREATION}', data=static_payloads)
        assert response.json() == DATA.Results.CONFLICT_ALREADY_EXIST

    @allure.title('Создание курьера. Нельзя создать двух одинаковых курьеров. Возвращает верный статус-код')
    def test_unable_create_same_courier_returns_correct_status_code(self, static_payloads):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_CREATION}', data=static_payloads)
        assert response.status_code == DATA.Codes.CONFLICT

    @allure.title('Создание курьера. Нельзя создать курьера без обязательного поля в теле запроса.')
    def test_unable_create_courier_not_enough_data(self):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_CREATION}',
                                 data=DATA.Payloads.HALF_PAYLOAD_MISSING_LOGIN)
        assert response.json() == DATA.Results.BAD_REQUEST_NOT_ENOUGH_DATA

    @allure.title('Создание курьера. Нельзя создать курьера без логина. Возвращает верный статус-код')
    def test_unable_create_courier_not_enough_data_returns_correct_status_code(self):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_CREATION}',
                                 data=DATA.Payloads.HALF_PAYLOAD_MISSING_LOGIN)
        assert response.status_code == DATA.Codes.BAD_REQUEST


@allure.description('тест ручки "Логин курьера" ')
class TestCourierLogin:
    @allure.title('Логин курьера. Успешный логин курьера. Возвращает верный статус-код')
    def test_courier_authorization_returns_correct_status_code(self, static_payloads):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}', data=static_payloads)
        assert response.status_code == DATA.Codes.SUCCESS

    @allure.title('Логин курьера. Успешный логин курьера.')
    def test_courier_success_authorize(self, static_payloads):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}', data=static_payloads)
        assert DATA.Results.LOGIN_SUCCESS in response.json()

    @allure.title('Логин курьера. Попытка логина без обязательного поля')
    @pytest.mark.parametrize('payloading',
                             [DATA.Payloads.HALF_PAYLOAD_MISSING_LOGIN, DATA.Payloads.HALF_PAYLOAD_MISSING_PASSWORD])
    def test_courier_empty_main_login_field_authorization(self, payloading):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}', data=payloading)
        assert response.json() == DATA.Results.LOGIN_HALF_EMPTY

    @allure.title('Логин курьера. Попытка логина без обязательного поля. Возвращает верный статус-код.')
    @pytest.mark.parametrize('payloading',
                             [DATA.Payloads.HALF_PAYLOAD_MISSING_LOGIN, DATA.Payloads.HALF_PAYLOAD_MISSING_PASSWORD])
    def test_courier_empty_main_login_field_authorization_returns_correct_status_code(self, payloading):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}', data=payloading)
        assert response.status_code == DATA.Codes.BAD_REQUEST

    @allure.title('Логин курьера. Попытка логина несуществующего курьера.')
    def test_courier_not_existing_login(self, payload):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}', data=payload.RANDOM_PAYLOAD)
        assert response.json() == DATA.Results.LOGIN_NOT_EXIST

    @allure.title('Логин курьера. Попытка логина несуществующего курьера. Возвращает верный статус-код')
    def test_courier_not_existing_login_returns_correct_status_code(self, payload):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}', data=payload.RANDOM_PAYLOAD)
        assert response.status_code == DATA.Codes.NOT_FOUND


@allure.description('тест ручки "Создание заказа" ')
class TestOrderCreation:
    @allure.title('Создание заказа. Можно создать заказ с разным набором цветов')
    @pytest.mark.parametrize('color', DATA.Colors.COLORS)
    def test_order_creation_success_with_dif_colors(self, color):
        DATA.Payloads.ORDER_CREATION_PAYLOAD['color'] = color
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}',
                                 data=DATA.Payloads.ORDER_CREATION_PAYLOAD)
        assert DATA.Results.ORDER_SUCCESS in response.json()

    @allure.title('Создание заказа. Можно создать заказ с разным набором цветов. Возвращает верный статус-код')
    @pytest.mark.parametrize('color', DATA.Colors.COLORS)
    def test_order_creation_success_with_dif_colors_returns_correct_status_code(self, color):
        DATA.Payloads.ORDER_CREATION_PAYLOAD['color'] = color
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}',
                                 data=DATA.Payloads.ORDER_CREATION_PAYLOAD)
        assert response.status_code == DATA.Codes.OK


@allure.description('тест ручки "Список заказов" ')
class TestOrderList:
    @allure.title('Список заказов. При запросе несуществующего заказа возвращает корректный статус-код')
    def test_order_list_non_existing_id_returns_correct_status_code(self):
        response = requests.get(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.COURIER_ID_PATH}{DATA.Id.id_zero}')
        assert response.status_code == DATA.Codes.NOT_FOUND

    @allure.title('Список заказов. При запросе несуществующего заказа возвращает сообщение об ошибке')
    def test_order_list_non_existing_id_returns_correct_message(self):
        response = requests.get(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.COURIER_ID_PATH}{DATA.Id.id_zero}')
        assert DATA.Results.COURIER_NOT_FOUND == response.json()

    @allure.title('Список заказов. При запросе существующего списка заказов возвращает тело заказа')
    def test_get_order_list_returns_list_of_orders(self, static_payloads):
        created_courier = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}',
                                        data=static_payloads)
        courier_id = created_courier.json()['id']
        response = requests.get(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.COURIER_ID_PATH}{courier_id}')
        assert DATA.Results.ORDER_FIELD in response.json()
        requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{courier_id}')

@allure.description('тест ручки "Удалить курьера"')
class TestDeleteCourier:
    @allure.title('Удалить курьера. Удаление несуществующего курьера возвращает сообщение об ошибке')
    def test_try_delete_non_existing_courier(self):
        response = requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{DATA.Id.id_zero}')
        assert response.json() == DATA.Results.DELETING_COURIER_NOT_FOUND

    @allure.title('Удалить курьера. Удаление несуществующего курьера возвращает корректный статус-код')
    def test_try_delete_non_existing_courier_returns_correct_status_code(self):
        response = requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{DATA.Id.id_zero}')
        assert response.status_code == DATA.Codes.NOT_FOUND

    @allure.title('Удалить курьера. Удаление существующего курьера возвращает сообщение об успешном выполнении запроса')
    def test_try_delete_existing_courier(self, static_payloads):
        created_courier = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}',
                                        data=static_payloads)
        response = requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{created_courier.json()["id"]}')
        assert response.json() == DATA.Results.OK_TRUE
        requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{created_courier.json()["id"]}')

    @allure.title('Удалить курьера. Удаление существующего курьера возвращает корректный статус-код')
    def test_try_delete_existing_courier_returns_correct_status_code(self, static_payloads):
        created_courier = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}',
                                        data=static_payloads)
        response = requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{created_courier.json()["id"]}')
        assert response.status_code == DATA.Codes.SUCCESS
        requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{created_courier.json()["id"]}')

    @allure.title('Удалить курьера. Удаление курьера без необходимого параметра в теле запроса возвращает корректное сообщение об ошибке')
    def test_try_delete_empty_id(self):  # Ошибка АПИ Яндекса. Обратитесь к куратору Исканов Камил.
        response = requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}')
        assert response.json() == DATA.Results.DELETING_COURIER_EMPTY_ID

    @allure.title('Удалить курьера. Удаление курьера без необходимого параметра в теле запроса возвращает корректный статус-код')
    def test_try_delete_empty_id_returns_correct_status_code(self):
        response = requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}')
        assert response.status_code == DATA.Codes.NOT_FOUND

@allure.description('тест ручки "Принять заказ"')
class TestAcceptOrder:
    @allure.title('Принять заказ. Корректный запрос возвращает сообщение об успешном выполнении запроса')
    def test_try_accept_order(self, static_payloads):
        created_courier = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}',
                                        data=static_payloads)
        created_order = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}',
                                      data=DATA.Payloads.ORDER_CREATION_PAYLOAD)
        track_id = created_order.json()['track']
        courier_id = created_courier.json()['id']
        get_track_info = requests.get(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}{track_id}')
        order_id = get_track_info.json()['order']['id']
        response = requests.put(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.ACCEPT_ORDER}{order_id}{DATA.Api.COURIER_ID_PATH}{courier_id}')
        assert response.json() == DATA.Results.OK_TRUE
        requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{courier_id}')

    @allure.title('Принять заказ. Попытка принять заказ без id курьера возвращает корректное сообщение об ошибке')
    def test_try_accept_order_without_courier_id(self):
        created_order = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}',
                                      data=DATA.Payloads.ORDER_CREATION_PAYLOAD)
        track_id = created_order.json()['track']
        get_track_info = requests.get(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}{track_id}')
        order_id = get_track_info.json()['order']['id']
        response = requests.put(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.ACCEPT_ORDER}{order_id}{DATA.Api.COURIER_ID_PATH}')
        assert response.json() == DATA.Results.ACCEPT_ORDER_NOT_ENOUGH_DATA

    @allure.title('Принять заказ. Попытка принять заказ без id курьера возвращает корректный статус-код')
    def test_try_accept_order_without_courier_id_returns_correct_status_code(self):
        created_order = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}',
                                      data=DATA.Payloads.ORDER_CREATION_PAYLOAD)
        track_id = created_order.json()['track']
        get_track_info = requests.get(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}{track_id}')
        order_id = get_track_info.json()['order']['id']
        response = requests.put(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.ACCEPT_ORDER}{order_id}{DATA.Api.COURIER_ID_PATH}')
        assert response.status_code == DATA.Codes.BAD_REQUEST

    @allure.title('Принять заказ. Попытка принять заказ без id заказа возвращает корректное сообщение об ошибке')
    def test_try_accept_order_without_order_id(self,
                                               static_payloads):  # Ошибка АПИ Яндекса. Обратитесь к куратору Исканов Камил.
        created_courier = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}',
                                        data=static_payloads)
        courier_id = created_courier.json()['id']
        response = requests.put(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.ACCEPT_ORDER}{DATA.Api.COURIER_ID_PATH}{courier_id}')
        print(response.json())
        assert response.json() == DATA.Results.ACCEPT_ORDER_NOT_ENOUGH_DATA
        requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{courier_id}')

    @allure.title('Принять заказ. Попытка принять заказ без id заказа возвращает корректный статус-код')
    def test_try_accept_order_without_order_id_returns_correct_status_code(self,
                                                                           static_payloads):  # Ошибка АПИ Яндекса. Обратитесь к куратору Исканов Камил.
        created_courier = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}',
                                        data=static_payloads)
        courier_id = created_courier.json()['id']
        response = requests.put(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.ACCEPT_ORDER}{DATA.Api.COURIER_ID_PATH}{courier_id}')
        print(response.json())
        assert response.status_code == DATA.Codes.BAD_REQUEST
        requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{courier_id}')

    @allure.title('Принять заказ. Попытка принять заказ с некорректным id курьера возвращает корректное сообщение об ошибке')
    def test_try_accept_order_with_non_existing_courier_id(self):
        created_order = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}',
                                      data=DATA.Payloads.ORDER_CREATION_PAYLOAD)
        track_id = created_order.json()['track']
        get_track_info = requests.get(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}{track_id}')
        order_id = get_track_info.json()['order']['id']
        response = requests.put(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.ACCEPT_ORDER}{order_id}{DATA.Api.COURIER_ID_PATH}{DATA.Id.id_zero}')
        assert response.json() == DATA.Results.ACCEPT_ORDER_COURIER_NOT_EXIST

    @allure.title('Принять заказ. Попытка принять заказ с некорректным id курьера возвращает корректный статус-код')
    def test_try_accept_order_with_non_existing_courier_id_returns_correct_status_code(self):
        created_order = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}',
                                      data=DATA.Payloads.ORDER_CREATION_PAYLOAD)
        track_id = created_order.json()['track']
        get_track_info = requests.get(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}{track_id}')
        order_id = get_track_info.json()['order']['id']
        response = requests.put(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.ACCEPT_ORDER}{order_id}{DATA.Api.COURIER_ID_PATH}{DATA.Id.id_zero}')
        assert response.status_code == DATA.Codes.NOT_FOUND

    @allure.title('Принять заказ. Попытка принять заказ с некорректным id заказа возвращает корректное сообщение об ошибке')
    def test_try_accept_order_non_existing_order(self, static_payloads):
        created_courier = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}',
                                        data=static_payloads)
        courier_id = created_courier.json()['id']
        response = requests.put(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.ACCEPT_ORDER}{DATA.Id.id_zero}{DATA.Api.COURIER_ID_PATH}{courier_id}')
        assert response.json() == DATA.Results.ACCEPT_ORDER_ORDER_NOT_EXIST
        requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{courier_id}')

    @allure.title('Принять заказ. Попытка принять заказ с несуществующим id заказа возвращает корректное сообщение об ошибке')
    def test_try_accept_order_non_existing_order_returns_correct_status_code(self, static_payloads):
        created_courier = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}',
                                        data=static_payloads)
        courier_id = created_courier.json()['id']
        response = requests.put(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.ACCEPT_ORDER}{DATA.Id.id_zero}{DATA.Api.COURIER_ID_PATH}{courier_id}')
        assert response.status_code == DATA.Codes.NOT_FOUND
        requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{courier_id}')

@allure.description('тест ручки "Получить заказ по его номеру"')
class TestGetOrderByNumber:
    @allure.title('Получить заказ по его номеру. Получить заказ по несуществующему номеру заказа возвращает корректное сообщение об ошибке.')
    def test_get_order_with_not_existing_order_returns_error(self):
        response = requests.get(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}{DATA.Id.id_zero}')
        assert response.json() == DATA.Results.GET_ORDER_BY_ITS_NUMBER_NOT_FOUND

    @allure.title('Получить заказ по его номеру. Получить заказ по несуществующему номеру заказа возвращает корректный статус-код.')
    def test_get_order_with_not_existing_order_returns_correct_status_code(self):
        response = requests.get(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}{DATA.Id.id_zero}')
        assert response.status_code == DATA.Codes.NOT_FOUND

    @allure.title('Получить заказ по его номеру. Попытка получить заказ по номеру без номера возвращает корректное сообщение об ошибке')
    def test_get_order_without_order_number_returns_error(self):
        response = requests.get(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}')
        assert response.json() == DATA.Results.GET_ORDER_WITHOUT_NUMBER

    @allure.title('Получить заказ по его номеру. Попытка получить заказ по номеру без номера возвращает корректный статус-код')
    def test_get_order_without_order_number_returns_correct_status_code(self):
        response = requests.get(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}')
        assert response.status_code == DATA.Codes.BAD_REQUEST

    @allure.title('Получить заказ по его номеру. Успешный запрос возвращает объект с заказом')
    def test_get_order_with_correct_number_returns_correct_response(self):
        created_order = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}',
                                      data=DATA.Payloads.ORDER_CREATION_PAYLOAD)
        track_id = created_order.json()['track']
        response = requests.get(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}{track_id}')
        assert response.status_code == DATA.Codes.SUCCESS


