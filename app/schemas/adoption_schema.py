from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class AdoptionRequest(BaseModel):
    customer_id: str
    pet_id: str
    adoption_date: Optional[datetime] = datetime.now()