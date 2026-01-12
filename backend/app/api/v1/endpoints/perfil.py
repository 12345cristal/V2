# app/api/v1/endpoints/perfil.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import time
import json
from pathlib import Path

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

    # Guardar archivo (sin archivos temporales .tmp)
    try:
        # Leer contenido completo primero
        contenido = file.file.read()
        
        # Guardar directamente sin crear .tmp
        with open(ruta_completa, "wb") as buffer:
            buffer.write(contenido)
        
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
    cv_archivo: UploadFile = File(None),
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

    # FOTO (solo si se sube)
    if foto_perfil and foto_perfil.filename:
        ruta = guardar_archivo(foto_perfil, FOTOS_DIR, personal.id)
        if ruta:
            perfil.foto_perfil = ruta

    # CV (solo si se sube)
    if cv_archivo and cv_archivo.filename:
        # Validar que sea PDF
        if not cv_archivo.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="El CV debe ser un archivo PDF")
        ruta = guardar_archivo(cv_archivo, CV_DIR, personal.id)
        if ruta:
            perfil.cv_archivo = ruta

    # CAMPOS (solo actualizar si se envían)
    if telefono_personal is not None:
        perfil.telefono_personal = telefono_personal
    if correo_personal is not None:
        perfil.correo_personal = correo_personal
    if grado_academico is not None:
        perfil.grado_academico = grado_academico
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

@router.post("/documentos-extra")
def agregar_documentos_extra(
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user),
    archivos: list[UploadFile] = File(None)
):
    """
    POST /api/v1/perfil/documentos-extra
    Agrega documentos extra (PDF, imágenes, etc)
    
    Permite subir múltiples documentos adicionales
    """
    personal = db.query(Personal).filter(Personal.id_usuario == current_user.id).first()
    if not personal:
        raise HTTPException(status_code=404, detail="No existe registro de personal.")

    perfil = db.query(PersonalPerfil).filter(
        PersonalPerfil.personal_id == personal.id
    ).first()

    if not perfil:
        perfil = PersonalPerfil(personal_id=personal.id)
        db.add(perfil)

    # Guardar documentos y mantener lista
    import json
    documentos = json.loads(perfil.documentos_extra or "[]")
    
    if archivos:
        for archivo in archivos:
            if archivo and archivo.filename:
                ruta = guardar_archivo(archivo, DOCUMENTOS_DIR, personal.id)
                if ruta:
                    documentos.append(ruta)
    
    # Guardar lista actualizada
    perfil.documentos_extra = json.dumps(documentos) if documentos else None
    
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


@router.get("/visualizar/{ruta_relativa:path}")
def visualizar_archivo(
    ruta_relativa: str,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user)
):
    """
    GET /api/v1/perfil/visualizar/{ruta_relativa}
    Visualiza un archivo PDF directamente sin descargar como .tmp
    
    Acepta rutas como:
    - cv/personal_1_1700000000_cv.pdf
    - documentos/personal_1_1700000000_certificado.pdf
    
    Retorna el PDF con mime-type correcto para visualización en navegador
    """
    from urllib.parse import unquote
    
    # Decodificar URL si viene codificada
    ruta_relativa = unquote(ruta_relativa)
    
    # Validar que es PDF
    if not ruta_relativa.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se pueden visualizar archivos PDF")

    # Extraer tipo de la ruta (cv, documentos, fotos)
    partes = ruta_relativa.split("/", 1)
    if len(partes) < 2:
        raise HTTPException(status_code=400, detail="Ruta de archivo inválida.")
    
    tipo = partes[0]
    filename = partes[1]
    
    # Validar tipo
    tipos_validos = {"cv", "documentos", "fotos"}
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

    # Retornar con media_type apropiado
    media_type = "application/pdf" if ruta_relativa.endswith('.pdf') else "image/*"
    headers = {"Content-Disposition": "inline"}  # Mostrar en navegador, no descargar
    
    return FileResponse(
        path=ruta_archivo,
        media_type=media_type,
        filename=filename,
        headers=headers
    )
