from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import auth
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Configuración CORS para Angular
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost",
    "http://127.0.0.1",
    "*",  # dev: permitir todo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=".*",  # asegura CORS con cualquier host en dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {"message": "Autismo Mochis API Running"}
