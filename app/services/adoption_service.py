from datetime import datetime, date
from typing import Optional

from bson import ObjectId
from fastapi import HTTPException

from app.entities.adoptions import Adoption
from app.schemas.adoption_schema import AdoptionRequest
from app.entities.customers import Customer
# from app.entities.pets import Pet
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
    adoption_dict = {** adoption.__dict__}
    return {'customer_id': str(adoption_dict['customer_id']), 'pet_id': str(adoption_dict['pet_id']), "_id": str(_id)}
    # return {"status": "success", "adoption_id": result.pk}


async def get_adoptions(fromDate: date ,
                        toDate: date,
                        limit: int = 0):
    # return fromDate
    # set default start and end dates if none are provided
    # if fromDate is None:
    #     fromDate = datetime.date.min
    # if toDate is None:
    #     toDate = datetime.date.max
    # fromDate = datetime.datetime.combine(fromDate, datetime.time.min)
    # toDate = datetime.datetime.combine(toDate, datetime.time.min)

    # retrieve all adoption records within the date range
    # adoptions = Adoption.objects.filter(
    #     adoption_date__gte=fromDate, adoption_date__lte=toDate).select_related()

    query = {}
    if fromDate:
        query["adoption_date"] = {"$gte": datetime(fromDate.year, fromDate.month, fromDate.day, 0, 0, 0)}
    if toDate:
        query["adoption_date"] = {"$lte": datetime(toDate.year, toDate.month, toDate.day, 23, 59, 59)}
    # if limit:
    #     query["age"] = {"$in": [a.lower() for a in age]}

    print("Query")
    print(query)
    res = adoption_collection.find(query).limit(limit)
    print(list(res))

    # format the adoption records for output
    # adoption_list = []
    # for adoption in adoptions:
    #     adopt = {}
    #
    #     adopt['adoption_id'] = adoption.pk
    #     adopt['adoption_date'] = adoption.adoption_date.date()
    #     adopt['customer'] = adoption.customer.to_mongo().to_dict()
    #     adopt['pet'] = adoption.pet.to_mongo().to_dict()
    #     adoption_list.append(adopt)
    #
    # if limit:
    #     adoption_list = adoption_list[:limit]

    return adoptions_serializer(adoption_collection.find(query).limit(limit)) #{"status": "success", "schemas": adoption_list}

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