from pydantic import BaseModel, Field


class CareTakerResponse(BaseModel):
    id: str
    name: str
    phone_number: str = Field(min_length=11, max_length=11)
    care_taker_email: str
    flat_no: str
