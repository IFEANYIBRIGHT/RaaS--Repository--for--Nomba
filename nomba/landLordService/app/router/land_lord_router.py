from datetime import datetime
from nomba.landLordService.app.schemas.property_update_request import PropertyUpdateRequest
from fastapi import APIRouter, Depends, HTTPException

from nomba.landLordService.app.dependencies import get_land_lord_service
from nomba.landLordService.app.services.land_lord_services import LandLordService
from nomba.landLordService.app.models.land_lord import LandLord
from nomba.landLordService.app.schemas.land_lord_request import LandLordRequest
from nomba.tenantServices.app.models.tenants import Tenants
from nomba.careTakerServices.app.models.care_taker import CareTaker
from nomba.landLordService.app.schemas.tenants_requests import TenantsRequests
from nomba.landLordService.app.schemas.care_takers_requests import CareTakersRequests
from nomba.landLordService.app.schemas.login_request import LoginRequest
from nomba.landLordService.app.schemas.virtual_account_request import VirtualAccountRequest
from nomba.landLordService.app.schemas.tenant_update_request import TenantUpdateRequest

router = APIRouter(prefix="/landlord", tags=["landlord"])


@router.post("/virtual-account")
async def set_virtual_account_number(
    request: VirtualAccountRequest,
    service: LandLordService = Depends(get_land_lord_service),
):
    updated = await service.set_virtual_account_number(request.identifier, request.virtual_account_number, request.bank_name, request.account_name)
    if not updated:
        raise HTTPException(status_code=404, detail="Landlord not found")
    return {"message": "Virtual account number saved successfully"}

@router.get("/virtual-account/{identifier}")
async def get_virtual_account_number(
    identifier: str,
    service: LandLordService = Depends(get_land_lord_service),
):
    number = await service.get_virtual_account_number(identifier)
    if number is None:
        raise HTTPException(status_code=404, detail="Virtual account number not found")
    return number


@router.post("/register")
async def register_property(
    request: LandLordRequest,
    service: LandLordService = Depends(get_land_lord_service),
):
    land_lord = LandLord(
        land_lord_name=request.name,
        password=request.password,
        email=request.email,
        phone_number=request.phone_number,
        residential_address=request.residential_number,
        property_address=request.property_address,
        land_use_type=request.land_use_type,
        certificate_of_occupancy=request.certificate_of_occupancy,
        plot_number=request.plot_number,
    )
    return await service.register_property(land_lord)


@router.post("/login")
async def login(
    request: LoginRequest,
    service: LandLordService = Depends(get_land_lord_service),
):
    land_lord = await service.login(request.identifier, request.password)
    if not land_lord:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    land_lord["_id"] = str(land_lord["_id"])
    return {
        "message": "Login successful",
        "land_lord": land_lord,
    }


@router.get("/tenants")
async def get_all_tenants(
    service: LandLordService = Depends(get_land_lord_service),
):
    return await service.get_all_tenants()


@router.get("/{land_lord_id}")
async def get_land_lord(
    land_lord_id: str,
    service: LandLordService = Depends(get_land_lord_service),
):
    land_lord = await service.get_land_lord_by_id(land_lord_id)
    if not land_lord:
        raise HTTPException(status_code=404, detail="Landlord not found")
    land_lord["_id"] = str(land_lord["_id"])
    return land_lord


@router.post("/tenants")
async def add_tenant(
    request: TenantsRequests,
    service: LandLordService = Depends(get_land_lord_service),
):
    tenant = Tenants(
        request.name,
        request.phone_number,
        request.tenant_email,
        request.flat_no,
        datetime.now(),
    )
    return await service.add_a_tenant(tenant, request.monthly_rent, request.lease_start, request.landlord_email)


@router.get("/tenants/{tenant_id}")
async def get_tenant(
    tenant_id: str,
    service: LandLordService = Depends(get_land_lord_service),
):
    return await service.get_a_tenant(tenant_id)


@router.delete("/tenants/{tenant_id}")
async def delete_tenant(
    tenant_id: str,
    service: LandLordService = Depends(get_land_lord_service),
):
    return await service.delete_a_tenant(tenant_id)


@router.patch("/tenants/{tenant_id}")
async def update_tenant(
    tenant_id: str,
    request: TenantUpdateRequest,
    service: LandLordService = Depends(get_land_lord_service),
):
    update_data = {k: v for k, v in request.model_dump().items() if v is not None}
    updated = await service.update_a_tenant(tenant_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return {"message": "Tenant updated successfully"}


@router.post("/caretakers")
async def add_caretaker(
    request: CareTakersRequests,
    service: LandLordService = Depends(get_land_lord_service),
):
    care_taker = CareTaker(
        id="",
        name=request.name,
        phone_number=request.phone_number,
        care_taker_email=request.care_taker_email,
        password="",
        flat_no=request.flat_no,
        date=datetime.now(),
    )
    return await service.add_a_caretaker(care_taker)

@router.patch("/property/{land_lord_id}")
async def update_property(
    land_lord_id: str,
    request: PropertyUpdateRequest,
    service: LandLordService = Depends(get_land_lord_service),
):
    return await service.update_property(land_lord_id, request.model_dump())