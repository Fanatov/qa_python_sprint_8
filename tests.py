import allure
import pytest
import requests
import DATA
import yandex_precode


class TestCourierCreation:
    def test_courier_creation(self, payload):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_CREATION}', data=payload.RANDOM_PAYLOAD)
        assert response.json() == DATA.Results.OK_TRUE

    def test_courier_creation_returns_correct_status_code(self, payload):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_CREATION}', data=payload.RANDOM_PAYLOAD)
        assert response.status_code == DATA.Codes.OK

    def test_unable_create_same_courier(self, static_payloads):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_CREATION}', data=static_payloads)
        assert response.json() == DATA.Results.CONFLICT_ALREADY_EXIST

    def test_unable_create_same_courier_returns_correct_status_code(self, static_payloads):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_CREATION}', data=static_payloads)
        assert response.status_code == DATA.Codes.CONFLICT

    def test_unable_create_courier_not_enough_data(self):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_CREATION}',
                                 data=DATA.Payloads.HALF_PAYLOAD_MISSING_LOGIN)
        assert response.json() == DATA.Results.BAD_REQUEST_NOT_ENOUGH_DATA

    def test_unable_create_courier_not_enough_data_returns_correct_status_code(self):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_CREATION}',
                                 data=DATA.Payloads.HALF_PAYLOAD_MISSING_LOGIN)
        assert response.status_code == DATA.Codes.BAD_REQUEST


class TestCourierLogin:
    def test_courier_authorization_returns_correct_status_code(self, static_payloads):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}', data=static_payloads)
        assert response.status_code == DATA.Codes.SUCCESS

    def test_courier_success_authorize(self, static_payloads):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}', data=static_payloads)
        assert DATA.Results.LOGIN_SUCCESS in response.json()

    @pytest.mark.parametrize('payloading',
                             [DATA.Payloads.HALF_PAYLOAD_MISSING_LOGIN, DATA.Payloads.HALF_PAYLOAD_MISSING_PASSWORD])
    def test_courier_empty_main_login_field_authorization(self, payloading):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}', data=payloading)
        assert response.json() == DATA.Results.LOGIN_HALF_EMPTY

    @pytest.mark.parametrize('payloading',
                             [DATA.Payloads.HALF_PAYLOAD_MISSING_LOGIN, DATA.Payloads.HALF_PAYLOAD_MISSING_PASSWORD])
    def test_courier_empty_main_login_field_authorization_returns_correct_status_code(self, payloading):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}', data=payloading)
        assert response.status_code == DATA.Codes.BAD_REQUEST

    def test_courier_not_existing_login(self, payload):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}', data=payload.RANDOM_PAYLOAD)
        assert response.json() == DATA.Results.LOGIN_NOT_EXIST

    def test_courier_not_existing_login_returns_correct_status_code(self, payload):
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}', data=payload.RANDOM_PAYLOAD)
        assert response.status_code == DATA.Codes.NOT_FOUND


class TestOrderCreation:
    @pytest.mark.parametrize('color', DATA.Colors.COLORS)
    def test_order_creation_success_with_dif_colors(self, color):
        DATA.Payloads.ORDER_CREATION_PAYLOAD['color'] = color
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}',
                                 data=DATA.Payloads.ORDER_CREATION_PAYLOAD)
        assert DATA.Results.ORDER_SUCCESS in response.json()

    @pytest.mark.parametrize('color', DATA.Colors.COLORS)
    def test_order_creation_success_with_dif_colors_returns_correct_status_code(self, color):
        DATA.Payloads.ORDER_CREATION_PAYLOAD['color'] = color
        response = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}',
                                 data=DATA.Payloads.ORDER_CREATION_PAYLOAD)
        assert response.status_code == DATA.Codes.OK


class TestOrderList:
    def test_order_list_non_existing_id_returns_correct_status_code(self):
        response = requests.get(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.COURIER_ID_PATH}{DATA.Id.id_zero}')
        assert response.status_code == DATA.Codes.NOT_FOUND

    def test_order_list_non_existing_id_returns_correct_message(self):
        response = requests.get(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.COURIER_ID_PATH}{DATA.Id.id_zero}')
        assert DATA.Results.COURIER_NOT_FOUND == response.json()

    def test_get_order_list_returns_list_of_orders(self, static_payloads):
        created_courier = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}',
                                        data=static_payloads)
        courier_id = created_courier.json()['id']
        response = requests.get(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.COURIER_ID_PATH}{courier_id}')
        assert DATA.Results.ORDER_FIELD in response.json()
        requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{courier_id}')


