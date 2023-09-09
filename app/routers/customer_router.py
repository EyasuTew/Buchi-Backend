from fastapi import APIRouter
from app.schemas.customer_schema import CustomerRequest, CustomerResponse
import app.services.customer_service as customer_service

router = APIRouter()


@router.post("/api/v1/customers")
async def create_customer(customer: CustomerRequest):
    return await customer_service.create_customer(customer)