from pydantic import BaseModel, Field


class RetrievePostUrlParams(BaseModel):
    id: int = Field(ge=1)
