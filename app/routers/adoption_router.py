from datetime import datetime, date
from typing import Optional

from fastapi import APIRouter

# from entities.adoptions import AdoptionInput
from app.schemas.adoption_schema import AdoptionRequest
import app.services.adoption_service as adoption_service

router = APIRouter()


@router.post("/api/v1/adoptions")
async def create_adoption(adoption: AdoptionRequest):
    return await adoption_service.create_adoption(adoption)

@router.get("/api/v1/adoptions")
async def get_adoptions(fromDate: Optional[date] = None, toDate: Optional[date] = None, limit: int = 0):
    return await adoption_service.get_adoptions(fromDate, toDate, limit)