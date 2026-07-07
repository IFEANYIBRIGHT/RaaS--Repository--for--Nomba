from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from bson.errors import InvalidId
from nomba.careTakerServices.app.models.care_taker import CareTaker


class CareTakerRepo:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_care_taker(self, care_taker_data: dict) -> str:
        result = await self.collection.insert_one(care_taker_data)
        return str(result.inserted_id)

    async def get_care_taker_by_id(self, care_taker_id: str) -> dict | None:
        try:
            oid = ObjectId(care_taker_id)
        except InvalidId:
            return None
        return await self.collection.find_one({"_id": oid})

    async def get_care_taker_by_identifier(self, identifier: str) -> dict | None:
        return await self.collection.find_one(
            {"$or": [{"care_taker_email": identifier}, {"phone_number": identifier}]}
        )

    async def update_password(self, identifier: str, hashed_password: str) -> bool:
        result = await self.collection.update_one(
            {"$or": [{"care_taker_email": identifier}, {"phone_number": identifier}]},
            {"$set": {"password": hashed_password}},
        )
        return result.matched_count > 0
