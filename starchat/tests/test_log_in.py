from django.utils.crypto import get_random_string
from rest_framework.test import APITestCase


class LogInTest(APITestCase):
    def test_registered_user_can_obtain_tokens(self):
        username = get_random_string(length=8)
        password = get_random_string(length=32)

        get_user_info_response = self.client.get(
            '/api/v1/user/current/',
        )
        self.assertEqual(401, get_user_info_response.status_code)

        register_response = self.client.post(
            '/api/v1/accounts/register/',
            {
                'username': username,
                'password': password,
                'password_confirm': password,
            }
        )
        self.assertEqual(201, register_response.status_code)

        obtain_token_response = self.client.post(
            '/api/v1/token/',
            {
                'username': username,
                'password': password
            }
        )
        self.assertEqual(200, obtain_token_response.status_code)

        get_user_info_response = self.client.get(
            '/api/v1/user/current/',
            headers={
                'Authorization': f'Bearer {obtain_token_response.data["access"]}'
            }
        )
        self.assertEqual(200, get_user_info_response.status_code)
