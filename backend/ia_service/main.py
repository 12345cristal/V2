from fastapi import FastAPI
from .routers import ia_gemini, ia_recomendacion, ia_topsis

app = FastAPI(
    title="Autismo Mochis - IA Service",
    version="1.0.0",
)

app.include_router(ia_gemini.router, prefix="/ia")
app.include_router(ia_recomendacion.router, prefix="/ia")
app.include_router(ia_topsis.router, prefix="/ia")
