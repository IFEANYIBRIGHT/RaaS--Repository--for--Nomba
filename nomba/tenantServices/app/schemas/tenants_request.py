from pydantic import BaseModel, Field


class TenantsRequest(BaseModel):
    name: str
    password: str = Field(min_length=8, max_length=19)
    tenant_email: str
    phone_number: str = Field(min_length=11, max_length=11)
    flat_no: str
