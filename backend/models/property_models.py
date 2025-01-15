from typing import Optional
from pydantic import BaseModel

class PropertyCreate(BaseModel):
    location: str
    price: float
    property_type: str
    description: Optional[str] = None
    amenities: Optional[list[str]] = None

class Property(PropertyCreate):
    pass