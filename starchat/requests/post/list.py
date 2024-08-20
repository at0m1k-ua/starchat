from pydantic import BaseModel, Field


class ListPostRequestParams(BaseModel):
    sender_id: int = Field(ge=1)

    @property
    def related_object_id(self):
        return self.sender_id
