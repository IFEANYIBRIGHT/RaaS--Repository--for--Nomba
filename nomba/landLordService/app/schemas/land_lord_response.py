from pydantic import BaseModel


class LandLordResponse(BaseModel):
    id: str
    name: str
    phone_number: str
    email: str
    residential_number: str
    property_address: str
    certificate_of_occupancy: str
    plot_number: str