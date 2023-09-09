from datetime import datetime, timedelta, date

from fastapi import APIRouter, HTTPException

from app.entities.adoptions import Adoption
from ..database import pet_collection, adoption_collection
from .adoption_service import get_adoptions
router = APIRouter()


async def generate_report(fromDate: date ,
                    toDate: date):
    # try:
    # try:
    #     datetime.strptime(fromDate, "%Y-%m-%d")
    #     datetime.strptime(toDate, "%Y-%m-%d")
    # except ValueError:
    #     raise HTTPException(
    #         status_code=400, detail="Wrong date format. Date must be like this: 2023-02-02")

    adopted_pet_types = {}
    weekly_adoption_requests = {}

    # Convert the date strings to datetime objects
    # from_date = datetime.strptime(fromDate, "%Y-%m-%d")
    # to_date = datetime.strptime(toDate, "%Y-%m-%d") + timedelta(days=1)

    # Query the database for adoptions within the date range
    # adoptions = Adoption.objects.filter(
    #     adoption_date__gte=from_date, adoption_date__lte=to_date).select_related()

    query = {}
    if fromDate:
        query["adoption_date"] = {"$gte": datetime(fromDate.year, fromDate.month, fromDate.day, 0, 0, 0)}
    if toDate:
        query["adoption_date"] = {"$lte": datetime(toDate.year, toDate.month, toDate.day, 23, 59, 59)}
    print("Query")
    print(query)
    adoptions = await get_adoptions(fromDate, toDate, 0)
    for adoption in adoptions:

        adoption_date = adoption.get("adoption_date", None)
        pet_type = adoption.get("pet_type", None)
        pet_type = adoption.get("pet_type", None)
        if pet_type:
            count = adopted_pet_types.get(pet_type, None)
            if count:
                adopted_pet_types[pet_type] = int(count) + 1
            else:
                adopted_pet_types[pet_type] = 1

        print("adoption_date")
        print(adoption_date)
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

    # result=adoption_collection.aggregate( [
    #    {
    #       "$match": query
    #    },
    #    {
    #       "$group": { "_id": "$pet_type", "count": { "$count": {} } }
    #    }
    # ] )

    print("RES")
    print(dict(adopted_pet_types))
    print(dict(weekly_adoption_requests))

    # Calculate the number of adoptions for each pet type
    # for adoption in adoptions:
    #     pet_type = adoption.pet.type
    #     if pet_type in adopted_pet_types:
    #         adopted_pet_types[pet_type] += 1
    #     else:
    #         adopted_pet_types[pet_type] = 1

  # Count adoption requests by week
  #   start_date = from_date - timedelta(days=from_date.weekday())
  #   end_date = to_date + timedelta(days=6-to_date.weekday())
  #   current_date = start_date
  #   while current_date <= end_date:
  #       week_start = current_date.strftime('%Y-%m-%d')
  #       week_end = (current_date + timedelta(days=6)).strftime('%Y-%m-%d')
  #       weekly_adoption_requests[week_start] = 0
  #       for adoption in adoptions:
  #           if week_start <= str(adoption.adoption_date.date()) <= week_end:
  #               weekly_adoption_requests[week_start] += 1
  #       current_date += timedelta(days=7)
  #
  #   report_data = {
  #       'adoptedPetTypes': adopted_pet_types,
  #       'weeklyAdoptionRequests': weekly_adoption_requests
  #   }

    # report = {
    #     'status': 'success',
    #     'schemas': report_data
    # }

    return { "adopted_pet_types" :adopted_pet_types, "weekly_adoption_requests": weekly_adoption_requests }
