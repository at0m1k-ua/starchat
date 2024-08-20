from pydantic import BaseModel, Field


class ListCommentRequestParams(BaseModel):
    post_id: int = Field(ge=1)

    @property
    def related_object_id(self):
        return self.post_id
