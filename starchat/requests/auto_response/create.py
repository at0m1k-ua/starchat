from pydantic import BaseModel, Field


class CreateAutoResponseRequestBody(BaseModel):
    timeout: int = Field(ge=0)
