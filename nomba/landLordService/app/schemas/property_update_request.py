from pydantic import BaseModel
from typing import Optional
from nomba.landLordService.app.enums.landUseType import LandUseType


class PropertyUpdateRequest(BaseModel):
    property_address: Optional[str] = None
    land_use_type: Optional[LandUseType] = None
    certificate_of_occupancy: Optional[str] = None
    plot_number: Optional[str] = None