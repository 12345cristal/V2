from fastapi import APIRouter
from app.api.v1 import auth, ninos, recomendaciones
from app.api.v1.endpoints import personal, terapias, citas, coordinador, perfil, topsis, recomendacion, topsis_terapeutas, recomendaciones_actividades, fichas_emergencia, gemini_ia, terapeuta, catalogos, usuarios

api_router = APIRouter()

# Incluir routers
api_router.include_router(catalogos.router, prefix="", tags=["Catálogos Públicos"])
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(ninos.router, prefix="/ninos", tags=["Niños Beneficiarios"])
api_router.include_router(personal.router, prefix="/personal", tags=["Personal"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Gestión de Usuarios"])
api_router.include_router(terapias.router, prefix="/terapias", tags=["Terapias"])
api_router.include_router(citas.router, prefix="/citas", tags=["Citas"])
api_router.include_router(coordinador.router, prefix="/coordinador", tags=["Coordinador"])
api_router.include_router(perfil.router, prefix="/perfil", tags=["Perfil de Usuario"])
api_router.include_router(topsis.router, prefix="/topsis", tags=["TOPSIS"])
api_router.include_router(recomendacion.router, prefix="/recomendacion", tags=["Recomendación"])
api_router.include_router(recomendaciones.router, prefix="/recomendaciones", tags=["Recomendaciones Inteligentes"])
api_router.include_router(recomendaciones_actividades.router, prefix="/recomendaciones-actividades", tags=["Recomendaciones de Actividades"])
api_router.include_router(fichas_emergencia.router, prefix="/fichas-emergencia", tags=["Fichas de Emergencia"])
api_router.include_router(gemini_ia.router, prefix="/ia", tags=["Inteligencia Artificial - Gemini"])
api_router.include_router(terapeuta.router, prefix="/terapeuta", tags=["Terapeuta"])
