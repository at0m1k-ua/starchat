from pydantic import BaseModel, Field


class DestroyPostRequestUrlParams(BaseModel):
    id: int = Field(gt=1)
