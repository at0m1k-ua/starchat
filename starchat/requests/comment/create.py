from pydantic import BaseModel, Field


class CreateCommentRequestBody(BaseModel):
    post_id: int = Field(ge=1)
    text: str = Field(min_length=1, max_length=5000)
    parent_id: int = Field(ge=1, default=None)
