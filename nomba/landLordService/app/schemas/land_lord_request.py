from pydantic import BaseModel, Field, EmailStr
from nomba.landLordService.app.enums.landUseType import LandUseType


class LandLordRequest(BaseModel):

    name: str
    password: str = Field(min_length=8, max_length=19)
    phone_number: str = Field(min_length=11, max_length=11)
    email: EmailStr
    residential_number: str = ""
    property_address: str = ""
    certificate_of_occupancy: str = ""
    plot_number: str = ""
    land_use_type: LandUseType = LandUseType.RESIDENTIAL
