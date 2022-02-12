from pydantic import BaseModel


class LocationInfo(BaseModel):
    zip_code: int
    city: str
    street: str
    house_number: int
    yearly_kwh_consumption: int

class Prices(BaseModel):
    unit_price: float
    grid_fees: float
    kwh_price: float
    total_price: float
