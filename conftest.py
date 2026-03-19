import pytest
import requests
from faker import Faker
faker = Faker()
from constants import BASE_URL, AUTH_ENDPOINT
from custom_requester.custom_requester import CustomRequester



@pytest.fixture
def booking_data():
    return {
        'firstname': faker.first_name(),
        'lastname': faker.last_name(),
        'totalprice': faker.random_int(min=100, max=100000),
        'depositpaid': True,
        'bookingdates': {
            'checkin': '2024-04-05',
            'checkout': '2024-04-08'
        },
        "additionalneeds": "Cigars"
    }

@pytest.fixture(scope='session')
def patch_json():
    return {
        'firstname': faker.first_name(),
        'lastname': faker.last_name()
    }


@pytest.fixture(scope='session')
def generate_number():
    return faker.random_int(min=10000000, max=100000000)


@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)


@pytest.fixture(scope="session")
def auth_token(requester):
    """Фикстура для получения токена один раз за сессию"""
    data = {'username': 'admin', 'password': 'password123'}
    response = requester.send_request(
        method='POST',
        endpoint=AUTH_ENDPOINT,
        data=data,
        expected_status=200
    )
    token = response.json().get('token')
    assert token is not None, "В ответе не оказалось токена"
    return {"Cookie": f"token={token}"}