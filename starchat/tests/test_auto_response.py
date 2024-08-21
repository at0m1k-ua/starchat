from unittest.mock import MagicMock

from django.contrib.auth.models import User

from starchat.celery import app
from starchat.models.auto_response import AutoResponse
from starchat.services.auto_response import AutoResponseService
from starchat.services.censorship import CensorshipService
from starchat.services.openai_api import OpenaiApiService
from starchat.singleton import SingletonMeta
from starchat.tests.api.auto_response import AutoResponseTestApi
from starchat.tests.api.comment import CommentTestApi
from starchat.tests.api.post import PostTestApi
from starchat.tests.test_api import ApiTest


class AutoResponseTest(ApiTest):
    def setUp(self):
        super().setUp()
        self.__auto_response_api = AutoResponseTestApi(self)
        self.__post_api = PostTestApi(self)
        self.__comment_api = CommentTestApi(self)
        app.conf.update(CELERY_TASK_ALWAYS_EAGER=True)

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

    def test_auto_response_creates_comment_reply(self):
        class CensorshipServiceMock:
            is_harmful = MagicMock(return_value=False)
        SingletonMeta.set_mock(CensorshipService, CensorshipServiceMock())

        class FakeOpenaiApiService:
            is_available = True
        SingletonMeta.set_mock(OpenaiApiService, FakeOpenaiApiService())

        reply_text = self._gen_text()

        class ModifiedAutoResponseService(AutoResponseService):
            def _generate_reply(self, comment):
                return reply_text

        SingletonMeta.set_mock(AutoResponseService, ModifiedAutoResponseService())
        self.__auto_response_api.set(1)

        post = self.__post_api.create(self._gen_text())

        second_user_name = self._gen_text(8)
        second_user_pass = self._gen_text(8)
        User.objects.create_user(username=second_user_name, password=second_user_pass)

        created_comment_response = self.client.post(
            self.__comment_api.URL,
            {'post_id': post['id'], 'text': self._gen_text()},
            headers=self.jwt_auth(self.get_access_token(second_user_name, second_user_pass))
        )
        self.assertEqual(200, created_comment_response.status_code)

        comments_after_answer = self.__comment_api.read_comments_of_post(post_id=post['id'])
        self.assertEqual(2, len(comments_after_answer))
        self.assertEqual(created_comment_response.data, comments_after_answer[0])
        self.assertEqual(reply_text, comments_after_answer[1]['text'])
        self.assertEqual(created_comment_response.data['id'], comments_after_answer[1]['parent'])
