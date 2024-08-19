class BaseTestApi:
    URL = '/api/v1/'

    def __init__(self, test):
        self._test = test

    def _jwt_auth(self):
        return {'Authorization': f'Bearer {self._test.access_token}'}
