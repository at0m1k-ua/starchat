from pydantic import BaseModel, Field


class ListPostRequestParams(BaseModel):
    sender_id: int = Field(ge=1)
