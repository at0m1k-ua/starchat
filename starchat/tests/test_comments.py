from starchat.tests.api.comment import CommentTestApi
from starchat.tests.api.post import PostTestApi
from starchat.tests.test_api import ApiTest


class CommentsTest(ApiTest):
    def setUp(self):
        super().setUp()
        self.__post_api = PostTestApi(test=self)
        self.__comment_api = CommentTestApi(test=self)

    def test_create_comment_creates_comment_in_db(self):
        created_post = self.__post_api.create(self._gen_text())
        created_comment = self.__comment_api.create(created_post['id'], self._gen_text())
        self.assertIsNotNone(created_comment)
