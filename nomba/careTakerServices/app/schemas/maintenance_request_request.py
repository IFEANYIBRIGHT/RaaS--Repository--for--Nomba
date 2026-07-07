from pydantic import BaseModel
from enum import Enum


class Priority(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class MaintenanceRequestRequest(BaseModel):
    title: str
    priority: Priority
    unit: str
    property_name: str
    care_taker_id: str
