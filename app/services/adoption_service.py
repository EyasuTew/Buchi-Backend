from datetime import datetime, date
from bson import ObjectId
from fastapi import HTTPException
from app.schemas.adoption_schema import AdoptionRequest
from ..database import pet_collection, adoption_collection, customer_collection

async def create_adoption(adoption: AdoptionRequest):
    adoption.adoption_date = datetime.datetime.now()
    if not adoption.customer_id:
        raise HTTPException(
            status_code=400, detail='customer id can not be empty.')
    if not adoption.pet_id:
        raise HTTPException(status_code=400, detail="pet id can not be empty.")

    customer = customer_collection.find_one({"_id": ObjectId(adoption.customer_id)})
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    # pet = Pet.get_by_id_or_none(adoption.pet_id)
    pet = pet_collection.find_one({"_id": ObjectId(adoption.pet_id)})
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    adopted = adoption_collection.find({"pet_id":adoption.pet_id})
    if len(list(adopted))>0:
        raise HTTPException(status_code=400, detail="pet is already adopted")
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    result = adoption_collection.insert_one(adoption.__dict__)
    _id = result.inserted_id
    return {"status": "success", "adoption_id": str(_id)}

async def search_adoptions(fromDate: date ,
                        toDate: date,
                        limit: int = 0):
    query = {}
    if fromDate:
        query["adoption_date"] = {"$gte": datetime(fromDate.year, fromDate.month, fromDate.day, 0, 0, 0)}
    if toDate:
        query["adoption_date"] = {"$lte": datetime(toDate.year, toDate.month, toDate.day, 23, 59, 59)}
    return adoptions_serializer(adoption_collection.find(query).limit(limit))


async def get_adoptions(fromDate: date ,
                        toDate: date,
                        limit: int = 0):
    query = {}
    if fromDate:
        query["adoption_date"] = {"$gte": datetime(fromDate.year, fromDate.month, fromDate.day, 0, 0, 0)}
    if toDate:
        query["adoption_date"] = {"$lte": datetime(toDate.year, toDate.month, toDate.day, 23, 59, 59)}
    return {"status": "success", "data": search_adoptions(fromDate, toDate, limit) }

def adoption_serializer(adoption)->dict:
    customer = customer_collection.find_one({"_id": ObjectId(str(adoption["customer_id"]))})
    pet = pet_collection.find_one({"_id": ObjectId(str(adoption["pet_id"]))})
    return {
        "_id": str(adoption["_id"]),
        "customer_id": str(adoption["customer_id"]),
        "pet_id": str(adoption["pet_id"]),
        "adoption_date": adoption.get("adoption_date", None),
        "customer_name": customer.get("name", None),
        "customer_phone": customer.get("phone_number", None),
        "pet_type": pet.get("pet_type", None),
        "gender": pet.get("gender", None),
        "size": pet.get("size", None),
        "age": pet.get("age", None),
        "good_with_children": pet.get("good_with_children", None),
    }
def adoptions_serializer(adoptions)->list:
    return [adoption_serializer(adoption) for adoption in adoptions]