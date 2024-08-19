from starchat.tests.test_api import ApiTest


class PostsTest(ApiTest):

    def test_create_post_creates_post_with_right_sender_id(self):
        create_data = self.__create_post(self._gen_text())
        self.assertEqual(self._user.id, create_data['sender'])

    def test_read_all_posts_of_user_retrieves_all_their_posts(self):
        post1_text = self._gen_text()
        post1 = self.__create_post(post1_text)

        post2_text = self._gen_text()
        post2 = self.__create_post(post2_text)

        get_response = self.__read_posts_of_user(self._user.id)
        self.assertEqual([post2, post1], get_response)

    def test_update_post_changes_its_text(self):
        initial_content = self._gen_text()
        changed_content = self._gen_text()

        created_post = self.__create_post(initial_content)
        self.assertEqual(initial_content, created_post['text'])

        received_initial_post = self.__read_post(created_post['id'])
        self.assertEqual(initial_content, received_initial_post['text'])

        update_response = self.__update_post(created_post['id'], changed_content)
        self.assertEqual(changed_content, update_response['text'])

        received_changed_post = self.__read_post(created_post['id'])
        self.assertEqual(changed_content, received_changed_post['text'])

    def test_delete_post_makes_it_inaccessible(self):
        created_post = self.__create_post(self._gen_text())
        post_id = created_post['id']
        self.__read_post(post_id, expected_status_code=200)

        self.__delete_post(post_id)
        self.__read_post(post_id, expected_status_code=404)

    def __create_post(self, text: str, expected_status_code: int = 200):
        response = self.client.post(
            f'{self._API_PREFIX}posts/',
            {'text': text},
            headers=self._jwt_auth()
        )
        self.assertEqual(expected_status_code, response.status_code)
        return response.data

    def __read_post(self, post_id: int, expected_status_code: int = 200):
        response = self.client.get(
            f'{self._API_PREFIX}posts/{post_id}/',
            headers=self._jwt_auth()
        )
        self.assertEqual(expected_status_code, response.status_code)
        return response.data

    def __read_posts_of_user(self, user_id: int, expected_status_code: int = 200):
        response = self.client.get(
            f'{self._API_PREFIX}posts/?sender_id={user_id}',
            headers=self._jwt_auth()
        )
        self.assertEqual(expected_status_code, response.status_code)
        return response.data

    def __update_post(self, post_id: int, text: str, expected_status_code: int = 200):
        response = self.client.put(
            f'{self._API_PREFIX}posts/{post_id}/',
            {'text': text},
            headers=self._jwt_auth()
        )
        self.assertEqual(expected_status_code, response.status_code)
        return response.data

    def __delete_post(self, post_id: int, expected_status_code: int = 200):
        response = self.client.delete(
            f'{self._API_PREFIX}posts/{post_id}/',
            headers=self._jwt_auth()
        )
        self.assertEqual(expected_status_code, response.status_code)
