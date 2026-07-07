from pydantic import BaseModel


class SetPasswordRequest(BaseModel):
    identifier: str
    new_password: str
