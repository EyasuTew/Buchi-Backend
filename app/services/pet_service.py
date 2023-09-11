from dotenv import load_dotenv
from fastapi import (APIRouter, File, Form, HTTPException, Query,
                     UploadFile)
from app.services.pet_finder_service import get_petfinder_results
from ..database import pet_collection
from ..schemas.pet_schema import PetData
import uuid
import shutil
load_dotenv()
async def create_pet(
    name: str = Form(),
    pet_type: str = Form(),
    good_with_children: bool = Form(),
    age: str = Form(),
    gender: str = Form(),
    size: str = Form(),
    photos: list[UploadFile] = File(...),
):

    # Validate the schemas
    if not name:
        raise HTTPException(status_code=400, detail="Pet name cannot be empty")
    if not pet_type:
        raise HTTPException(status_code=400, detail="Pet type cannot be empty")
    if not age:
        raise HTTPException(status_code=400, detail="Pet age range cannot be empty")
    if not gender:
        raise HTTPException(status_code=400, detail="Pet gender cannot be empty")
    if not size:
        raise HTTPException(status_code=400, detail="Pet size cannot be empty")
    if not photos:
        raise HTTPException(status_code=400, detail="Pet photo cannot be empty")

    photo_urls = []
    for photo in photos:
        photo_url = "public/"+uuid.uuid1().__str__()+"."+photo.filename.split(".")[1] #photo.content_type
        with open(photo_url, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        photo_url= "http://localhost:8000/"+photo_url
        photo_urls.append(photo_url)

    pet = PetData(name = name, photos = photo_urls, pet_type = pet_type, good_with_children = good_with_children,
                  age = age, gender = gender, size = size, source="local")

    result = pet_collection.insert_one(pet.__dict__)
    _id = result.inserted_id
    # return {**pet.__dict__, "_id": str(_id)}
    return {"status": "success", "petId": str(_id)}

async def search_pets(
    pet_type: str | None = None,
    age: list[str] | None = Query(None),
    size: list[str] | None = Query(None),
    gender: list[str] | None = Query(None),
    good_with_children: bool | None = None,
    limit: int = 0,
):
    # Validate the age range
    if age:
        for a in age:
            if a not in ["baby", "young", "adult", "senior", "Baby", "Young", "Adult", "Senior"]:
                raise HTTPException(status_code=400, detail="Invalid pet age range")

    # Validate the size range
    if size:
        for s in size:
            if s not in ["small", "medium", "large", "Small", "Medium", "Large"]:
                raise HTTPException(status_code=400, detail="Invalid pet size range")

    # Validate the gender range
    if gender:
        for g in gender:
            if g not in ["male", "female", "Male", "Female"]:
                raise HTTPException(status_code=400, detail="Invalid pet gender range")
    # Query the database for the pets
    query_local = {}
    query_pet_finder = {}
    if pet_type:
        query_local["type"] = pet_type.lower()
        query_pet_finder["type"] = pet_type.lower()
    if age:
        query_local["age"] = {"$in": [a.lower() for a in age]}
        query_pet_finder["age"] = [a.lower() for a in age]
    if size:
        query_local["size"] = {"$in": [s.lower() for s in size]}
        query_pet_finder["size"] = [s.lower() for s in size]
    if gender:
        query_local["gender"] = {"$in": [g.lower() for g in gender]}
        query_pet_finder["gender"] = [g.lower() for g in gender]
    if good_with_children is not None:
        query_local["good_with_children"] = good_with_children
        query_pet_finder["good_with_children"] = good_with_children

    local_result = pets_serializer(pet_collection.find(query_local).limit(limit))
    if(len(local_result)>=limit):
        return local_result
    else:
        remaining = limit - len(local_result)
        query_local["limit"] = remaining
        if "pet_type" in query_local:
            query_local["type"] = query_local["pet_type"]
            del query_local["pet_type"]

        petfinder_results = await get_petfinder_results(query_pet_finder)
        return {"status": "success", "pets": local_result+petfinder_results}

def pet_serializer(pet)->dict:
    return {
        "pet_id": str(pet["_id"]),
        "source": pet["source"],
        "size": pet["size"],
        "name": pet["name"],
        "type": pet["pet_type"],
        "age": pet["age"],
        "gender": pet["gender"],
        "good_with_children": pet["good_with_children"],
        "photos": pet["photos"],
    }
def pets_serializer(pets)->list:
    return [pet_serializer(pet) for pet in pets]
