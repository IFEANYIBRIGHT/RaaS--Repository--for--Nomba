from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "rentflow_landlord_db")

client: AsyncIOMotorClient = None
database: AsyncIOMotorDatabase = None


async def connect_to_mongo():
    global client, database
    client = AsyncIOMotorClient(MONGO_URI)
    database = client[DB_NAME]


async def close_mongo_connection():
    global client
    if client:
        client.close()


def get_database() -> AsyncIOMotorDatabase:
    return database
