from constants import base_url
import requests


class TestBookings:
    def test_positive_booking(self, auth_session, booking_data, new_put_json, patch_json):
        # TODO Создаём бронирование
        create_booking = auth_session.post(f"{base_url}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], \
            "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], \
            "Заданная стоимость не совпадает"

        # TODO Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{base_url}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        # TODO Изменяем данные через PUT
        put_booking = auth_session.put(f'{base_url}/booking/{booking_id}', json=new_put_json)
        assert put_booking.status_code == 200, "Данные не изменены"
        assert put_booking.json()["firstname"] != get_booking.json()["firstname"], "Заданное имя совпадает"
        assert put_booking.json()["totalprice"] != get_booking.json()["totalprice"], "Заданная стоимость совпадает"
        assert put_booking.json()["firstname"] == new_put_json["firstname"], "Имя не обновилось"
        assert put_booking.json()["lastname"] == new_put_json["lastname"], "Фамилия не обновилась"

        # TODO Изменяем данные через PATCH
        patch_booking = auth_session.patch(f"{base_url}/booking/{booking_id}", json=patch_json)
        assert patch_booking.status_code == 200, "Данные не изменены"
        assert patch_booking.json()["firstname"] != put_booking.json()["firstname"], "Имя совпадает"
        assert patch_booking.json()["lastname"] != put_booking.json()["lastname"], "Фамилия совпадает"
        assert patch_booking.json()["totalprice"] == put_booking.json()["totalprice"], "Cтоимость не совпадает"
        assert patch_booking.json()["firstname"] == patch_json["firstname"], "Имя не обновилось"
        assert patch_booking.json()["lastname"] == patch_json["lastname"], "Фамилия не обновилась"

        # TODO Удаляем бронирование
        deleted_booking = auth_session.delete(f"{base_url}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась" # TODO Должен быть 204
        # TODO Проверяем, что бронирование больше недоступно
        get_booking_delite = auth_session.get(f"{base_url}/booking/{booking_id}")
        assert get_booking_delite.status_code == 404, "Бронь не удалилась"

    def test_negative_booking(self, auth_session, negative_scenario_json, two_negative_scenario_json, booking_data,
                              three_negative_scenario_json):
        # TODO Создание учетной записи без "lastname"
        create_booking = auth_session.post(f'{base_url}/booking', json=negative_scenario_json)
        assert create_booking.status_code == 500, f"Учетная запись создана {create_booking.status_code}"

        # TODO  Создание int в замен str в "lastname"
        two_negative_booking = auth_session.post(f'{base_url}/booking', json=two_negative_scenario_json)
        assert two_negative_booking.status_code == 500, f"Учетная запись создана {two_negative_booking.status_code}"

        # TODO Попытка удалить обьект без прав доступа
        four_negative_booking = requests.delete(f'{base_url}/booking/{444455555444}')
        assert four_negative_booking.status_code == 403, "Сервер принимает корректный запрос"

        # TODO Попытка удалить не свой обьект, с правами доступа
        five_negative_booking = auth_session.delete(f'{base_url}/booking/{444455555444}')
        assert five_negative_booking.status_code == 405, "Сервер принимает корректный запрос"

        # TODO Попытка объновить несуществующий обьект
        six_negative_booking = auth_session.put(f'{base_url}/booking/{444455555444}', json=booking_data)
        assert six_negative_booking.status_code == 405, "Сервер принимает корректный запрос"

        # TODO Попытка найти несуществующий обьект
        seven_negative_booking = auth_session.get(f"{base_url}/booking/{444455554444}")
        assert seven_negative_booking.status_code == 404, "Сервер принимает корректный запрос"

        # TODO Передача пустых данных в PUT
        eight_negative_booking = auth_session.put(f'{base_url}/booking/{4}', json=three_negative_scenario_json)
        assert eight_negative_booking.status_code == 400, "Сервер принимает корректный запрос"