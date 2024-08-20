class BaseTestApi:
    URL = '/api/v1/'

    def __init__(self, test):
        self._test = test
