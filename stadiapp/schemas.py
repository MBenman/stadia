from ninja import Schema
from datetime import date
from pydantic import validator, Field
from typing import Optional

class StadiumSchema(Schema):
    id: int
    name: str
    sport: str
    city: str
    state: str
    capacity: Optional[int] = None

class CreateStadiumSchema(Schema):
    name: str = Field(..., min_length=1, max_length=100, description="Stadium name cannot be empty")
    sport: str = Field(..., min_length=1, max_length=100)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    capacity: Optional[int] = Field(default=0, ge=0, description="Capacity must be non-negative")
    
   
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Stadium name cannot be empty')
        return v.strip()
   
    @validator('capacity')
    def capacity_must_be_realistic(cls, v):
        if v is None:  # Allow None values
            return 0  # Convert None to 0, or return v to keep as None
        if v < 0:
            raise ValueError('Capacity cannot be negative')
        if v > 200000:  # upper limit
            raise ValueError('Capacity seems unrealistic (max 200,000)')
        return v  

