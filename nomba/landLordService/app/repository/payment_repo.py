from motor.motor_asyncio import AsyncIOMotorCollection


class PaymentRepo:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_payment(self, payment: dict) -> None:
        await self.collection.insert_one(payment)

    async def get_by_reference(self, reference: str) -> dict | None:
        return await self.collection.find_one({"reference": reference})