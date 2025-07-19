from ninja import Schema
from datetime import date

class StadiumSchema(Schema):
    id: int
    name: str
    sport: str
    city: str
    state: str
    capacity: int

class CreateStadiumSchema(Schema):
    name: str
    sport: str
    city: str
    state: str
    capacity: int

