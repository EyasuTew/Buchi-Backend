from datetime import datetime, timedelta, date

from fastapi import APIRouter, HTTPException
from .adoption_service import search_adoptions
router = APIRouter()

async def generate_report(fromDate: date ,
                    toDate: date):

    adopted_pet_types = {}
    weekly_adoption_requests = {}

    query = {}
    if fromDate:
        query["adoption_date"] = {"$gte": datetime(fromDate.year, fromDate.month, fromDate.day, 0, 0, 0)}
    if toDate:
        query["adoption_date"] = {"$lte": datetime(toDate.year, toDate.month, toDate.day, 23, 59, 59)}
    adoptions = search_adoptions(fromDate, toDate, 0)
    for adoption in adoptions:

        adoption_date = adoption.get("adoption_date", None)
        pet_type = adoption.get("pet_type", None)
        if pet_type:
            count = adopted_pet_types.get(pet_type, None)
            if count:
                adopted_pet_types[pet_type] = int(count) + 1
            else:
                adopted_pet_types[pet_type] = 1

        if adoption_date:
            my_dt_trunc = date(adoption_date.year,  # Truncate time component
                                        adoption_date.month,
                                        adoption_date.day)
            start_of_week = my_dt_trunc - timedelta(days=my_dt_trunc.weekday())  # timedelta & weekday
            end_of_week = start_of_week + timedelta(days=6)

            # if start_of_week in weekly_adoption_requests:
            count = weekly_adoption_requests.get(start_of_week, None)
            if count:
                weekly_adoption_requests[start_of_week] = int(count) + 1
            else:
                weekly_adoption_requests[start_of_week] = 1

    return { "status" : "success",
             "data" : {
                 "adopted_pet_types" :adopted_pet_types,
                 "weekly_adoption_requests": weekly_adoption_requests
             }
        }
