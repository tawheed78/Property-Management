from pydantic import BaseModel

class PropertyCreate(BaseModel):
    location: str
    price: float
    property_type: str
    description: str
    amenities: list[str]

class Property(PropertyCreate):
    pass