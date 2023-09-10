from datetime import datetime, date
from typing import Optional

from bson import ObjectId
# from mongoengine import (ValidationError, DateTimeField)
from pydantic import BaseModel, validator


# def validate_object_id(value):
#     if not ObjectId.is_valid(value):
#         raise ValidationError("Invalid ObjectId")
#     return ObjectId(value)


class AdoptionRequest(BaseModel):

    customer_id: str

    pet_id: str

    adoption_date: Optional[datetime] = date.today()#= datetime.datetime.now() #DateTimeField(default=datetime.datetime.utcnow())


    # @validator('customer_id')
    # def validate_customer_id(cls, value):
    #     return validate_object_id(value)
    #
    # @validator('pet_id')
    # def validate_pet_id(cls, value):
    #     return validate_object_id(value)
