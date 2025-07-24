from ninja import NinjaAPI
from .models import Stadium
from .schemas import StadiumSchema, CreateStadiumSchema
from django.shortcuts import get_object_or_404 

api = NinjaAPI()

@api.get("/stadiums", response=list[StadiumSchema])
def list_stadiums(request):
    stadiums =Stadium.objects.all()
    return stadiums

@api.post("/stadiums", response=StadiumSchema)
def create_stadium(request, payload: CreateStadiumSchema):
    stadium = Stadium.objects.create(**payload.dict())
    return stadium

@api.get("stadiums/{stadium_id}", response=StadiumSchema)
def get_stadium(request, stadium_id: int):
    stadium = get_object_or_404(Stadium, id=stadium_id)
    return stadium

@api.put("stadiums/{stadium_id}", response=StadiumSchema)
def update_stadium(request, stadium_id: int, payload: CreateStadiumSchema):
    stadium = get_object_or_404(Stadium, id=stadium_id)
    for attr, value in payload.dict().items():
        setattr(stadium, attr, value)
    stadium.save()
    return stadium

@api.delete("stadiums/{stadium_id}")
def delete_stadium(request, stadium_id: int):
    stadium = get_object_or_404(Stadium, id=stadium_id)
    stadium.delete()
    return {"success": True}

