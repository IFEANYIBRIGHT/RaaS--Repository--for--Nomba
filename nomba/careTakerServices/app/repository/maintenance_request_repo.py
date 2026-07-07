from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from bson.errors import InvalidId


class MaintenanceRequestRepo:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_request(self, request_data: dict) -> dict:
        result = await self.collection.insert_one(request_data)
        request_data["id"] = str(result.inserted_id)
        request_data.pop("_id", None)
        return request_data

    async def get_all_requests(self) -> list[dict]:
        requests = []
        async for doc in self.collection.find({}).sort("reported_date", -1):
            doc["id"] = str(doc.pop("_id"))
            requests.append(doc)
        return requests

    async def update_status(self, request_id: str, status: str) -> bool:
        try:
            oid = ObjectId(request_id)
        except InvalidId:
            return False
        result = await self.collection.update_one(
            {"_id": oid},
            {"$set": {"status": status}},
        )
        return result.modified_count > 0

    async def count_by_status(self, status: str) -> int:
        return await self.collection.count_documents({"status": status})
