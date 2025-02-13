from pydantic import BaseModel
from typing import List
from datetime import datetime



class ProcessedData_Model1(BaseModel):
    Date: datetime
    Name: str
    Density_Level: float
    Work_Type_x: int
    Preferred_Morning: int
    Preferred_Evening: int
    Weekly_Sales: float
    Day_Off_Monday: int	
    Day_Off_Tuesday: int	
    Day_Off_Wednesday: int	
    Day_Off_Thursday: int	
    Day_Off_Friday: int	
    Day_Off_Saturday: int	
    Day_Off_Sunday: int	
    Required_Employees: int


class ProcessedDataList_Model1(BaseModel):
    processed_data: List[ProcessedData_Model1]