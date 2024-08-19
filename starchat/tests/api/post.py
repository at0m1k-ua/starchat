from starchat.tests.api.base import BaseTestApi


class PostTestApi(BaseTestApi):
    URL = f'{BaseTestApi.URL}post/'

    def create(self, text: str | None, expected_status_code: int = 200):
        response = self._test.client.post(
            self.URL,
            {'text': text},
            headers=self._jwt_auth()
        )
        self._test.assertEqual(expected_status_code, response.status_code)
        return response.data

    def read(self, post_id: int, expected_status_code: int = 200):
        response = self._test.client.get(
            f'{self.URL}{post_id}/',
            headers=self._jwt_auth()
        )
        self._test.assertEqual(expected_status_code, response.status_code)
        return response.data

    def read_posts_of_user(self, user_id: int, expected_status_code: int = 200):
        response = self._test.client.get(
            f'{self.URL}?sender_id={user_id}',
            headers=self._jwt_auth()
        )
        self._test.assertEqual(expected_status_code, response.status_code)
        return response.data

    def update(self, post_id: int, text: str, expected_status_code: int = 200):
        response = self._test.client.put(
            f'{self.URL}{post_id}/',
            {'text': text},
            headers=self._jwt_auth()
        )
        self._test.assertEqual(expected_status_code, response.status_code)
        return response.data

    def delete(self, post_id: int, expected_status_code: int = 200):
        response = self._test.client.delete(
            f'{self.URL}{post_id}/',
            headers=self._jwt_auth()
        )
        self._test.assertEqual(expected_status_code, response.status_code)
