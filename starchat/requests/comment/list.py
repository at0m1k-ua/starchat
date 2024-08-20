from pydantic import BaseModel, Field


class ListCommentRequestParams(BaseModel):
    post_id: int = Field(ge=1)
