from datetime import date

from pydantic import BaseModel


class CommentAnalyticsRequest(BaseModel):
    date_from: date
    date_to: date
