from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework.test import APITestCase


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

    def test_read_all_posts_of_user_retrieves_all_their_posts(self):
        post1_text = get_random_string(length=128)
        post1_response = self.client.post(
            '/api/v1/posts/',
            {'text': post1_text},
            headers=self.__jwt_auth()
        )
        self.assertEqual(200, post1_response.status_code)
        post1 = post1_response.data

        post2_text = get_random_string(length=128)
        post2_response = self.client.post(
            '/api/v1/posts/',
            {'text': post2_text},
            headers=self.__jwt_auth()
        )
        self.assertEqual(200, post2_response.status_code)
        post2 = post2_response.data

        get_response = self.client.get(
            f'/api/v1/posts/?sender_id={self.__user.id}',
            headers=self.__jwt_auth()
        )
        self.assertEqual(200, get_response.status_code)

        self.assertEqual([post2, post1], get_response.data)

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

        received_initial_post = self.client.get(
            f'/api/v1/posts/{create_response.data["id"]}/',
            headers=self.__jwt_auth()
        )
        self.assertEqual(initial_content, received_initial_post.data['text'])

        update_response = self.client.put(
            f'/api/v1/posts/{create_response.data["id"]}/',
            {'text': changed_content},
            headers=self.__jwt_auth()
        )
        self.assertEqual(200, update_response.status_code)
        received_changed_content = update_response.data['text']
        self.assertEqual(changed_content, received_changed_content)

        received_changed_post = self.client.get(
            f'/api/v1/posts/{update_response.data["id"]}/',
            headers=self.__jwt_auth()
        )
        self.assertEqual(changed_content, received_changed_post.data['text'])

    def __jwt_auth(self):
        return {'Authorization': f'Bearer {self.__access_token}'}
