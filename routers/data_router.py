from fastapi import APIRouter, HTTPException
from typing import List
from models.models_1.incoming_data_model1 import IncomingData_Model1
from services.model1_services.model1_data_service import process_incoming_data_m1
from models.models_2.incoming_data_model2 import IncomingData_Model2
from models.models_2.processed_data_model2 import ProcessedDataList_Model2
from services.model2_services.model2_data_service import process_incoming_data_m2



router = APIRouter(prefix="/data", tags=["Data"])


@router.post("/process-shift")
async def process_data(data: List[IncomingData_Model1]):
    result = await process_incoming_data_m1([item.dict() for item in data])
    return {"message": "Data processed successfully", "result": result}



@router.post("/process-campaign", response_model=ProcessedDataList_Model2, summary="Process campaign data")
async def process_data_campaign(data: List[IncomingData_Model2]) -> ProcessedDataList_Model2:
    """
    Processes incoming campaign data using FP-Growth algorithm.

    Args:
        data: A list of campaign data items to process.

    Returns:
        A `ProcessedDataList_Model2` object containing the processed data.

    Raises:
        HTTPException: If any error occurs during processing.
    """

    '''
        try:
        # İşleme fonksiyonunu çağır
        result = await process_incoming_data_m2(data)
        return result
    except ValueError as e:
        # Doğrulama hatası durumunda 400 dön
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    except Exception as e:
        # Genel hatalar için 500 dön
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
    
    '''

    
    result = await process_incoming_data_m2(data)
    return result