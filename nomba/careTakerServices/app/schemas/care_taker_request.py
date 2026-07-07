from pydantic import BaseModel, Field


class CareTakerRequest(BaseModel):
    name: str
    phone_number: str = Field(min_length=11, max_length=11)
    care_taker_email: str
    password: str = Field(min_length=11, max_length=11)
    flat_no: str
