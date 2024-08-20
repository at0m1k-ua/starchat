from pydantic import BaseModel, Field


class DestroyItemRequestUrlParams(BaseModel):
    id: int = Field(ge=1)
