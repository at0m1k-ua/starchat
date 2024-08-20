from pydantic import BaseModel, Field


class DestroyCommentRequestUrlParams(BaseModel):
    id: int = Field(ge=1)
