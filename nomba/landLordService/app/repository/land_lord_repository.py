from motor.motor_asyncio import AsyncIOMotorCollection
from nomba.landLordService.app.models.land_lord import LandLord
from bson import ObjectId


class LandLordRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def save_land_lord(self, land_lord: LandLord):
        document = {
            "land_lord_name": land_lord.land_lord_name,
            "password": land_lord.password,
            "email": land_lord.email,
            "phone_number": land_lord.phone_number,
            "residential_address": land_lord.residential_address,
            "property_address": land_lord.property_address,
            "land_use_type": land_lord.land_use_type.value,
            "certificate_of_occupancy": land_lord.certificate_of_occupancy,
            "plot_number": land_lord.plot_number,
            "plot_number": land_lord.plot_number,
            "virtual_account_number": land_lord.virtual_account_number,
        }
        result = await self.collection.insert_one(document)
        return str(result.inserted_id)
    
    async def get_land_lord(self):
        return await self.collection.find()

    async def update_land_lord_property(self, land_lord_id: str, updates: dict):
        result = await self.collection.update_one(
            {"_id": ObjectId(land_lord_id)},
            {"$set": updates}
        )
        return result.modified_count > 0

    async def delete_land_lord(self, land_lord: LandLord):
        return await self.collection.delete_one(land_lord)

    async def get_all_land_lords(self):
        return await self.collection.find()

    def get_all_land_lords_count(self):
        return self.collection.count()


    async def get_all_land_lords_by_id(self, land_lords_id: str):
        return await self.collection.find_one({"_id": ObjectId(land_lords_id)})

    def get_all_land_lords_by_name(self, land_lords_name: str):
        return self.collection.find({"name":land_lords_name}).limit(1)

    def get_all_land_lords_by_address(self, land_lords_address: str):
        return self.collection.find({"address":land_lords_address}).limit(1)

    def get_all_land_lords_by_phone(self, land_lords_phone: str):
        return self.collection.find({"phone":land_lords_phone}).limit(1)

    def update_land_lord(self, land_lord: LandLord):
        return self.collection.update_one(land_lord,{"$set":land_lord})

    def delete_land_lord_by_id(self, land_lords_id: int):
        return self.collection.delete_one(land_lords_id)



    async def get_land_lord_by_identifier(self, identifier: str):
        return await self.collection.find_one(
            {"$or": [{"email": identifier}, {"phone_number": identifier}]}
        )
    async def update_virtual_account_number(self, identifier: str, virtual_account_number: str, bank_name: str = "", account_name: str = "") -> bool:
        update_fields = {"virtual_account_number": virtual_account_number}
        if bank_name:
            update_fields["bank_name"] = bank_name
        if account_name:
            update_fields["account_name"] = account_name
        result = await self.collection.update_one(
            {"$or": [{"email": identifier}, {"phone_number": identifier}]},
            {"$set": update_fields},
        )
        return result.matched_count > 0
    async def get_virtual_account_number_by_identifier(self, identifier: str):
        land_lord = await self.collection.find_one(
            {"$or": [{"email": identifier}, {"phone_number": identifier}]},
            {"virtual_account_number": 1, "bank_name": 1, "account_name": 1},
        )
        if not land_lord:
            return None
        return {
            "virtual_account_number": land_lord.get("virtual_account_number"),
            "bank_name": land_lord.get("bank_name", ""),
            "account_name": land_lord.get("account_name", ""),
        }
