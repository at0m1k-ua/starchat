from starchat.tests.api.post import PostTestApi
from starchat.tests.test_api import ApiTest


class PostsTest(ApiTest):
    def setUp(self):
        super().setUp()
        self.__api = PostTestApi(test=self)

    def test_create_post_creates_post_with_right_sender_id(self):
        create_data = self.__api.create_post(self._gen_text())
        self.assertEqual(self._user.id, create_data['sender'])

    def test_create_post_with_no_data_fails(self):
        create_response = self.client.post(
            f'{self.__api.URL}',
            headers=self.__api._jwt_auth()
        )
        self.assertEqual(400, create_response.status_code)

    def test_create_post_with_empty_data_fails(self):
        create_response = self.client.post(
            f'{self.__api.URL}',
            {},
            headers=self.__api._jwt_auth()
        )
        self.assertEqual(400, create_response.status_code)

    def test_create_post_with_empty_text_fails(self):
        self.__api.create_post('', 400)

    def test_read_all_posts_of_user_retrieves_all_their_posts(self):
        post1_text = self._gen_text()
        post1 = self.__api.create_post(post1_text)

        post2_text = self._gen_text()
        post2 = self.__api.create_post(post2_text)

        get_response = self.__api.read_posts_of_user(self._user.id)
        self.assertEqual([post2, post1], get_response)

    def test_update_post_changes_its_text(self):
        initial_content = self._gen_text()
        changed_content = self._gen_text()

        created_post = self.__api.create_post(initial_content)
        self.assertEqual(initial_content, created_post['text'])

        received_initial_post = self.__api.read_post(created_post['id'])
        self.assertEqual(initial_content, received_initial_post['text'])

        update_response = self.__api.update_post(created_post['id'], changed_content)
        self.assertEqual(changed_content, update_response['text'])

        received_changed_post = self.__api.read_post(created_post['id'])
        self.assertEqual(changed_content, received_changed_post['text'])

    def test_delete_post_makes_it_inaccessible(self):
        created_post = self.__api.create_post(self._gen_text())
        post_id = created_post['id']
        self.__api.read_post(post_id, expected_status_code=200)

        self.__api.delete_post(post_id)
        self.__api.read_post(post_id, expected_status_code=404)
