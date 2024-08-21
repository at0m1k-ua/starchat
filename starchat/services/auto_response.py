from starchat import tasks
from starchat.models import Comment
from starchat.services.openai_api import OpenaiApiService
from starchat.singleton import SingletonMeta


class AutoResponseService(metaclass=SingletonMeta):
    TIMEOUT_MULTIPLIER = 60

    def register(self, comment: Comment):
        if comment.post.sender.id == comment.sender.id:
            return

        autoresponse_or_empty = comment.post.sender.autoresponse_set
        if not autoresponse_or_empty.exists():
            return

        if not OpenaiApiService().is_available:
            return

        timeout = autoresponse_or_empty.get().timeout
        reply = self._generate_reply(comment)
        tasks.save_comment.apply_async(
            kwargs={
                'sender_id': comment.post.sender.id,
                'parent_id': comment.id,
                'post_id': comment.post.id,
                'text': reply
            },
            countdown=timeout*self.TIMEOUT_MULTIPLIER)
        comment.save()

    def _generate_reply(self, comment):
        return OpenaiApiService().process([
                    {"role": "system", "content":
                        "You are a auto-answering bot. User A writes post, "
                        "User B writes a comment. You should create an answer "
                        "from user B to user A on this comment. Now you will "
                        "receive a post and a comment. Make up an answer and send it back. "
                        "It should not contain any headers, footers or braces, like 'Answer:' etc. "
                        "It should be a raw comment to insert."},
                    {"role": "user", "content": f"Post:\n{comment.post.text}\n\nComment:\n{comment.text}"},
                ])
