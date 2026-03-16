import pytest
import requests
from faker import Faker
from constants import header, base_url

@pytest.fixture(scope='session')
def auth_session():
    session = requests.Session()
    session.headers.update(header)
    response = session.post(f'{base_url}/auth',
                             json={'username' : 'admin', 'password' : 'password123'})
    assert response.status_code == 200, f'Ошибка авторизации: {response.status_code}'
    token = response.json().get('token')
    assert token is not None, "В ответе не оказалось токена"
    session.headers.update({"Cookie": f"token={token}"})
    return session

faker = Faker()

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

@pytest.fixture
def new_put_json():
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

@pytest.fixture
def patch_json():
    return {
        'firstname': faker.first_name(),
        'lastname': faker.last_name()
    }


@pytest.fixture
def negative_scenario_json():
    return {
        'firstname': faker.first_name(),
        'totalprice': faker.random_int(min=100, max=100000),
        'depositpaid': True,
        'bookingdates': {
            'checkin': '2024-04-05',
            'checkout': '2024-04-08'
        },
        "additionalneeds": "Cigars"
    }

@pytest.fixture
def two_negative_scenario_json():
    return {
        'firstname': faker.first_name(),
        'lastname': faker.random_int(min=100, max=100000),
        'totalprice': faker.random_int(min=100, max=100000),
        'depositpaid': True,
        'bookingdates': {
            'checkin': '2024-04-05',
            'checkout': '2024-04-08'
        },
        "additionalneeds": "Cigars"
    }

@pytest.fixture
def three_negative_scenario_json():
    return {}