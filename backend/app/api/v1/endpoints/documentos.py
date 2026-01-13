from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from datetime import datetime
import shutil
import os
from pathlib import Path

# Asumiendo que tienes una estructura de BD
# Si no tienes modelos, créalos primero

router = APIRouter(
    prefix="/api/v1/documentos",
    tags=["Documentos"]
)

# Carpeta para almacenar archivos
UPLOAD_DIR = Path("uploads/documentos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ============================================
# GET - Listar todos los documentos
# ============================================
@router.get("")
async def listar_documentos(
    usuario_id: int = Query(...),
    tipo: str = Query(None)
):
    """
    Lista documentos del usuario
    - usuario_id: ID del usuario propietario
    - tipo: filtrar por tipo (opcional)
    """
    try:
        # TODO: Conectar a BD y filtrar por usuario_id
        documentos = [
            {
                "id": 1,
                "nombre": "Documento1.pdf",
                "tipo": "pdf",
                "fecha_creacion": "2026-01-12",
                "usuario_id": usuario_id
            }
        ]
        return documentos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# GET - Descargar documento específico
# ============================================
@router.get("/{documento_id}")
async def descargar_documento(documento_id: int):
    """
    Descarga un documento específico
    """
    try:
        # TODO: Buscar en BD y retornar archivo
        # Por ahora retorna estructura
        return {
            "id": documento_id,
            "nombre": "documento.pdf",
            "contenido": "base64_encoded_file"
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Documento no encontrado")


# ============================================
# POST - Subir nuevo documento
# ============================================
@router.post("")
async def subir_documento(
    file: UploadFile = File(...),
    usuario_id: int = Query(...),
    titulo: str = Query(None)
):
    """
    Sube un nuevo documento
    """
    try:
        # Validar tipo de archivo
        tipos_permitidos = ["pdf", "docx", "xlsx", "jpg", "png", "txt"]
        extension = file.filename.split(".")[-1].lower()
        
        if extension not in tipos_permitidos:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de archivo no permitido. Permitidos: {', '.join(tipos_permitidos)}"
            )
        
        # Generar nombre único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{usuario_id}_{timestamp}_{file.filename}"
        ruta_archivo = UPLOAD_DIR / nombre_archivo
        
        # Guardar archivo
        with open(ruta_archivo, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # TODO: Guardar registro en BD
        documento_creado = {
            "id": 1,
            "nombre": file.filename,
            "nombre_almacenado": nombre_archivo,
            "tipo": extension,
            "tamaño": file.size,
            "fecha_creacion": datetime.now().isoformat(),
            "usuario_id": usuario_id,
            "titulo": titulo or file.filename
        }
        
        return documento_creado
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# DELETE - Eliminar documento
# ============================================
@router.delete("/{documento_id}")
async def eliminar_documento(documento_id: int, usuario_id: int = Query(...)):
    """
    Elimina un documento
    """
    try:
        # TODO: Buscar en BD y verificar propiedad
        # Eliminar archivo del servidor
        # ruta_archivo = UPLOAD_DIR / "nombre_archivo"
        # if ruta_archivo.exists():
        #     ruta_archivo.unlink()
        
        return {
            "mensaje": "Documento eliminado correctamente",
            "documento_id": documento_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# PUT - Actualizar documento
# ============================================
@router.put("/{documento_id}")
async def actualizar_documento(
    documento_id: int,
    titulo: str = Query(None),
    usuario_id: int = Query(...)
):
    """
    Actualiza metadatos del documento
    """
    try:
        # TODO: Actualizar en BD
        return {
            "id": documento_id,
            "titulo": titulo,
            "fecha_actualizacion": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))