from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from api.deps import get_current_user
import os

router = APIRouter(prefix="/archivos", tags=["Archivos"])

@router.get("/{tipo}/{filename}")
def obtener_archivo(
    tipo: str,
    filename: str,
    user = Depends(get_current_user)
):
    base_path = f"uploads/{tipo}"
    path = os.path.join(base_path, filename)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    return FileResponse(
        path,
        media_type="application/octet-stream",
        filename=filename
    )
