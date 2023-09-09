from typing import Optional

from fastapi import APIRouter

import app.services.report_service as report_service
from datetime import date
router = APIRouter()

@router.get("/api/v1/generateReport")
async def generate_report(fromDate: Optional[date] = None, toDate: Optional[date] = None):
    return await report_service.generate_report(fromDate, toDate)