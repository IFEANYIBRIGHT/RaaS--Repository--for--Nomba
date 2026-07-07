from pydantic import BaseModel


class VirtualAccountRequest(BaseModel):
    identifier: str
    virtual_account_number: str
