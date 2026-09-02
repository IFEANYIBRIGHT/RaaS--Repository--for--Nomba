from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    identifier: str
    password: str = Field(max_length=72)
