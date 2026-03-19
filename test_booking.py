from constants import BOOKING_ENDPOINT


class TestAuth:
    booking_id = None
    create_booking = None
    put_booking = None

# TODO Создаём бронирование
class TestCreateBooking(TestAuth):
    def test_create_booking(self,requester,auth_token, booking_data):
        create_booking = requester.send_request(
                                        method='POST',
                                        endpoint=BOOKING_ENDPOINT,
                                        headers= auth_token,
                                        data=booking_data,
                                        expected_status=200)
        TestAuth.booking_id = create_booking.json().get("bookingid")
        assert TestAuth.booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], \
            "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], \
            "Заданная стоимость не совпадает"
        TestAuth.create_booking = create_booking


# TODO Проверяем, что бронирование можно получить по ID
class TestGetBookings(TestAuth):
    def test_get_booking(self, requester, auth_token):
        get_booking = requester.send_request(
                                        method='GET',
                                        endpoint=BOOKING_ENDPOINT + f'/{TestAuth.booking_id}',
                                        headers=auth_token,
                                        expected_status=200)
        assert get_booking.json()["lastname"] == self.create_booking.json()["booking"]["lastname"], "Заданная фамилия не совпадает"


# TODO Изменяем данные через PUT
class TestPutBooking(TestAuth):
    def test_put_booking(self, requester, auth_token, booking_data):
        put_booking = requester.send_request(
                                        method='PUT',
                                        endpoint=BOOKING_ENDPOINT + f'/{TestAuth.booking_id}',
                                        headers=auth_token,
                                        data=booking_data,
                                        expected_status=200)
        put_booking = put_booking.json()
        assert put_booking["firstname"] != self.create_booking.json()["booking"]["firstname"], "Заданное имя совпадает"
        assert put_booking["totalprice"] != self.create_booking.json()["booking"]["totalprice"], "Заданная стоимость совпадает"
        assert put_booking["firstname"] == booking_data["firstname"], "Имя не обновилось"
        assert put_booking["lastname"] == booking_data["lastname"], "Фамилия не обновилась"
        TestAuth.put_booking = put_booking


# TODO Изменяем данные через PATCH
class TestPatchBooking(TestAuth):
    def test_patch_booking(self, requester, auth_token, patch_json):
        patch_booking = requester.send_request(
                                        method='PATCH',
                                        endpoint=BOOKING_ENDPOINT + f'/{TestAuth.booking_id}',
                                        headers=auth_token,
                                        data=patch_json,
                                        expected_status=200)
        patch_booking = patch_booking.json()
        assert patch_booking["firstname"] != self.put_booking["firstname"], "Имя совпадает"
        assert patch_booking["lastname"] != self.put_booking["lastname"], "Фамилия совпадает"
        assert patch_booking["totalprice"] == self.put_booking["totalprice"], "Cтоимость не совпадает"
        assert patch_booking["firstname"] == patch_json["firstname"], "Имя не обновилось"
        assert patch_booking["lastname"] == patch_json["lastname"], "Фамилия не обновилась"


# TODO Удаляем бронирование
class TestDeliteBooking(TestAuth):
    def test_delite_booking(self, requester, auth_token):
        requester.send_request(
                    method='DELETE',
                    endpoint=BOOKING_ENDPOINT + f'/{TestAuth.booking_id}',
                    headers=auth_token,
                    expected_status=201)

        requester.send_request(
                    method='GET',
                    endpoint=BOOKING_ENDPOINT + f'/{TestAuth.booking_id}',
                    headers=auth_token,
                    expected_status=404)


class TestNegativeBooking(TestAuth):
    def test_delete_not_auth(self, requester, generate_number):
        # TODO Попытка удалить обьект без прав доступа
        requester.send_request(
                    method='DELETE',
                    endpoint=BOOKING_ENDPOINT + f'/{generate_number}',
                    expected_status=405)

    def test_delete_auth(self, requester, generate_number, auth_token):
        # TODO Попытка удалить не свой обьект, с правами доступа
        requester.send_request(
                    method='DELETE',
                    endpoint=BOOKING_ENDPOINT + f'/{generate_number}',
                    headers=auth_token,
                    expected_status=405)

    def test_put(self, requester, generate_number, auth_token, booking_data):
        # TODO Попытка удалить не свой обьект, с правами доступа
        requester.send_request(
                    method='PUT',
                    endpoint=BOOKING_ENDPOINT + f'/{generate_number}',
                    headers=auth_token,
                    data=booking_data,
                    expected_status=405)


    def test_search(self, requester, generate_number, auth_token):
        # TODO Попытка найти несуществующий обьект
        requester.send_request(
                    method='GET',
                    endpoint=BOOKING_ENDPOINT + f'/{generate_number}',
                    headers=auth_token,
                    expected_status=404)



    def test_none_json(self, generate_number, auth_token, requester):
        # TODO Передача пустых данных в PUT
        requester.send_request(
                    method='PUT',
                    endpoint=BOOKING_ENDPOINT + f'/{generate_number}',
                    headers=auth_token,
                    expected_status=400)
