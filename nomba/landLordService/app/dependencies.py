from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from nomba.database import get_database
from nomba.landLordService.app.repository.tenant_repo import TenantsRepo
from nomba.landLordService.app.repository.land_lord_repository import LandLordRepository
from nomba.landLordService.app.repository.payment_repo import PaymentRepo
from nomba.landLordService.app.nomba_client.nomba_client import NombaClient
from nomba.landLordService.app.services.land_lord_services import LandLordService
from nomba.landLordService.app.services.payment_services import PaymentService
from nomba.careTakerServices.app.repository.care_taker_repo import CareTakerRepo


def get_tenants_collection() -> AsyncIOMotorCollection:
    return get_database()["tenants"]

def get_land_lords_collection() -> AsyncIOMotorCollection:
    return get_database()["land_lords"]

def get_payments_collection() -> AsyncIOMotorCollection:
    return get_database()["payments"]

def get_tenants_repo(collection: AsyncIOMotorCollection = Depends(get_tenants_collection)) -> TenantsRepo:
    return TenantsRepo(collection)

def get_land_lord_repo(collection: AsyncIOMotorCollection = Depends(get_land_lords_collection)) -> LandLordRepository:
    return LandLordRepository(collection)

def get_payment_repo(collection: AsyncIOMotorCollection = Depends(get_payments_collection)) -> PaymentRepo:
    return PaymentRepo(collection)

def get_nomba_client() -> NombaClient:
    return NombaClient()

def get_care_takers_collection() -> AsyncIOMotorCollection:
    return get_database()["care_takers"]

def get_care_taker_repo(collection: AsyncIOMotorCollection = Depends(get_care_takers_collection)) -> CareTakerRepo:
    return CareTakerRepo(collection)

def get_land_lord_service(
    land_lord_repo: LandLordRepository = Depends(get_land_lord_repo),
    tenants_repo: TenantsRepo = Depends(get_tenants_repo),
    care_taker_repo: CareTakerRepo = Depends(get_care_taker_repo),
) -> LandLordService:
    return LandLordService(land_lord_repo, tenants_repo, care_taker_repo)

def get_payment_service(
    nomba_client: NombaClient = Depends(get_nomba_client),
    payment_repo: PaymentRepo = Depends(get_payment_repo),
    tenants_repo: TenantsRepo = Depends(get_tenants_repo),
) -> PaymentService:
    return PaymentService(nomba_client, payment_repo, tenants_repo)