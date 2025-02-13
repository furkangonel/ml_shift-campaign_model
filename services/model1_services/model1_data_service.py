from datetime import datetime
from models.models_1.processed_data_model1 import ProcessedData_Model1, ProcessedDataList_Model1
from models.models_1.incoming_data_model1 import IncomingData_Model1
from typing import List
from database.connection import db
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import math


async def process_incoming_data_m1(data_list: List["IncomingData_Model1"]) -> dict:
    """
    Gelen veri listesi işlenir ve işlenmiş veriler veritabanına kaydedilir.

    Args:
        data_list (list): İşlenecek veri listesi.
    Returns: 
        list: İşlenmiş verilerin listesi.
    """

    processed_data_list = ProcessedDataList_Model1(processed_data=[])

    weekly_sales_values = [data.weekly_sales for data in data_list]
    density_level_values = [data.density_level for data in data_list]

    scaler = MinMaxScaler()
    scaled_weekly_sales = scaler.fit_transform(np.array(weekly_sales_values).reshape(-1, 1))
    scaled_density_level = scaler.fit_transform(np.array(density_level_values).reshape(-1, 1))

    # Her bir veriyi işleme
    for i, data in enumerate(data_list):
        normalized_weekly_sales = scaled_weekly_sales[i][0]
        normalized_density_level = scaled_density_level[i][0]

        # Work type sınıflandırılması
        work_type = work_type_process(data)

        # Day_Off_* işaretleme
        day_off_flags = generate_day_off_flags(data.day_off_preferred)

        # Preferred Shift Flags
        preferred_shift_flags = generate_preferred_shift_flags(data.preferred_shift)

        required_employees = max(2, math.floor(len(weekly_sales_values) / 7))


        # İşlenmiş veri modeli
        processed_data = ProcessedData_Model1(
            Date=data.date,  # Tarihi datetime olarak kaydediyoruz
            Name=data.name,
            Density_Level=normalized_density_level,
            Work_Type_x=work_type,
            Preferred_Morning=preferred_shift_flags[0],
            Preferred_Evening=preferred_shift_flags[1],
            Weekly_Sales=normalized_weekly_sales,
            Day_Off_Monday=day_off_flags[0],
            Day_Off_Tuesday=day_off_flags[1],
            Day_Off_Wednesday=day_off_flags[2],
            Day_Off_Thursday=day_off_flags[3],
            Day_Off_Friday=day_off_flags[4],
            Day_Off_Saturday=day_off_flags[5],
            Day_Off_Sunday=day_off_flags[6],
            Required_Employees=required_employees
        )

        # İşlenmiş veriyi listeye ekleme
        processed_data_list.processed_data.append(processed_data)

    # Veritabanına kaydetme
    document_to_save = processed_data_list.dict()
    await db.processed_data_collection.insert_one(document_to_save)

    return processed_data_list


def work_type_process(data):
    """Work type değerini sınıflandırır."""
    if data.work_type == "Part-time":
        return 0
    else:
        return 1


def generate_day_off_flags(day_off_preferred):
    """Haftanın 7 günü için day_off_preferred'e göre bayrakları oluşturur."""
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    flags = [1 if day in day_off_preferred else 0 for day in days_of_week]
    return flags


def generate_preferred_shift_flags(preferred_shift):
    """Tercih edilen vardiya saatlerini preferred_shift'e göre bayrakları oluşturur."""
    morning_flag = 1 if "Morning" in preferred_shift else 0
    evening_flag = 1 if "Evening" in preferred_shift else 0
    return [morning_flag, evening_flag]