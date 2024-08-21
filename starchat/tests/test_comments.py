from starchat.tests.api.comment import CommentTestApi
from starchat.tests.api.post import PostTestApi
from starchat.tests.test_api import ApiTest


class CommentsTest(ApiTest):
    def setUp(self):
        super().setUp()
        self.__post_api = PostTestApi(test=self)
        self.__comment_api = CommentTestApi(test=self)
        self.__post = self.__post_api.create(self._gen_text())

    def test_create_comment_creates_readable_comment(self):
        comment_text = self._gen_text()
        created_comment = self.__comment_api.create(self.__post['id'], comment_text)
        self.assertEqual(comment_text, created_comment['text'])

        read_comment = self.__comment_api.read(created_comment['id'])
        self.assertEqual(created_comment, read_comment)

    def test_create_sub_comment(self):
        comment_1 = self.__comment_api.create(self.__post['id'], self._gen_text())
        comment_2 = self.__comment_api.create(self.__post['id'], self._gen_text(), parent_id=comment_1['id'])

        self.assertIsNone(comment_1['parent'])
        self.assertEqual(comment_1['id'], comment_2['parent'])

    def test_read_all_comments_of_post_retrieves_all_its_comments(self):
        comment_1 = self.__comment_api.create(self.__post['id'], self._gen_text())
        comment_2 = self.__comment_api.create(self.__post['id'], self._gen_text())

        get_response = self.__comment_api.read_comments_of_post(self.__post['id'])
        self.assertEqual([comment_1, comment_2], get_response)

    def test_update_comment_changes_its_text(self):
        initial_comment = self.__comment_api.create(self.__post['id'], self._gen_text())
        updated_comment = self.__comment_api.update(initial_comment['id'], self._gen_text())
        self.assertEqual(initial_comment['id'], updated_comment['id'])
        self.assertNotEqual(initial_comment['text'], updated_comment['text'])
    
    def test_delete_post_makes_it_inaccessible(self):
        created_comment = self.__comment_api.create(self.__post['id'], self._gen_text())
        comment_id = created_comment['id']
        self.__comment_api.read(comment_id, expected_status_code=200)

        self.__comment_api.delete(comment_id)
        self.__comment_api.read(comment_id, expected_status_code=404)
