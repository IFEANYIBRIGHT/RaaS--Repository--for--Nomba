from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from nomba.careTakerServices.app.database import get_database
from nomba.careTakerServices.app.repository.care_taker_repo import CareTakerRepo
from nomba.careTakerServices.app.services.care_taker_services import CareTakerService
from nomba.careTakerServices.app.repository.maintenance_request_repo import MaintenanceRequestRepo
from nomba.careTakerServices.app.services.maintenance_request_service import MaintenanceRequestService


def get_care_takers_collection() -> AsyncIOMotorCollection:
    return get_database()["care_takers"]


def get_care_taker_repo(collection: AsyncIOMotorCollection = Depends(get_care_takers_collection)) -> CareTakerRepo:
    return CareTakerRepo(collection)


def get_care_taker_service(repo: CareTakerRepo = Depends(get_care_taker_repo)) -> CareTakerService:
    return CareTakerService(repo)


def get_maintenance_requests_collection() -> AsyncIOMotorCollection:
    return get_database()["maintenance_requests"]


def get_maintenance_request_repo(collection: AsyncIOMotorCollection = Depends(get_maintenance_requests_collection)) -> MaintenanceRequestRepo:
    return MaintenanceRequestRepo(collection)


def get_maintenance_request_service(repo: MaintenanceRequestRepo = Depends(get_maintenance_request_repo)) -> MaintenanceRequestService:
    return MaintenanceRequestService(repo)
