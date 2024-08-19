from pydantic import BaseModel, Field


class CreatePostRequestBody(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
