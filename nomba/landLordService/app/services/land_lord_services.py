from datetime import datetime
from nomba.landLordService.app.models.land_lord import LandLord
from nomba.tenantServices.app.models.tenants import Tenants
from nomba.careTakerServices.app.models.care_taker import CareTaker
from nomba.landLordService.app.repository.land_lord_repository import LandLordRepository
from nomba.landLordService.app.repository.tenant_repo import TenantsRepo
from nomba.careTakerServices.app.repository.care_taker_repo import CareTakerRepo


class LandLordService:
    def __init__(self, land_lord_repository: LandLordRepository, tenants_repo: TenantsRepo, care_taker_repo: CareTakerRepo = None):
        self.land_lord_repository = land_lord_repository
        self.tenants_repo = tenants_repo
        self.care_taker_repo = care_taker_repo

    async def register_property(self, land_lord: LandLord) -> str:
        land_lord_id = await self.land_lord_repository.save_land_lord(land_lord)
        return {"id": land_lord_id, "message": "Property Registered Successfully"}

    async def add_a_tenant(self, tenant: Tenants, monthly_rent: int = 0, lease_start: str = "", landlord_email: str = ""):
        next_due_date = ""
        if lease_start:
            try:
                start = datetime.strptime(lease_start, "%Y-%m-%d")
                if start.month == 12:
                    next_month = start.replace(year=start.year + 1, month=1)
                else:
                    next_month = start.replace(month=start.month + 1)
                next_due_date = next_month.strftime("%Y-%m-%d")
            except ValueError:
                next_due_date = ""
        tenant_data = {
            "name": tenant.name,
            "phone_number": tenant.phone_number,
            "tenant_email": tenant.tenant_email,
            "password": tenant.password,
            "flat_no": tenant.flat_no,
            "date": tenant.date,
            "monthly_rent": monthly_rent,
            "lease_start": lease_start,
            "next_due_date": next_due_date,
            "balance": 0,
            "landlord_email": landlord_email,
        }
        return await self.tenants_repo.create_tenant(tenant_data)

    async def add_a_caretaker(self, care_taker: CareTaker):
        care_taker_data = {
            "name": care_taker.name,
            "phone_number": care_taker.phone_number,
            "care_taker_email": care_taker.care_taker_email,
            "password": care_taker.password,
            "flat_no": care_taker.flat_no,
            "date": care_taker.date,
        }
        return await self.care_taker_repo.create_care_taker(care_taker_data)

    async def get_land_lord_by_id(self, land_lord_id: str):
        return await self.land_lord_repository.get_all_land_lords_by_id(land_lord_id)

    async def get_a_tenant(self, tenant_id: str) -> Tenants | None:
        return await self.tenants_repo.get_tenant_by_id(tenant_id)

    async def delete_a_tenant(self, tenant_id: str) -> str:
        deleted = await self.tenants_repo.delete_tenant(tenant_id)
        if not deleted:
            return "Tenant not found"
        return "Tenant Deleted Successfully"

    async def login(self, identifier: str, password: str):
        land_lord = await self.land_lord_repository.get_land_lord_by_identifier(identifier)
        if not land_lord:
            return None
        if land_lord.get("password") != password:
            return None
        return land_lord

    async def number_of_tenants(self) -> int:
        return await self.tenants_repo.count_tenants()

    async def get_all_tenants(self):
        return await self.tenants_repo.get_all_tenants()

    async def set_virtual_account_number(self, identifier: str, virtual_account_number: str) -> bool:
        return await self.land_lord_repository.update_virtual_account_number(identifier, virtual_account_number)

    async def get_virtual_account_number(self, identifier: str):
        return await self.land_lord_repository.get_virtual_account_number_by_identifier(identifier)