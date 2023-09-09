from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.routers import report_router
import app.routers.adoption_router as adoption_router
import app.routers.customer_router as customer_router
import app.routers.pet_router as pet_router
import app.routers.report_router as report_router

description = """
Buchi Pet finder API helps you to find a pet. 🚀

## pets
You can:
* **Read pets**.
* **Post pets** (_Note: you have to be regesterd to make a post request_).
* **Update pets** (_not implemented_).
* **Delete pets** (_not implemented_).

## adoptions

* **Read adoptions**.
* **Post adoptions** (_Note: you have to be registerd an authenticated to make a post request_).
* **Update adoptions** (_not implemented_).
* **Delete adoptions** (_not implemented_).

## Users

You will be able to:

* **Register user**.
* **Login user** (_you will get a token when you logged in_).
* **Read current user**.

## Report 

* **Read report** (_you can get weekely adoption rate_)
"""

app = FastAPI(
    title="Buchi Pet finder API",
    description=description,
    version="1",
    contact={
        "name": "Abrham Mesfin",
        "email": "abrshtgam@gmail.com",
    }
)

app.include_router(adoption_router.router, tags=['Adoptions'])
app.include_router(customer_router.router, tags=['Customers'])
app.include_router(pet_router.router, tags=['Pets'])
app.include_router(report_router.router, tags=['Reports'])
# app.include_router(users.router, tags=['users'])
app.mount("/public", StaticFiles(directory="public"), name="static")

# app.post(8080)
# app.host(host="0.0.0.0:8080", name="Buchi-Backend", app=app)
# @app.get('/', tags=['home'])
# async def home():
#     return {
#         "docs": "https://buchi-api.onrender.com/docs", #http://127.0.0.1:8000/docs
#         "redoc": "https://buchi-api.onrender.com/redoc" #http://127.0.0.1:8000/redoc
#     }
