from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class SheduleRequest(BaseModel):
    id: Optional[str]
    density_level: int
    work_type: str
    preferred_shift: str
    weekly_sales: float
    day_off_preferred: List[str]
    required_employees: int
    worked: int
    

    