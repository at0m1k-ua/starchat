from pydantic import BaseModel, Field


class UpdateCommentRequestUrlParams(BaseModel):
    id: int = Field(ge=1)


class UpdateCommentRequestBody(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
