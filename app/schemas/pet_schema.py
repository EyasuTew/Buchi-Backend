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
    photos: list