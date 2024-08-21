from starchat.tests.api.base import BaseTestApi


class AutoResponseTestApi(BaseTestApi):
    URL = f'{BaseTestApi.URL}auto_response/'

    def set(self, value: int, expected_status_code: int = 200):
        response = self._test.client.post(
            self.URL,
            {'timeout': value},
            headers=self._test.jwt_auth()
        )
        self._test.assertEqual(expected_status_code, response.status_code)
        return response.data

    def get(self, expected_status_code: int = 200):
        response = self._test.client.get(
            self.URL,
            headers=self._test.jwt_auth()
        )
        self._test.assertEqual(expected_status_code, response.status_code)
        return response.data
