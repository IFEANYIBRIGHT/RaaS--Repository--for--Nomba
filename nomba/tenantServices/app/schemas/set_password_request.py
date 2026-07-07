from pydantic import BaseModel, Field


class SetPasswordRequest(BaseModel):
    identifier: str
    new_password: str = Field(min_length=8, max_length=19)
