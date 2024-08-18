from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework.test import APITestCase

from starchat.models import Post


class PostsTest(APITestCase):
    def setUp(self) -> None:
        username = get_random_string(length=8)
        password = get_random_string(length=32)

        user_id = self.client.post(
            '/api/v1/accounts/register/',
            {
                'username': username,
                'password': password,
                'password_confirm': password,
            }
        ).data['id']
        self.__user = User.objects.get(id=user_id)

        self.__access_token = self.client.post(
            '/api/v1/token/',
            {
                'username': username,
                'password': password
            }
        ).data['access']

    def test_create_post_creates_post_with_right_sender_id(self):
        create_response = self.client.post(
            '/api/v1/posts/',
            {'text': get_random_string(length=128)},
            headers=self.__jwt_auth()
        )
        self.assertEqual(200, create_response.status_code)
        self.assertEqual(self.__user.id, create_response.data['sender'])

    def test_update_post_changes_its_text(self):
        initial_content = get_random_string(length=128)
        changed_content = get_random_string(length=128)

        create_response = self.client.post(
            '/api/v1/posts/',
            {'text': initial_content},
            headers=self.__jwt_auth()
        )
        self.assertEqual(200, create_response.status_code)
        received_initial_content = create_response.data['text']
        self.assertEqual(initial_content, received_initial_content)
        post_from_db = Post.objects.get(id=create_response.data['id'])
        self.assertEqual(initial_content, post_from_db.text)

        update_response = self.client.put(
            f'/api/v1/posts/{create_response.data["id"]}/',
            {'text': changed_content},
            headers=self.__jwt_auth()
        )
        self.assertEqual(200, update_response.status_code)
        received_changed_content = update_response.data['text']
        self.assertEqual(changed_content, received_changed_content)
        post_from_db.refresh_from_db()
        self.assertEqual(changed_content, post_from_db.text)

    def __jwt_auth(self):
        return {'Authorization': f'Bearer {self.__access_token}'}
