import pytest

from genlogic import GeneratedPayloads
from yandex_precode import StaticData


@pytest.fixture
def payload():
    payload = GeneratedPayloads()
    return payload


@pytest.fixture()
def static_payloads():
    tries = StaticData()
    whole = tries.register_new_courier_and_return_login_password()
    STATIC_PAYLOAD = {
        "login": whole[0],
        "password": whole[1],
        "firstName": whole[2],

    }
    return STATIC_PAYLOAD
