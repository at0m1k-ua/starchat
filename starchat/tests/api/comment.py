from starchat.tests.api.base import BaseTestApi


class CommentTestApi(BaseTestApi):
    URL = f'{BaseTestApi.URL}comment/'

    def create(self, post_id: int, text: str, parent_id: int = None, expected_status_code: int = 200):
        body = {'post_id': post_id, 'text': text}
        if parent_id:
            body['parent_id'] = parent_id

        response = self._test.client.post(
            self.URL,
            body,
            headers=self._test.jwt_auth()
        )
        self._test.assertEqual(expected_status_code, response.status_code)
        return response.data

    def read(self, comment_id: int, expected_status_code: int = 200):
        response = self._test.client.get(
            f'{self.URL}{comment_id}/',
            headers=self._test.jwt_auth()
        )
        self._test.assertEqual(expected_status_code, response.status_code)
        return response.data

    def read_comments_of_post(self, post_id: int, expected_status_code: int = 200):
        response = self._test.client.get(
            f'{self.URL}?post_id={post_id}',
            headers=self._test.jwt_auth()
        )
        self._test.assertEqual(expected_status_code, response.status_code)
        return response.data

    def update(self, comment_id, text: str, expected_status_code: int = 200):
        response = self._test.client.put(
            f'{self.URL}{comment_id}/',
            {'text': text},
            headers=self._test.jwt_auth()
        )
        self._test.assertEqual(expected_status_code, response.status_code)
        return response.data

    def delete(self, post_id: int, expected_status_code: int = 200):
        response = self._test.client.delete(
            f'{self.URL}{post_id}/',
            headers=self._test.jwt_auth()
        )
        self._test.assertEqual(expected_status_code, response.status_code)

