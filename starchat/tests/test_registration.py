from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.utils.crypto import get_random_string


class RegistrationTest(APITestCase):
    def test_registration_flow_creates_user(self):
        username = get_random_string(length=8)
        password = get_random_string(length=32)

        response = self.client.post(
            '/api/v1/accounts/register/',
            {
                'username': username,
                'password': password,
                'password_confirm': password,
            }
        )
        self.assertEqual(201, response.status_code)

        response_data = response.data
        user_from_db = User.objects.get(id=response_data['id'])
        self.assertEqual(response_data['username'], user_from_db.username)
