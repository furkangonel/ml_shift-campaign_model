from pydantic import BaseModel
from typing import List



class ProcessedData_Model2(BaseModel):
    antecedents: str
    consequents: str
    support: float
    confidence: float
    lift: float
    antecedent_info: str
    consequent_info: str



class ProcessedDataList_Model2(BaseModel):
    processedData: List[ProcessedData_Model2]