from celery import shared_task

from starchat.models import Comment


@shared_task
def save_comment(**kwargs):
    new_comment = Comment(**kwargs)
    new_comment.save()
    new_comment.refresh_from_db()
    return new_comment.id
