from pydantic import BaseModel, Field


class TenantsRequests(BaseModel):
    name: str
    tenant_email: str
    phone_number: str = Field(min_length=11, max_length=11)
    flat_no: str
    monthly_rent: int = 0
    lease_start: str = ""
    landlord_email: str
