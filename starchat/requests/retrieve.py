from pydantic import BaseModel, Field


class RetrieveItemUrlParams(BaseModel):
    id: int = Field(ge=1)
