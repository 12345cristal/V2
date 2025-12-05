# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.endpoints import auth, personal, ia  # luego agregas terapias, usuarios, ninos

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_v1 = FastAPI()
api_v1.include_router(auth.router)
api_v1.include_router(personal.router)
api_v1.include_router(ia.router)

app.mount(settings.API_V1_PREFIX, api_v1)
