from pydantic import BaseModel


class LocationInfo(BaseModel):
    zip_code: int
    city: str
    street: str
    house_number: int
    yearly_kwh_consumption: int
