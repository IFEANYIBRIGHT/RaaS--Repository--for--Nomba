from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection

from nomba.tenantServices.app.dependencies import get_tenants_service, get_land_lords_collection
from nomba.tenantServices.app.services.tenants_services import TenantsService
from nomba.tenantServices.app.schemas.login_request import LoginRequest
from nomba.tenantServices.app.schemas.set_password_request import SetPasswordRequest
from nomba.tenantServices.app.schemas.tenant_response import TenantResponse

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("/set-password")
async def set_password(
    request: SetPasswordRequest,
    service: TenantsService = Depends(get_tenants_service),
):
    updated = await service.set_password(request.identifier, request.new_password)
    if not updated:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return {"message": "Password set successfully"}


@router.post("/login")
async def login(
    request: LoginRequest,
    service: TenantsService = Depends(get_tenants_service),
):
    tenant = await service.login(request.identifier, request.password)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    tenant["id"] = str(tenant["_id"])
    return {
        "message": "Login successful",
        "tenant": TenantResponse(**tenant),
    }


@router.get("/landlord/virtual-account/{landlord_identifier}")
async def get_landlord_virtual_account(
    landlord_identifier: str,
    land_lords_collection: AsyncIOMotorCollection = Depends(get_land_lords_collection),
):
    land_lord = await land_lords_collection.find_one(
        {"$or": [{"email": landlord_identifier}, {"phone_number": landlord_identifier}]},
        {"virtual_account_number": 1, "bank_name": 1, "account_name": 1},
    )
    return {
        "virtual_account_number": land_lord.get("virtual_account_number") if land_lord else None,
        "bank_name": land_lord.get("bank_name") if land_lord else None,
        "account_name": land_lord.get("account_name") if land_lord else None,
    }


@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_my_profile(
    tenant_id: str,
    service: TenantsService = Depends(get_tenants_service),
):
    tenant = await service.get_my_profile(tenant_id)
    tenant["id"] = str(tenant["_id"])
    return TenantResponse(**tenant)
