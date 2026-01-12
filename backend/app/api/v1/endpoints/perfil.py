# app/api/v1/endpoints/perfil.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import shutil
import os

from app.api.deps import get_db_session, get_current_user
from app.models.usuario import Usuario
from app.models.personal import Personal
from app.models.personal_perfil import PersonalPerfil
from app.schemas.perfil import PerfilResponse
from app.core.config import settings

router = APIRouter(
    tags=["Perfil"]
)

# ==================== CONFIGURACIÓN DE DIRECTORIOS ====================
UPLOADS_DIR = Path(settings.BASE_DIR) / "uploads"
FOTOS_DIR = UPLOADS_DIR / "fotos"
CV_DIR = UPLOADS_DIR / "cv"
DOCUMENTOS_DIR = UPLOADS_DIR / "documentos"

# Crear directorios si no existen
FOTOS_DIR.mkdir(parents=True, exist_ok=True)
CV_DIR.mkdir(parents=True, exist_ok=True)
DOCUMENTOS_DIR.mkdir(parents=True, exist_ok=True)


# ==================== HELPER FUNCTIONS ====================
def generar_nombre_unico(personal_id: int, filename: str) -> str:
    """
    Genera nombre único: personal_<id>_<timestamp>_<filename>
    Ejemplo: personal_1_1700000000_foto.png
    """
    timestamp = int(time.time())
    # Eliminar espacios del filename original
    safe_filename = filename.replace(" ", "_")
    return f"personal_{personal_id}_{timestamp}_{safe_filename}"


def guardar_archivo(
    file: UploadFile,
    directorio: Path,
    personal_id: int
) -> str:
    """
    Guarda archivo en el directorio especificado
    Retorna: ruta relativa (ej: "fotos/personal_1_1700000000_foto.png")
    """
    if not file or not file.filename:
        return None

    # Generar nombre único
    nombre_unico = generar_nombre_unico(personal_id, file.filename)
    ruta_completa = directorio / nombre_unico
    ruta_relativa = f"{directorio.name}/{nombre_unico}"  # fotos/..., cv/..., documentos/...

    # Guardar archivo
    try:
        with open(ruta_completa, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return ruta_relativa
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al guardar archivo: {str(e)}"
        )
    finally:
        file.file.close()


# ==================== ENDPOINTS ====================

# ===============================
# CONFIGURACIÓN DE UPLOADS
# ===============================
UPLOADS_BASE = Path("uploads")
FOTOS_DIR = UPLOADS_BASE / "fotos"
CV_DIR = UPLOADS_BASE / "cv"

FOTOS_DIR.mkdir(parents=True, exist_ok=True)
CV_DIR.mkdir(parents=True, exist_ok=True)

MAX_IMAGE_SIZE = 3 * 1024 * 1024  # 3MB
MAX_PDF_SIZE = 5 * 1024 * 1024    # 5MB


# ===============================
# GET PERFIL
# ===============================
@router.get("/me", response_model=PerfilResponse)
def get_me(db: Session = Depends(get_db_session), current_user: Usuario = Depends(get_current_user)):
    personal = db.query(Personal).filter(Personal.id_usuario == current_user.id).first()
    if not personal:
        raise HTTPException(status_code=404, detail="No existe registro de personal asociado.")

    perfil = (
        db.query(PersonalPerfil)
        .filter(PersonalPerfil.personal_id == personal.id)
        .first()
    )

    # Crear perfil si no existe
    if not perfil:
        perfil = PersonalPerfil(personal_id=personal.id)
        db.add(perfil)
        db.commit()
        db.refresh(perfil)

    return PerfilResponse.from_db(personal, perfil, current_user)


