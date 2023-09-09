from pydantic import BaseModel


class WeeklyAdoptedPetsData(BaseModel):
    adoptedPetTypes: dict[str, int]
    weeklyAdoptionRequests: dict[str, int]


class ReportData(BaseModel):
    status: str = 'success'
    data: WeeklyAdoptedPetsData
