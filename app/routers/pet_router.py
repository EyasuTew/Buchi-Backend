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
    # user: str = Depends(get_current_user),
    # file: UploadFile = File(...),
    # pet: PetData
):

    return await per_service.create_pet(name, pet_type, good_with_children, age, gender, size, photos)
    # # Validate the schemas
    # if not name:
    #     raise HTTPException(status_code=400, detail="Pet name cannot be empty")
    # if not type:
    #     raise HTTPException(status_code=400, detail="Pet type cannot be empty")
    # if not age:
    #     raise HTTPException(status_code=400, detail="Pet age range cannot be empty")
    # if not gender:
    #     raise HTTPException(status_code=400, detail="Pet gender cannot be empty")
    # if not size:
    #     raise HTTPException(status_code=400, detail="Pet size cannot be empty")
    # if not photos:
    #     raise HTTPException(status_code=400, detail="Pet photo cannot be empty")
    #
    # img_url = []
    # for img in photos:
    #     # upload the pet's photo to cloudinary and get its URL
    #     f = upload(img.file)
    #     img_url.append(f.get("url"))
    #
    # # insert the pet into the database and get its id
    # pet = Pet(
    #     name=name,
    #     age=age.lower(),
    #     size=size.lower(),
    #     photo_url=img_url,
    #     type=pet_type.lower(),
    #     gender=gender.lower(),
    #     good_with_children=good_with_children,
    # )
    # pet.save()
    #
    # return {"status": "success", "id": pet.pk}


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
    # # Validate the age range
    # if age:
    #     for a in age:
    #         if a not in ["baby", "young", "adult", "senior"]:
    #             raise HTTPException(status_code=400, detail="Invalid pet age range")
    #
    # # Validate the size range
    # if size:
    #     for s in size:
    #         if s not in ["small", "medium", "large"]:
    #             raise HTTPException(status_code=400, detail="Invalid pet size range")
    #
    # # Validate the gender range
    # if gender:
    #     for g in gender:
    #         if g not in ["male", "female"]:
    #             raise HTTPException(status_code=400, detail="Invalid pet gender range")
    # # Query the database for the pets
    # query = {}
    # if pet_type:
    #     query["type__iexact"] = pet_type.lower()
    # if age:
    #     query["age__in"] = [a.lower() for a in age]
    # if size:
    #     query["size__in"] = [s.lower() for s in size]
    # if gender:
    #     query["gender__in"] = [g.lower() for g in gender]
    # if good_with_children:
    #     query["good_with_children"] = good_with_children
    #
    # results = Pet.objects.filter(**query)[:limit]
    #
    # # Process the results from the API
    # params = {
    #     "pet_type": pet_type,
    #     "age": ",".join(age),
    #     "size": ",".join(size),
    #     "gender": ",".join(gender),
    #     "good_with_children": good_with_children,
    # }
    # petfinder_results = await get_petfinder_results(params)
    #
    # combined_results = [r.to_mongo().to_dict() for r in results] + petfinder_results
    #
    # return {"status": "success", "pets": combined_results}
