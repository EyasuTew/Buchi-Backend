from fastapi import APIRouter, HTTPException

from app.schemas.customer_schema import CustomerRequest
from ..database import customer_collection

router = APIRouter()

async def create_customer(customer: CustomerRequest):

    if not customer.name:
        raise HTTPException(status_code=400, detail="Name can not be empty.")
    if not customer.phone_number:
        raise HTTPException(
            status_code=400, detail="Phone number can not be empty.")

    res=customer_collection.find({"phone_number":customer.phone_number})
    # print(res)
    # print(list(res))
    # print(len(list(res)))
    if(len(list(res))>0):
        raise HTTPException(status_code=403,
                            detail="Customer with specified number is already registered!")
    result = customer_collection.insert_one(customer.__dict__)
    _id = result.inserted_id
    return  {**customer.__dict__, "_id": str(_id)}