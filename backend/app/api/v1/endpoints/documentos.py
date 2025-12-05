from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import uuid, os

from app.db.session import get_db
from app.core.deps import get_current_active_user

router = APIRouter(prefix="/documentos")


class CrearDocumentoPadreDto(BaseModel):
    ninoId: int
    titulo: str
    descripcion: str | None = None
    tipo: str
    parentesco: str
    visibleParaTerapeutas: bool


@router.get("/terapeuta/{nino_id}")
def get_docs_terapeuta(nino_id: int, db: Session = Depends(get_db),
                       current=Depends(get_current_active_user)):
    # filtrar documentos visibles para terapeutas
    from app.models.documentos import Documento  # si la creas
    return db.query(Documento).filter(
        Documento.nino_id == nino_id,
        Documento.visible_terapeutas == True
    ).all()


@router.get("/padre/{nino_id}")
def get_docs_padre(nino_id: int, db: Session = Depends(get_db),
                   current=Depends(get_current_active_user)):
    from app.models.documentos import Documento
    return db.query(Documento).filter(
        Documento.nino_id == nino_id
    ).all()


@router.post("/padre")
async def subir_documento_padre(
    ninoId: int = Form(...),
    titulo: str = Form(...),
    descripcion: str | None = Form(default=None),
    tipo: str = Form(...),
    parentesco: str = Form(...),
    visibleParaTerapeutas: bool = Form(...),
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current=Depends(get_current_active_user),
):
    # Guarda archivo
    filename = f"{uuid.uuid4()}_{archivo.filename}"
    path = f"uploads/docs/{filename}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(await archivo.read())

    from app.models.documentos import Documento
    doc = Documento(
        nino_id=ninoId,
        titulo=titulo,
        descripcion=descripcion,
        fecha_subida=datetime.now(),
        url_archivo=path,
        nombre_archivo=archivo.filename,
        tipo=tipo,
        subido_por="PADRE",
        parentesco=parentesco,
        visible_terapeutas=visibleParaTerapeutas,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.delete("/padre/{doc_id}")
def eliminar_documento(doc_id: int, db: Session = Depends(get_db),
                       current=Depends(get_current_active_user)):
    from app.models.documentos import Documento
    doc = db.query(Documento).filter(Documento.id == doc_id).first()
    if not doc:
        raise HTTPException(404, "Documento no encontrado")
    db.delete(doc)
    db.commit()
    return {"ok": True}
