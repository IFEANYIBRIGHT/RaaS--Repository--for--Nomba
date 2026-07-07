from nomba.tenantServices.app.exception.tenantNotFoundError import TenantNotFoundError
from nomba.tenantServices.app.models.tenants import Tenants
from nomba.tenantServices.app.repository.tenants_repo import TenantsRepo
from nomba.tenantServices.app.utils.security import hash_password, verify_password


class TenantsService:
    def __init__(self, repo: TenantsRepo):
        self.repo = repo

    async def get_my_profile(self, tenant_id: str) -> Tenants:
        tenant = await self.repo.get_tenant_by_id(tenant_id)
        if not tenant:
            raise TenantNotFoundError(tenant_id)
        return tenant

    async def set_password(self, identifier: str, new_password: str) -> bool:
        tenant = await self.repo.get_tenant_by_identifier(identifier)
        if not tenant:
            raise TenantNotFoundError(identifier)
        hashed = hash_password(new_password)
        return await self.repo.update_password(identifier, hashed)

    async def login(self, identifier: str, password: str):
        tenant = await self.repo.get_tenant_by_identifier(identifier)
        if not tenant:
            return None
        stored_password = tenant.get("password")
        if not stored_password:
            return None
        if not verify_password(password, stored_password):
            return None
        return tenant
