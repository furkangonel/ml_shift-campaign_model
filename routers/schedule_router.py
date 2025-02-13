import tempfile
from fastapi import APIRouter
from typing import List
from fastapi.responses import FileResponse
from models.models_1.processed_data_model1 import ProcessedDataList_Model1
from models.models_1.incoming_data_model1 import IncomingData_Model1
from services.model1_services.model1_service import predict_from_model_m1, run_shift_planning, create_pdf_from_table, create_table_and_store
from services.model1_services.model1_data_service import process_incoming_data_m1
from models.models_2.processed_data_model2 import ProcessedDataList_Model2
from models.models_2.incoming_data_model2 import IncomingData_Model2
from services.model2_services.model2_data_service import process_incoming_data_m2
from services.model2_services.model2_services import predict_from_model_m2
from services.model2_services.model2_services import process_campaign_predictions



router = APIRouter(prefix="/schedule", tags=["Schedule"])


@router.post("/predict-shift", response_class=FileResponse)
async def predict_schedule(data: List[IncomingData_Model1]):
    """
    Verilen özelliklere göre modelden tahmin alır.

    Args:
        data (List[dict]): İşlenecek IncomingData listesi.
    Returns:
        dict: Modelden alınan tahminler.
    """

    # Gelen veriler işlenir
    processed_data_list = await process_incoming_data_m1(data)
    
    # İşlenmiş verilerle tahmin alınır
    '''
    predictions = predict_from_model(processed_data_list)
    await run_shift_planning(processed_data_list, data)
    '''
    # Tahminler alınır ve PDF oluşturulur
    predictions = predict_from_model_m1(processed_data_list)
    df = await create_table_and_store(predictions, data)

    pdf_file_name = "Shift_Table.pdf"
    pdf_path = "/Users/furkangonel/Desktop/tmp/Shift_Table.pdf"
    pdf_path = f"/tmp/{pdf_file_name}"  # Geçici bir dizine kaydediyoruz
    create_pdf_from_table(df, pdf_path)
    
    # PDF'yi istemciye gönder
    return FileResponse(
        path=pdf_path,
        filename=pdf_file_name,
        media_type="application/pdf"
    )
    
    


@router.post("/predict-campaign", response_class=FileResponse)
async def predict_campaign(data: List[IncomingData_Model2]):
    """
    Verilen özelliklere göre kampanya tahmini alır ve PDF oluşturur.

    Args:
        data (List[IncomingData_Model2]): İşlenecek IncomingData listesi.
    Returns:
        FileResponse: Kampanya tahmini için oluşturulan PDF dosyası.
    """
    # Geçici bir dosya oluştur
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        # Kampanya tahmin sürecini çalıştır ve PDF oluştur
        await process_campaign_predictions(data, temp_pdf.name)
        temp_pdf_path = temp_pdf.name

    # PDF'yi istemciye gönder
    return FileResponse(
        path=temp_pdf_path,
        filename="Campaigns.pdf",
        media_type="application/pdf"
    )

    

