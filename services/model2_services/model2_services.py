import joblib
import os
import numpy as np
import ast
from fpdf import FPDF
from typing import List, Tuple
from models.models_2.processed_data_model2 import ProcessedDataList_Model2
from models.models_2.incoming_data_model2 import IncomingData_Model2
from services.model2_services.model2_data_service import process_incoming_data_m2
from database.connection import db

# Modeli yükleme
model = joblib.load("../Model_API/ai_models/campaign_model_rfc.pkl")


def predict_from_model_m2(processed_data_list: ProcessedDataList_Model2) -> list:
    """
    İşlenmiş verilerle modelden tahmin yapılır ve tahmin sonuçları işlenmiş verilerle birleştirilir.

    Args: 
        processed_data_list (ProcessedDataList_Model2): İşlenmiş veriler.

    Returns:
        list: Tahmin sonuçları ve ilgili işlenmiş verilerin birleştirildiği liste.
    """
    features = [
        [
            float(data.support),
            float(data.confidence),
            float(data.lift),
        ]
        for data in processed_data_list.processedData
    ]

    features = np.array(features)

    # Modelden tahmin al
    predictions = model.predict(features)

    # Tahmin sonuçlarını işlenmiş verilerle birleştir
    data_records = []
    for i, data in enumerate(processed_data_list.processedData):
        data_records.append({
            "Antecedents": data.antecedents,
            "Consequents": data.consequents,
            "Support": float(data.support),
            "Confidence": float(data.confidence),
            "Lift": float(data.lift),
            "Antecedent_Info": data.antecedent_info,
            "Consequent_Info": data.consequent_info,
            "Prediction": int(predictions[i])
        })

    return data_records


def create_campaign_pdf(campaigns: list, file_path: str):
    """
    Kampanya tahmin sonuçlarını PDF olarak oluşturur.

    Args:
        campaigns (list): Kampanya tahminleri.
        file_path (str): PDF'nin kaydedileceği dosya yolu.

    Returns:
        str: Oluşturulan PDF dosyasının yolu.
    """
    output_dir = os.path.dirname(file_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)

    # Unicode destekleyen yazı tipini yükleme
    pdf.add_font("DejaVuSans", "", "../Model_API/fonts/DejaVuSans.ttf", uni=True)

    for campaign in campaigns:
        antecedents = campaign["Antecedents"]
        consequents = campaign["Consequents"]
        confidence = campaign["Confidence"]
        antecedent_info = ast.literal_eval(campaign["Antecedent_Info"])
        consequent_info = ast.literal_eval(campaign["Consequent_Info"])
        prediction = campaign["Prediction"]

        pdf.add_page()

        # Arka plan
        pdf.set_fill_color(243, 198, 55)
        pdf.rect(0, 0, 297, 210, style='F')

        # Başlık
        pdf.set_font("DejaVuSans", size=36)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 20, txt="KAMPANYA", ln=True, align="C")
        pdf.ln(10)

        # Fiyat ve İndirim Detayları
        if prediction == 1:
            pdf.set_font("DejaVuSans", size=40)
            pdf.cell(0, 10, txt=f"{antecedents} alana {consequents} indirimli!", ln=True, align="C")
            pdf.ln(15)
            pdf.cell(0, 10, txt=f"{consequents} İndirimli Fiyat: {consequent_info['Prices'][0]} ₺", ln=True, align="C")
        elif prediction == 2:
            pdf.set_font("DejaVuSans", size=36)
            total_price = antecedent_info['Prices'][0] + consequent_info['Prices'][0]
            discounted_price = total_price * 0.9
            pdf.multi_cell(0, 10, txt=f"{antecedents} ve {consequents} birlikte alınca %10 indirim!", align="C")
            pdf.ln(15)
            pdf.cell(0, 10, txt=f"Toplam: {total_price} ₺", ln=True, align="C")
            pdf.cell(0, 10, txt=f"İndirimli: {discounted_price:.2f} ₺", ln=True, align="C")

    pdf.output(file_path)
    print(f"PDF oluşturuldu: {file_path}")

    return file_path


async def process_campaign_predictions(data: List[IncomingData_Model2], file_path: str) -> Tuple[str, list]:
    """
    Kampanya tahmin sürecini yürütür ve sonuçları döndürür.

    Args:
        data (List[IncomingData_Model2]): İşlenecek veriler.
        file_path (str): PDF'nin kaydedileceği yol.

    Returns:
        Tuple[str, list]: PDF yolu ve tüm tahminler.
    """
    processed_data_list = await process_incoming_data_m2(data)
    predictions = predict_from_model_m2(processed_data_list)

    # Kampanya tahminlerini filtrele (Prediction = 1 veya 2)
    campaign_records = [record for record in predictions if record["Prediction"] in [1, 2]]

    if campaign_records:
        combined_document = {"type": "campaign_predictions", "campaign_predictions": campaign_records}
        existing_doc = await db.campaign_model_collection.find_one({"type": "campaign_predictions"})
        if existing_doc:
            await db.campaign_model_collection.update_one(
                {"type": "campaign_predictions"},
                {"$set": {"campaign_predictions": campaign_records}}
            )
            print("Mevcut JSON güncellendi.")
        else:
            await db.campaign_model_collection.insert_one(combined_document)
            print("Yeni JSON başarıyla MongoDB'ye kaydedildi.")

        create_campaign_pdf(campaign_records, file_path)

    return file_path