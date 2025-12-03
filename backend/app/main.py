# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.endpoints import auth as auth_router
from app.api.v1.endpoints import usuarios as usuarios_router
from app.api.v1.endpoints import ninos as ninos_router
from app.api.v1.endpoints import notificaciones as notifs_router

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix=settings.API_V1_PREFIX)
app.include_router(usuarios_router.router, prefix=settings.API_V1_PREFIX)
app.include_router(ninos_router.router, prefix=settings.API_V1_PREFIX)
app.include_router(notifs_router.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    return {"message": "Autismo Mochis IA API"}
