from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework.test import APITestCase


class ApiTest(APITestCase):
    _API_PREFIX = '/api/v1/'

    def setUp(self) -> None:
        username = get_random_string(length=8)
        password = get_random_string(length=32)

        user_id = self.client.post(
            f'{self._API_PREFIX}accounts/register/',
            {
                'username': username,
                'password': password,
                'password_confirm': password,
            }
        ).data['id']
        self._user = User.objects.get(id=user_id)

        self.access_token = self.get_access_token(username, password)

    def get_access_token(self, username, password):
        return self.client.post(
            f'{self._API_PREFIX}token/',
            {
                'username': username,
                'password': password
            }
        ).data['access']

    @staticmethod
    def _gen_text(length: int = 128):
        return get_random_string(length=length)

    def jwt_auth(self, access_token=None):
        if not access_token:
            access_token = self.access_token
        return {'Authorization': f'Bearer {access_token}'}
    