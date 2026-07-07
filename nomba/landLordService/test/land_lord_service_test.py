import unittest
from datetime import datetime
from unittest.mock import AsyncMock

from nomba.landLordService.app.enums.landUseType import LandUseType
from nomba.landLordService.app.models.land_lord import LandLord
from nomba.tenantServices.app.models.tenants import Tenants
from nomba.landLordService.app.services.land_lord_services import LandLordService


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.land_lord_repository = AsyncMock()
        self.tenants_repo = AsyncMock()
        self.service = LandLordService(self.land_lord_repository, self.tenants_repo)

        self.land_lord = LandLord(
            "Bright", "Bright","12345678","brightifeanyi799@gmail.com","08131913381","312 johnson st","910 inec street", LandUseType.RESIDENTIAL,"certificate",122 )

        self.tenants = Tenants(
            "mock-id", "Bright", "081412345","tenant@gmail.com","123445675","flat 5",  datetime.now())

    async def test_register_land_lord_(self):
        self.land_lord_repository.save_land_lord.return_value = "Property Registered Successfully"
        result = await self.service.register_property(self.land_lord)
        self.assertIsNotNone(result)

    async def test_add_tenant(self):
        self.tenants_repo.create_tenant.return_value = self.tenants
        result = await self.service.add_a_tenant(self.tenants)
        self.assertTrue(result)
        self.tenants_repo.create_tenant.assert_called_once()

    async def test_get_a_tenant(self):
        self.tenants_repo.get_tenant_by_id.return_value = self.tenants
        result = await self.service.get_a_tenant("mock-id")
        self.assertEqual(self.tenants, result)

    async def test_get_all_tenants(self):
        self.tenants_repo.count_tenants.return_value = 4
        result = await self.service.number_of_tenants()
        self.assertEqual(4, result)

    async def test_delete_a_tenant(self):
        self.tenants_repo.delete_tenant.return_value = None
        self.tenants_repo.count_tenants.return_value = 1
        await self.service.delete_a_tenant("mock-id")
        result = await self.service.number_of_tenants()
        self.assertEqual(1, result)


if __name__ == '__main__':
    unittest.main()