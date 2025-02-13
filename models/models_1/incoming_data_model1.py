from pydantic import BaseModel
from typing import List
from datetime import datetime


class IncomingData_Model1(BaseModel):
    date: datetime
    name: str
    density_level: float
    work_type: str
    preferred_shift: List[str]
    weekly_sales: float
    day_off_preferred: List[str]
    
    