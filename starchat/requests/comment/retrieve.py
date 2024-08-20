from pydantic import BaseModel, Field


class RetrieveCommentUrlParams(BaseModel):
    id: int = Field(ge=1)
