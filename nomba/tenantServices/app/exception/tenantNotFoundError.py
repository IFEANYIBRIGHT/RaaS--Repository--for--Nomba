class TenantNotFoundError(Exception):
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        super().__init__(f"Tenant not found: {tenant_id}")