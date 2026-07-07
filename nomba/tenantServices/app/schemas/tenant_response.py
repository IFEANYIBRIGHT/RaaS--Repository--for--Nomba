from pydantic import BaseModel


class TenantResponse(BaseModel):
    id: str
    name: str
    phone_number: str
    tenant_email: str
    flat_no: str
    monthly_rent: int = 0
    lease_start: str = ""
    next_due_date: str = ""
    balance: int = 0
    landlord_email: str = ""

    class Config:
        from_attributes = True