class TestDeleteCourier:
    def test_try_delete_non_existing_courier(self):
        response = requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{DATA.Id.id_zero}')
        assert response.json() == DATA.Results.DELETING_COURIER_NOT_FOUND

    def test_try_delete_non_existing_courier_returns_correct_status_code(self):
        response = requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{DATA.Id.id_zero}')
        assert response.status_code == DATA.Codes.NOT_FOUND

    def test_try_delete_existing_courier(self, static_payloads):
        created_courier = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}',
                                        data=static_payloads)
        response = requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{created_courier.json()["id"]}')
        assert response.json() == DATA.Results.OK_TRUE
        requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{created_courier.json()["id"]}')

    def test_try_delete_existing_courier_returns_correct_status_code(self, static_payloads):
        created_courier = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}',
                                        data=static_payloads)
        response = requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{created_courier.json()["id"]}')
        assert response.status_code == DATA.Codes.SUCCESS
        requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{created_courier.json()["id"]}')


    def test_try_delete_empty_id(self):  # Ошибка АПИ Яндекса. Обратитесь к куратору Исканов Камил.
        response = requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}')
        assert response.json() == DATA.Results.DELETING_COURIER_EMPTY_ID

    def test_try_delete_empty_id_returns_correct_status_code(self):
        response = requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}')
        assert response.status_code == DATA.Codes.NOT_FOUND


class TestAcceptOrder:
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

    def test_try_accept_order_without_courier_id(self):
        created_order = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}',
                                      data=DATA.Payloads.ORDER_CREATION_PAYLOAD)
        track_id = created_order.json()['track']
        get_track_info = requests.get(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}{track_id}')
        order_id = get_track_info.json()['order']['id']
        response = requests.put(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.ACCEPT_ORDER}{order_id}{DATA.Api.COURIER_ID_PATH}')
        assert response.json() == DATA.Results.ACCEPT_ORDER_NOT_ENOUGH_DATA

    def test_try_accept_order_without_courier_id_returns_correct_status_code(self):
        created_order = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}',
                                      data=DATA.Payloads.ORDER_CREATION_PAYLOAD)
        track_id = created_order.json()['track']
        get_track_info = requests.get(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}{track_id}')
        order_id = get_track_info.json()['order']['id']
        response = requests.put(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.ACCEPT_ORDER}{order_id}{DATA.Api.COURIER_ID_PATH}')
        assert response.status_code == DATA.Codes.BAD_REQUEST

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

    def test_try_accept_order_with_non_existing_courier_id(self):
        created_order = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}',
                                      data=DATA.Payloads.ORDER_CREATION_PAYLOAD)
        track_id = created_order.json()['track']
        get_track_info = requests.get(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}{track_id}')
        order_id = get_track_info.json()['order']['id']
        response = requests.put(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.ACCEPT_ORDER}{order_id}{DATA.Api.COURIER_ID_PATH}{DATA.Id.id_zero}')
        assert response.json() == DATA.Results.ACCEPT_ORDER_COURIER_NOT_EXIST

    def test_try_accept_order_with_non_existing_courier_id_returns_correct_status_code(self):
        created_order = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}',
                                      data=DATA.Payloads.ORDER_CREATION_PAYLOAD)
        track_id = created_order.json()['track']
        get_track_info = requests.get(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}{track_id}')
        order_id = get_track_info.json()['order']['id']
        response = requests.put(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.ACCEPT_ORDER}{order_id}{DATA.Api.COURIER_ID_PATH}{DATA.Id.id_zero}')
        assert response.status_code == DATA.Codes.NOT_FOUND

    def test_try_accept_order_non_existing_order(self, static_payloads):
        created_courier = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}',
                                        data=static_payloads)
        courier_id = created_courier.json()['id']
        response = requests.put(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.ACCEPT_ORDER}{DATA.Id.id_zero}{DATA.Api.COURIER_ID_PATH}{courier_id}')
        assert response.json() == DATA.Results.ACCEPT_ORDER_ORDER_NOT_EXIST
        requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{courier_id}')

    def test_try_accept_order_non_existing_order_returns_correct_status_code(self, static_payloads):
        created_courier = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.COURIER_LOGIN}',
                                        data=static_payloads)
        courier_id = created_courier.json()['id']
        response = requests.put(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.ACCEPT_ORDER}{DATA.Id.id_zero}{DATA.Api.COURIER_ID_PATH}{courier_id}')
        assert response.status_code == DATA.Codes.NOT_FOUND
        requests.delete(f'{DATA.Url.MAIN_URL}{DATA.Api.DELETE_COURIER}{courier_id}')


class TestGetOrderByNumber:
    def test_get_order_with_not_existing_order_returns_error(self):
        response = requests.get(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}{DATA.Id.id_zero}')
        assert response.json() == DATA.Results.GET_ORDER_BY_ITS_NUMBER_NOT_FOUND

    def test_get_order_with_not_existing_order_returns_correct_status_code(self):
        response = requests.get(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}{DATA.Id.id_zero}')
        assert response.status_code == DATA.Codes.NOT_FOUND

    def test_get_order_without_order_number_returns_error(self):
        response = requests.get(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}')
        assert response.json() == DATA.Results.GET_ORDER_WITHOUT_NUMBER

    def test_get_order_without_order_number_returns_correct_status_code(self):
        response = requests.get(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}')
        assert response.status_code == DATA.Codes.BAD_REQUEST

    def test_get_order_with_correct_number_returns_correct_response(self):
        created_order = requests.post(f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}',
                                      data=DATA.Payloads.ORDER_CREATION_PAYLOAD)
        track_id = created_order.json()['track']
        response = requests.get(
            f'{DATA.Url.MAIN_URL}{DATA.Api.ORDER_CREATION}{DATA.Api.FIND_ORDER_ID}{track_id}')
        assert response.status_code == DATA.Codes.SUCCESS
