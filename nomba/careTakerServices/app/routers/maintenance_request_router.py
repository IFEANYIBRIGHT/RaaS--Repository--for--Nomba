from fastapi import APIRouter, Depends, HTTPException
from nomba.careTakerServices.app.dependencies import get_maintenance_request_service
from nomba.careTakerServices.app.services.maintenance_request_service import MaintenanceRequestService
from nomba.careTakerServices.app.schemas.maintenance_request_request import MaintenanceRequestRequest
from nomba.careTakerServices.app.schemas.update_status_request import UpdateStatusRequest

router = APIRouter(prefix="/maintenance-requests", tags=["maintenance-requests"])


@router.post("")
async def create_request(
    request: MaintenanceRequestRequest,
    service: MaintenanceRequestService = Depends(get_maintenance_request_service),
):
    return await service.create_request(
        title=request.title,
        priority=request.priority.value,
        unit=request.unit,
        property_name=request.property_name,
        care_taker_id=request.care_taker_id,
    )


@router.get("")
async def get_all_requests(
    service: MaintenanceRequestService = Depends(get_maintenance_request_service),
):
    return await service.get_all_requests()


@router.get("/summary")
async def get_task_summary(
    service: MaintenanceRequestService = Depends(get_maintenance_request_service),
):
    return await service.get_task_summary()


@router.patch("/{request_id}/status")
async def update_status(
    request_id: str,
    request: UpdateStatusRequest,
    service: MaintenanceRequestService = Depends(get_maintenance_request_service),
):
    updated = await service.update_status(request_id, request.status.value)
    if not updated:
        raise HTTPException(status_code=404, detail="Maintenance request not found")
    return {"message": "Status updated successfully"}
