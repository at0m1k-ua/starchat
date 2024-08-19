from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework.test import APITestCase


class PostsTest(APITestCase):
    __API_PREFIX = '/api/v1/'

    def setUp(self) -> None:
        username = get_random_string(length=8)
        password = get_random_string(length=32)

        user_id = self.client.post(
            f'{self.__API_PREFIX}accounts/register/',
            {
                'username': username,
                'password': password,
                'password_confirm': password,
            }
        ).data['id']
        self.__user = User.objects.get(id=user_id)

        self.__access_token = self.client.post(
            f'{self.__API_PREFIX}token/',
            {
                'username': username,
                'password': password
            }
        ).data['access']

    def test_create_post_creates_post_with_right_sender_id(self):
        create_data = self.__create_post(get_random_string(length=128))
        self.assertEqual(self.__user.id, create_data['sender'])

    def test_read_all_posts_of_user_retrieves_all_their_posts(self):
        post1_text = get_random_string(length=128)
        post1 = self.__create_post(post1_text)

        post2_text = get_random_string(length=128)
        post2 = self.__create_post(post2_text)

        get_response = self.__read_posts_of_user(self.__user.id)
        self.assertEqual([post2, post1], get_response)

    def test_update_post_changes_its_text(self):
        initial_content = get_random_string(length=128)
        changed_content = get_random_string(length=128)

        created_post = self.__create_post(initial_content)
        self.assertEqual(initial_content, created_post['text'])

        received_initial_post = self.__read_post(created_post['id'])
        self.assertEqual(initial_content, received_initial_post['text'])

        update_response = self.__update_post(created_post['id'], changed_content)
        self.assertEqual(changed_content, update_response['text'])

        received_changed_post = self.__read_post(created_post['id'])
        self.assertEqual(changed_content, received_changed_post['text'])

    def test_delete_post_makes_it_inaccessible(self):
        created_post = self.__create_post(get_random_string(length=128))
        post_id = created_post['id']
        self.__read_post(post_id, expected_status_code=200)

        self.__delete_post(post_id)
        self.__read_post(post_id, expected_status_code=404)

    def __create_post(self, text: str, expected_status_code: int = 200):
        response = self.client.post(
            f'{self.__API_PREFIX}posts/',
            {'text': text},
            headers=self.__jwt_auth()
        )
        self.assertEqual(expected_status_code, response.status_code)
        return response.data

    def __read_post(self, post_id: int, expected_status_code: int = 200):
        response = self.client.get(
            f'{self.__API_PREFIX}posts/{post_id}/',
            headers=self.__jwt_auth()
        )
        self.assertEqual(expected_status_code, response.status_code)
        return response.data

    def __read_posts_of_user(self, user_id: int, expected_status_code: int = 200):
        response = self.client.get(
            f'{self.__API_PREFIX}posts/?sender_id={user_id}',
            headers=self.__jwt_auth()
        )
        self.assertEqual(expected_status_code, response.status_code)
        return response.data

    def __update_post(self, post_id: int, text: str, expected_status_code: int = 200):
        response = self.client.put(
            f'{self.__API_PREFIX}posts/{post_id}/',
            {'text': text},
            headers=self.__jwt_auth()
        )
        self.assertEqual(expected_status_code, response.status_code)
        return response.data

    def __delete_post(self, post_id: int, expected_status_code: int = 200):
        response = self.client.delete(
            f'{self.__API_PREFIX}posts/{post_id}/',
            headers=self.__jwt_auth()
        )
        self.assertEqual(expected_status_code, response.status_code)

    def __jwt_auth(self):
        return {'Authorization': f'Bearer {self.__access_token}'}
