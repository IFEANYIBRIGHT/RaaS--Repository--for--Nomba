from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from nomba.tenantServices.app.models.tenants import Tenants


class TenantsRepo:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get_tenant_by_id(self, tenant_id: str) -> Tenants:
        return await self.collection.find_one({"_id": ObjectId(tenant_id)})

    async def get_tenant_by_identifier(self, identifier: str):
        return await self.collection.find_one(
            {"$or": [{"tenant_email": identifier}, {"phone_number": identifier}]}
        )

    async def update_password(self, identifier: str, hashed_password: str) -> bool:
        result = await self.collection.update_one(
            {"$or": [{"tenant_email": identifier}, {"phone_number": identifier}]},
            {"$set": {"password": hashed_password}},
        )
        return result.matched_count > 0
    async def update_tenant(self, tenant_id: str, update_data: dict) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(tenant_id)},
            {"$set": update_data},
        )
        return result.matched_count > 0