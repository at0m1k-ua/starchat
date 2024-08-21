from starchat.models.auto_response import AutoResponse
from starchat.tests.api.auto_response import AutoResponseTestApi
from starchat.tests.test_api import ApiTest


class AutoResponseTest(ApiTest):
    def setUp(self):
        super().setUp()
        self.__auto_response_api = AutoResponseTestApi(self)

    def test_no_auto_response_returns_zero(self):
        get_response = self.__auto_response_api.get()
        self.assertEqual({'timeout': 0}, get_response)

    def test_auto_response_after_setup_changes_value(self):
        value = 120

        set_response = self.__auto_response_api.set(value)
        self.assertEqual({'timeout': value}, set_response)

        get_response = self.__auto_response_api.get()
        self.assertEqual({'timeout': value}, get_response)

    def test_auto_response_after_setting_zero_deletes_item_from_db(self):
        value = 90

        set_response = self.__auto_response_api.set(value)
        self.assertEqual({'timeout': value}, set_response)
        auto_response = AutoResponse.objects.get(user_id=self._user.id)
        self.assertEqual(value, auto_response.timeout)

        remove_response = self.__auto_response_api.set(0)
        self.assertEqual({'timeout': 0}, remove_response)
        get_response = self.__auto_response_api.get()
        self.assertEqual({'timeout': 0}, get_response)
        self.assertFalse(AutoResponse.objects.filter(user_id=self._user.id).exists())
