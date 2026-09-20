from pydantic import BaseModel
from typing import Optional


class TenantUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    flat_no: Optional[str] = None
    monthly_rent: Optional[int] = None
    lease_start: Optional[str] = None
