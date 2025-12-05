from app.api.v1.endpoints import ia_terapeuta

api_router.include_router(ia_terapeuta.router)
from app.api.v1.endpoints import ia_recomendaciones_padre

api_router.include_router(ia_recomendaciones_padre.router)
