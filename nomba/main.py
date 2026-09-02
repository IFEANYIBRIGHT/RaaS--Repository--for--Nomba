from contextlib import asynccontextmanager
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from nomba.database import connect_to_mongo, close_mongo_connection
from nomba.careTakerServices.app.exception.careTakerNotFoundError import CareTakerNotFoundError
from nomba.tenantServices.app.exception.tenantNotFoundError import TenantNotFoundError

from nomba.careTakerServices.app.routers import care_taker_router
from nomba.careTakerServices.app.routers import maintenance_request_router
from nomba.tenantServices.app.routers import tenants_router
from nomba.landLordService.app.router import land_lord_router
from nomba.landLordService.app.router import payment

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(title="Nomba", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "https://rentflow-frontend-five.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(CareTakerNotFoundError)
async def care_taker_not_found_handler(request: Request, exc: CareTakerNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(TenantNotFoundError)
async def tenant_not_found_handler(request: Request, exc: TenantNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

app.include_router(care_taker_router.router)
app.include_router(maintenance_request_router.router)
app.include_router(tenants_router.router)
app.include_router(land_lord_router.router)
