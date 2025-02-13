from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np
from fpdf import FPDF
import os
import pandas as pd
from models.models_1.processed_data_model1 import ProcessedDataList_Model1
from database.connection import db

model = joblib.load("../Model_API/ai_models/shiftPlanner_model.pkl")


# Işlenmiş data'yi alarak model girdisi haline getirir.
def predict_from_model_m1(processed_data_list: ProcessedDataList_Model1) -> list:
    """
    İşlenmiş verilerle modelden tahmin yapılır.

    Args: 
        processed_data_list (ProcessedDataList): İşlenmiş veriler.
    Returns:
        List: Tahmin sanuçları.
    """

        # Özellikleri numpy array'e çevriyorum
    features = [
        [
            data.Density_Level,
            data.Work_Type_x,
            data.Preferred_Morning,
            data.Preferred_Evening,
            data.Weekly_Sales,
            data.Day_Off_Monday,
            data.Day_Off_Tuesday,
            data.Day_Off_Wednesday,
            data.Day_Off_Thursday,
            data.Day_Off_Friday,
            data.Day_Off_Saturday,
            data.Day_Off_Sunday,
            data.Required_Employees
        ]
        for data in processed_data_list.processed_data
    ]

    features = np.array(features)

    # Modelden tahmin alıyorum
    predictions = model.predict(features)

    return predictions.tolist()


async def create_table_and_store(predictions: list, input_data: list):
    """
    Tahmin sonuçlarına göre bir tablo oluşturur ve tüm günlerin verilerini tek bir JSON olarak MongoDB'ye kaydeder.

    Args:
        predictions (list): Tahmin sonuçlarının listesi.
        input_data (list): Girdi JSON verisi.
    """
    # Tüm günleri tek bir JSON nesnesinde toplamak için yapı oluşturma
    all_shifts = {}

    for i, entry in enumerate(input_data):
        shift = "Calismiyor" if predictions[i] == 0 else "Sabahci" if predictions[i] == 1 else "Aksamci"
        tarih = entry.date

        if tarih not in all_shifts:
            all_shifts[tarih] = []

        all_shifts[tarih].append({
            "Calisan": entry.name,
            "Durum": shift
        })

    # Tüm verileri tek bir JSON nesnesi olarak hazırlama
    combined_document = {
        "VardiyaVerileri": [{"Tarih": tarih, "Vardiyalar": vardiyalar} for tarih, vardiyalar in all_shifts.items()]
    }

    # Mevcut veriyi güncellemek veya yeni bir belge olarak eklemek için işlem
    existing_doc = await db.shift_schedule_collection.find_one({"type": "all_shifts"})
    if existing_doc:
        await db.shift_schedule_collection.update_one(
            {"type": "all_shifts"}, {"$set": {"VardiyaVerileri": combined_document["VardiyaVerileri"]}}
        )
        print("Veri mevcut JSON'a güncellendi.")
    else:
        combined_document["type"] = "all_shifts"
        await db.shift_schedule_collection.insert_one(combined_document)
        print("Yeni JSON MongoDB'ye kaydedildi.")

    # DataFrame oluşturma (isteğe bağlı)
    rows = [{"Tarih": tarih, "Calisan": vardiya["Calisan"], "Durum": vardiya["Durum"]}
            for tarih, vardiyalar in all_shifts.items() for vardiya in vardiyalar]
    df = pd.DataFrame(rows)
    print("Tablo oluşturuldu:")
    print(df)

    return df




def create_pdf_from_table(df: pd.DataFrame, file_path: str):
    """
    Tabloyu PDF olarak oluşturur.

    Args:
        df (pd.DataFrame): Tablo verisi.
        file_name (str): Oluşturulacak PDF dosyasının adı.
    """


    # Dizini oluştur
    output_dir = os.path.dirname(file_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Doğru yazı tipi yükleme
    pdf.add_font("DejaVuSans", "", "../Model_API/fonts/DejaVuSans.ttf", uni=True)

    # Başlık
    pdf.set_font("DejaVuSans", size=16)
    pdf.cell(200, 10, txt="Vardiya Tahmin Sonuçları", ln=True, align="C")
    pdf.ln(10)

    # Tablo başlıkları
    pdf.set_font("DejaVuSans", size=12)
    pdf.cell(70, 10, txt="Tarih", border=1, align="C")
    pdf.cell(70, 10, txt="Calisan", border=1, align="C")
    pdf.cell(50, 10, txt="Durum", border=1, align="C")
    pdf.ln()

    # Tablo verileri
    pdf.set_font("DejaVuSans", size=12)
    for _, row in df.iterrows():
        pdf.cell(70, 10, txt=str(row["Tarih"]), border=1)
        pdf.cell(70, 10, txt=row["Calisan"], border=1)
        pdf.cell(50, 10, txt=row["Durum"], border=1)
        pdf.ln()

    # PDF dosyasını kaydetme
    pdf.output(file_path)
    print(f"{file_path} başarıyla oluşturuldu!")




async def run_shift_planning(processed_data_list: ProcessedDataList_Model1, input_data: list):
    """
    Tüm süreci yürütmek için fonksiyonları bağlar:
    - Tahmin yapar.
    - Tablo oluşturur ve MongoDB'ye kaydeder.
    - PDF oluşturur.

    Args:
        processed_data_list (ProcessedDataList_Model1): İşlenmiş veriler.
        input_data (list): Girdi JSON verisi.
    """
    predictions = predict_from_model_m1(processed_data_list)
    df = await create_table_and_store(predictions, input_data)
    create_pdf_from_table(df)