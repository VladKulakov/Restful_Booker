import pytest
import requests
from faker import Faker
faker = Faker()

@pytest.fixture()
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

@pytest.fixture
def three_negative_scenario_json():
    return {}

@pytest.fixture(scope='session')
def generate_number():
    return faker.random_int(min=10000000, max=100000000)