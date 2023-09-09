from pydantic import BaseModel


class CustomerRequest(BaseModel):
    name: str
    phone_number: str


class CustomerResponse(BaseModel):
    id: str
    name: str
    phone_number: str
