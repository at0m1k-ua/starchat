from pydantic import BaseModel, Field


class UpdatePostRequestUrlParams(BaseModel):
    id: int = Field(ge=1)


class UpdatePostRequestBody(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
