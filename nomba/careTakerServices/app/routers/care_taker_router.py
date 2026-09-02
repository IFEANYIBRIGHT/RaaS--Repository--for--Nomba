from fastapi import APIRouter, Depends, HTTPException
from nomba.careTakerServices.app.dependencies import get_care_taker_service
from nomba.careTakerServices.app.services.care_taker_services import CareTakerService
from nomba.careTakerServices.app.schemas.login_request import LoginRequest
from nomba.careTakerServices.app.schemas.set_password_request import SetPasswordRequest
from nomba.careTakerServices.app.schemas.care_taker_response import CareTakerResponse

router = APIRouter(prefix="/caretakers", tags=["caretakers"])


@router.post("/set-password")
async def set_password(
    request: SetPasswordRequest,
    service: CareTakerService = Depends(get_care_taker_service),
):
    updated = await service.set_password(request.identifier, request.new_password)
    if not updated:
        raise HTTPException(status_code=404, detail="Care taker not found")
    return {"message": "Password set successfully"}


@router.post("/login")
async def login(
    request: LoginRequest,
    service: CareTakerService = Depends(get_care_taker_service),
):
    care_taker = await service.login(request.identifier, request.password)
    if not care_taker:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    care_taker["id"] = str(care_taker["_id"])
    return {
        "message": "Login successful",
        "care_taker": CareTakerResponse(**care_taker),
    }


@router.get("/{care_taker_id}", response_model=CareTakerResponse)
async def get_my_profile(
    care_taker_id: str,
    service: CareTakerService = Depends(get_care_taker_service),
):
    care_taker = await service.get_my_profile(care_taker_id)
    care_taker["id"] = str(care_taker["_id"])
    return CareTakerResponse(**care_taker)
