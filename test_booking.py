from constants import header, base_url
import requests


# TODO Создаём session для всех классов
class TestAuth:
    session = None
    booking_id = None
    create_booking = None
    put_booking = None

    def test_auth_session(self):
        session = requests.Session()
        session.headers.update(header)
        response = session.post(f'{base_url}/auth',
                                 json={'username' : 'admin', 'password' : 'password123'})
        assert response.status_code == 200, f'Ошибка авторизации: {response.status_code}'
        token = response.json().get('token')
        assert token is not None, "В ответе не оказалось токена"
        session.headers.update({"Cookie": f"token={token}"})
        TestAuth.session = session


 # TODO Создаём бронирование
class TestCreateBooking(TestAuth):
    def test_create_booking(self, booking_data):
        create_booking = TestAuth.session.post(f"{base_url}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"
        TestAuth.booking_id = create_booking.json().get("bookingid")
        assert TestAuth.booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], \
            "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], \
            "Заданная стоимость не совпадает"
        TestAuth.create_booking = create_booking


# TODO Проверяем, что бронирование можно получить по ID
class TestGetBookings(TestAuth):
    def test_get_booking(self, booking_data):
        get_booking = TestAuth.session.get(f"{base_url}/booking/{TestAuth.booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == TestAuth.create_booking.json()["booking"]["lastname"], "Заданная фамилия не совпадает"


# TODO Изменяем данные через PUT
class TestPutBooking(TestAuth):
    def test_put_booking(self, booking_data):
        put_booking = TestAuth.session.put(f'{base_url}/booking/{TestAuth.booking_id}', json=booking_data)
        assert put_booking.status_code == 200, "Данные не изменены"
        assert put_booking.json()["firstname"] != TestAuth.create_booking.json()["booking"]["firstname"], "Заданное имя совпадает"
        assert put_booking.json()["totalprice"] != TestAuth.create_booking.json()["booking"]["totalprice"], "Заданная стоимость совпадает"
        assert put_booking.json()["firstname"] == booking_data["firstname"], "Имя не обновилось"
        assert put_booking.json()["lastname"] == booking_data["lastname"], "Фамилия не обновилась"
        TestAuth.put_booking = put_booking


# TODO Изменяем данные через PATCH
class TestPatchBooking(TestAuth):
    def test_patch_booking(self, patch_json):
        patch_booking = TestAuth.session.patch(f"{base_url}/booking/{TestAuth.booking_id}", json=patch_json)
        assert patch_booking.status_code == 200, "Данные не изменены"
        assert patch_booking.json()["firstname"] != TestAuth.put_booking.json()["firstname"], "Имя совпадает"
        assert patch_booking.json()["lastname"] != TestAuth.put_booking.json()["lastname"], "Фамилия совпадает"
        assert patch_booking.json()["totalprice"] == TestAuth.put_booking.json()["totalprice"], "Cтоимость не совпадает"
        assert patch_booking.json()["firstname"] == patch_json["firstname"], "Имя не обновилось"
        assert patch_booking.json()["lastname"] == patch_json["lastname"], "Фамилия не обновилась"


# TODO Удаляем бронирование
class TestDeliteBooking(TestAuth):
    def test_delite_booking(self):
        deleted_booking = TestAuth.session.delete(f"{base_url}/booking/{TestAuth.booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась" # TODO Должен быть 204
        # TODO Проверяем, что бронирование больше недоступно
        get_booking_delite = TestAuth.session.get(f"{base_url}/booking/{TestAuth.booking_id}")
        assert get_booking_delite.status_code == 404, "Бронь не удалилась"


class TestNegativeBooking(TestAuth):
    def test_delete_not_auth(self, generate_number):
        # TODO Попытка удалить обьект без прав доступа
        four_negative_booking = requests.delete(f'{base_url}/booking/{generate_number}')
        assert four_negative_booking.status_code == 403, "Сервер принимает корректный запрос"

    def test_delete_auth(self, generate_number):
        # TODO Попытка удалить не свой обьект, с правами доступа
        five_negative_booking = TestAuth.session.delete(f'{base_url}/booking/{generate_number}')
        assert five_negative_booking.status_code == 405, "Сервер принимает корректный запрос"

    def test_put(self, booking_data, generate_number):
        # TODO Попытка объновить несуществующий обьект
        six_negative_booking = TestAuth.session.put(f'{base_url}/booking/{generate_number}', json=booking_data)
        assert six_negative_booking.status_code == 405, "Сервер принимает корректный запрос"

    def test_search(self, generate_number):
        # TODO Попытка найти несуществующий обьект
        seven_negative_booking = TestAuth.session.get(f"{base_url}/booking/{generate_number}")
        assert seven_negative_booking.status_code == 404, "Сервер принимает корректный запрос"

    def test_none_json(self, generate_number, three_negative_scenario_json):
        # TODO Передача пустых данных в PUT
        eight_negative_booking = TestAuth.session.put(f'{base_url}/booking/{generate_number}', json=three_negative_scenario_json)
        assert eight_negative_booking.status_code == 400, "Сервер принимает корректный запрос"