from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from nomba.database import get_database
from nomba.tenantServices.app.repository.tenants_repo import TenantsRepo
from nomba.tenantServices.app.services.tenants_services import TenantsService


def get_tenants_collection() -> AsyncIOMotorCollection:
    return get_database()["tenants"]


def get_tenants_repo(collection: AsyncIOMotorCollection = Depends(get_tenants_collection)) -> TenantsRepo:
    return TenantsRepo(collection)


def get_tenants_service(repo: TenantsRepo = Depends(get_tenants_repo)) -> TenantsService:
    return TenantsService(repo)

def get_land_lords_collection() -> AsyncIOMotorCollection:
    return get_database()["land_lords"]