# ===============================
# UPDATE PERFIL
# ===============================
@router.put("/me", response_model=PerfilResponse)
def actualizar_perfil(
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user),

    telefono_personal: str = Form(None),
    correo_personal: str = Form(None),

    grado_academico: str = Form(None),
    especialidades: str = Form(None),
    experiencia: str = Form(None),

    domicilio_calle: str = Form(None),
    domicilio_colonia: str = Form(None),
    domicilio_cp: str = Form(None),
    domicilio_municipio: str = Form(None),
    domicilio_estado: str = Form(None),

    foto_perfil: UploadFile = File(None),
    cv_archivo: UploadFile = File(None)
):
    personal = db.query(Personal).filter(Personal.id_usuario == current_user.id).first()
    if not personal:
        raise HTTPException(status_code=404, detail="No existe registro de personal.")

    perfil = db.query(PersonalPerfil).filter(
        PersonalPerfil.personal_id == personal.id
    ).first()

    if not perfil:
        perfil = PersonalPerfil(personal_id=personal.id)
        db.add(perfil)

    # Crear directorio si no existe
    os.makedirs("static/fotos", exist_ok=True)
    os.makedirs("static/cv", exist_ok=True)

    # FOTO (solo si se sube)
    if foto_perfil and foto_perfil.filename:
        ruta = f"static/fotos/personal_{personal.id}_{foto_perfil.filename}"
        with open(ruta, "wb") as f:
            shutil.copyfileobj(foto_perfil.file, f)
        perfil.foto_url = ruta

    # CV (solo si se sube)
    if cv_archivo and cv_archivo.filename:
        ruta = f"static/cv/personal_{personal.id}_{cv_archivo.filename}"
        with open(ruta, "wb") as f:
            shutil.copyfileobj(cv_archivo.file, f)
        perfil.cv_url = ruta

    # CAMPOS (solo actualizar si se envían)
    if telefono_personal is not None:
        perfil.telefono_personal = telefono_personal
    if correo_personal is not None:
        perfil.correo_personal = correo_personal
    if especialidades is not None:
        perfil.especialidades = especialidades
    if experiencia is not None:
        perfil.experiencia = experiencia

    # Domicilio
    if domicilio_calle is not None:
        perfil.domicilio_calle = domicilio_calle
    if domicilio_colonia is not None:
        perfil.domicilio_colonia = domicilio_colonia
    if domicilio_cp is not None:
        perfil.domicilio_cp = domicilio_cp
    if domicilio_municipio is not None:
        perfil.domicilio_municipio = domicilio_municipio
    if domicilio_estado is not None:
        perfil.domicilio_estado = domicilio_estado

    db.commit()
    db.refresh(perfil)
    db.refresh(personal)

    return PerfilResponse.from_db(personal, perfil, current_user)


# ==================== ENDPOINT DE DESCARGAS PROTEGIDAS ====================

@router.get("/archivos/{tipo}/{filename}")
def descargar_archivo(
    tipo: str,
    filename: str,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user)
):
    """
    GET /api/v1/perfil/archivos/{tipo}/{filename}
    Descarga un archivo protegido por JWT
    
    Tipos válidos:
    - fotos
    - cv
    - documentos
    
    Ejemplo:
    GET /api/v1/perfil/archivos/fotos/personal_1_1700000000_foto.png
    """
    # Validar tipo
    tipos_validos = {"fotos", "cv", "documentos"}
    if tipo not in tipos_validos:
        raise HTTPException(status_code=400, detail="Tipo de archivo inválido.")

    # Mapear tipo a directorio
    directorios = {
        "fotos": FOTOS_DIR,
        "cv": CV_DIR,
        "documentos": DOCUMENTOS_DIR
    }

    directorio = directorios[tipo]
    ruta_archivo = directorio / filename

    # Validar que el archivo existe y está dentro del directorio permitido
    try:
        ruta_archivo = ruta_archivo.resolve()
        directorio = directorio.resolve()
        
        # Seguridad: verificar que la ruta está dentro del directorio
        if not str(ruta_archivo).startswith(str(directorio)):
            raise HTTPException(status_code=403, detail="Acceso denegado.")
        
        if not ruta_archivo.exists():
            raise HTTPException(status_code=404, detail="Archivo no encontrado.")

    except (ValueError, RuntimeError):
        raise HTTPException(status_code=403, detail="Ruta inválida.")

    # Retornar archivo
    return FileResponse(
        path=ruta_archivo,
        media_type="application/octet-stream",
        filename=filename
    )
