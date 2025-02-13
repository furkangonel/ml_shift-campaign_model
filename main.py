from fastapi import FastAPI
from routers.schedule_router import router as schedule_router
from routers.data_router import router as data_router
from database.connection import connect_to_mongo, close_mongo_connection

app = FastAPI()

app.include_router(schedule_router)
app.include_router(data_router)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

@app.get("/")
async def root():
    return {"message": "Welcome to the *Cafe AI Model's* API"}