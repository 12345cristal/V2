from app.api.v1.endpoints import ia_terapeuta

api_router.include_router(ia_terapeuta.router)
from app.api.v1.endpoints import ia_recomendaciones_padre

api_router.include_router(ia_recomendaciones_padre.router)
api_router.include_router(ia_recomendaciones_terapeuta.router)
from app.api.v1.endpoints import decision_support

api_router.include_router(decision_support.router)
