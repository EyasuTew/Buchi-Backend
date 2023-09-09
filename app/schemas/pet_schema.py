from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile

class PetData(BaseModel):
    source: str
    name: str
    pet_type: str
    age: str
    gender: str
    size: str
    good_with_children: bool | None
    # file: bytes = File(...)
    # photos: list
    photos: list #list[UploadFile] = File(...),


class PetResponse(BaseModel):
    status: str = 'success'
    pets: list[PetData]
