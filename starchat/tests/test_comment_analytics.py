import datetime

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from starchat.models import Post, Comment
from starchat.tests.test_api import ApiTest


class CommentAnalyticsTest(ApiTest):
    def test_get_comment_analytics_returns_analytics(self):
        username = 'root'
        password = get_random_string(8)

        user = User.objects.create_superuser(username=username, password=password)
        user.save()

        post = Post.objects.create(sender_id=user.id, text='a', created_at=datetime.date(2024, 1, 1))
        post.save()

        comments = [
            Comment.objects.create(sender_id=user.id, post_id=post.id, is_banned=False),
            Comment.objects.create(sender_id=user.id, post_id=post.id, is_banned=False),
            Comment.objects.create(sender_id=user.id, post_id=post.id, is_banned=True),
            Comment.objects.create(sender_id=user.id, post_id=post.id, is_banned=False),
            Comment.objects.create(sender_id=user.id, post_id=post.id, is_banned=True),
            Comment.objects.create(sender_id=user.id, post_id=post.id, is_banned=True),
            Comment.objects.create(sender_id=user.id, post_id=post.id, is_banned=False),
            Comment.objects.create(sender_id=user.id, post_id=post.id, is_banned=False),
        ]

        updated_dates = [
            datetime.date(2024, 2, 1),
            datetime.date(2024, 2, 2),
            datetime.date(2024, 2, 2),
            datetime.date(2024, 2, 4),
            datetime.date(2024, 2, 5),
            datetime.date(2024, 2, 5),
            datetime.date(2024, 2, 5),
            datetime.date(2024, 2, 6),
        ]
        for comment, created_at in zip(comments, updated_dates):
            comment.save()
            comment.created_at = created_at
            comment.save()

        response = self.client.get(
            f'{self._API_PREFIX}analytics/comments/?date_from=2024-02-03&date_to=2024-02-05',
            headers=self.jwt_auth(self.get_access_token(username, password))
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual([
            {'date': datetime.date(2024, 2, 4), 'banned_count': 0, 'not_banned_count': 1},
            {'date': datetime.date(2024, 2, 5), 'banned_count': 2, 'not_banned_count': 1},
        ], list(response.data))
