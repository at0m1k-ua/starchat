from pydantic import BaseModel, Field


class DestroyPostRequestUrlParams(BaseModel):
    id: int = Field(ge=1)
