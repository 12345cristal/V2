# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.endpoints import (
    auth,
    usuarios,
    roles,
    personal,
    ninos,
    citas,
    terapias,
    actividades_padre,
    recursos_terapeuta,
    notificaciones,
    perfil,
    terapeuta,
    inicio_padre,
    inicio_terapeuta,
    ia,
    topsis,
    documentos,
)

def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    prefix = settings.API_V1_PREFIX

    app.include_router(auth.router, prefix=prefix, tags=["auth"])
    app.include_router(usuarios.router, prefix=prefix, tags=["usuarios"])
    app.include_router(roles.router, prefix=prefix, tags=["roles"])
    app.include_router(personal.router, prefix=prefix, tags=["personal"])
    app.include_router(ninos.router, prefix=prefix, tags=["ninos"])
    app.include_router(citas.router, prefix=prefix, tags=["citas"])
    app.include_router(terapias.router, prefix=prefix, tags=["terapias"])
    app.include_router(actividades_padre.router, prefix=prefix, tags=["padre-actividades"])
    app.include_router(recursos_terapeuta.router, prefix=prefix, tags=["terapeuta-recursos"])
    app.include_router(notificaciones.router, prefix=prefix, tags=["notificaciones"])
    app.include_router(perfil.router, prefix=prefix, tags=["perfil"])
    app.include_router(terapeuta.router, prefix=prefix, tags=["terapeuta"])
    app.include_router(inicio_padre.router, prefix=prefix, tags=["padres-inicio"])
    app.include_router(inicio_terapeuta.router, prefix=prefix, tags=["inicio-terapeuta"])
    app.include_router(ia.router, prefix=prefix, tags=["ia"])
    app.include_router(topsis.router, prefix=prefix, tags=["topsis"])
    app.include_router(documentos.router, prefix=prefix, tags=["documentos"])

    return app


app = create_application()
