from pydantic import BaseModel
from enum import Enum


class Status(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class UpdateStatusRequest(BaseModel):
    status: Status
