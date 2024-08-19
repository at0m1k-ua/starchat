from starchat.tests.api.base import BaseTestApi


class CommentTestApi(BaseTestApi):
    URL = f'{BaseTestApi.URL}comment/'

    def create(self, post_id: int, text: str, expected_status_code: int = 200):
        response = self._test.client.post(
            self.URL,
            {'post_id': post_id, 'text': text},
            headers=self._jwt_auth()
        )
        self._test.assertEqual(expected_status_code, response.status_code)
        return response.data
