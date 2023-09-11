from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

import app.routers.adoption_router as adoption_router
import app.routers.customer_router as customer_router
import app.routers.pet_router as pet_router
import app.routers.report_router as report_router

app = FastAPI(
    title="Buchi-Backend",
    description="Buchi-Backend",
    version="1",
    contact={
        "name": "Eyasu Tewodros",
        "email": "eyasutew1@gmail.com",
    }
)

app.include_router(adoption_router.router, tags=['Adoptions'])
app.include_router(customer_router.router, tags=['Customers'])
app.include_router(pet_router.router, tags=['Pets'])
app.include_router(report_router.router, tags=['Reports'])
app.mount("/public", StaticFiles(directory="public"), name="static")