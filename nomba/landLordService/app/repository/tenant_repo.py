from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from bson.errors import InvalidId


class TenantsRepo:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_tenant(self, tenant_data: dict) -> dict:
        result = await self.collection.insert_one(tenant_data)
        tenant_data["id"] = str(result.inserted_id)
        tenant_data.pop("_id", None)
        return tenant_data

    async def get_tenant_by_id(self, tenant_id: str) -> dict | None:
        try:
            oid = ObjectId(tenant_id)
        except InvalidId:
            return None

        doc = await self.collection.find_one({"_id": oid})
        if not doc:
            return None

        doc["id"] = str(doc.pop("_id"))
        return doc

    async def delete_tenant(self, tenant_id: str) -> bool:
        try:
            oid = ObjectId(tenant_id)
        except InvalidId:
            return False

        result = await self.collection.delete_one({"_id": oid})
        return result.deleted_count > 0

    async def count_tenants(self) -> int:
        return await self.collection.count_documents({})

    async def get_all_tenants(self) -> list[dict]:
        tenants = []
        async for doc in self.collection.find({}):
            doc["id"] = str(doc.pop("_id"))
            tenants.append(doc)
        return tenants

    async def update_tenant_balance(self, tenant_id: str, amount: int) -> bool:
        try:
            oid = ObjectId(tenant_id)
        except InvalidId:
            return False

        result = await self.collection.update_one(
            {"_id": oid},
            {"$inc": {"balance": -amount}},
        )
        return result.modified_count > 0

    async def update_tenant(self, tenant_id: str, update_data: dict) -> bool:
        try:
            oid = ObjectId(tenant_id)
        except InvalidId:
            return False

        result = await self.collection.update_one(
            {"_id": oid},
            {"$set": update_data},
        )
        return result.modified_count > 0
