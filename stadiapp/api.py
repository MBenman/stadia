from ninja import NinjaAPI, 
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


