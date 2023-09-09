import pydantic
from bson.objectid import ObjectId
from dotenv import load_dotenv
from fastapi import (APIRouter, File, Form, Query, UploadFile)
from starlette.staticfiles import StaticFiles

# from routers.users import get_current_user
import app.services.pet_service as per_service
from app.schemas.pet_schema import PetData

# pydantic.Json.ENCODERS_BY_TYPE[ObjectId] = str
load_dotenv()

router = APIRouter()


@router.post("/api/v1/pets")
async def create_pet(
    name: str = Form(),
    pet_type: str = Form(),
    good_with_children: bool = Form(),
    age: str = Form(),
    gender: str = Form(),
    size: str = Form(),
    photos: list[UploadFile] = File(...),
):
    return await per_service.create_pet(name, pet_type, good_with_children, age, gender, size, photos)

@router.get("/api/v1/pets")
async def search_pets(
    pet_type: str | None = None,
    age: list[str] | None = Query(None),
    size: list[str] | None = Query(None),
    gender: list[str] | None = Query(None),
    good_with_children: bool | None = None,
    limit: int = 0,
):
    return await per_service.search_pets(pet_type, age, size, gender, good_with_children, limit)