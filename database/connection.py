from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv


load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    database = None
    processed_data_collection = None
    shift_schedule_collection = None
    campaign_processed_collection = None
    campaign_model_collection = None


db = Database()


async def connect_to_mongo():
    """
    MongoDB bağlantısını başlatır ve gerekli koleksiyonları tanımlar.
    """
    db.client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db.database = db.client.get_database(os.getenv("MONGO_DB_NAME"))
    db.processed_data_collection = db.database["processed_data_collection"]
    db.shift_schedule_collection = db.database["shift_schedule_collection"]
    db.campaign_processed_collection = db.database["campaign_processed_collection"]
    db.campaign_model_collection = db.database["campaign_model_collection"]

async def close_mongo_connection():
    """
    MongoDB bağlantısını kapatır.
    """
    db.client.close()