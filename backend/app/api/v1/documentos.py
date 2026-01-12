# app/api/v1/documentos.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.session import get_db
from app.api.deps import get_current_active_user
from app.models.usuario import Usuario
from app.models.documento import Documento, DocumentoVisto, TipoDocumento
from app.schemas.documento import (
    DocumentoResponse, DocumentoCreate, DocumentoUpdate, RespuestaDocumentos
)
from pathlib import Path
import shutil
import os
from datetime import datetime


router = APIRouter(prefix="/documentos", tags=["documentos"])

# Directorio de uploads
UPLOAD_DIR = Path("uploads/documentos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ==================================================
# GET - OBTENER DOCUMENTOS DE UN NIÑO
# ==================================================
@router.get("/hijo/{hijo_id}", response_model=RespuestaDocumentos)
def get_documentos_por_nino(
    hijo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtiene todos los documentos de un hijo.
    
    - **hijo_id**: ID del niño
    """
    try:
        # Obtener documentos
        documentos = db.query(Documento).filter(
            and_(
                Documento.nino_id == hijo_id,
                Documento.activo == True
            )
        ).order_by(Documento.nuevo.desc(), Documento.fecha_subida.desc()).all()
        
        # Mapear documentos con info de visto
        docs_response = []
        for doc in documentos:
            visto = db.query(DocumentoVisto).filter(
                and_(
                    DocumentoVisto.documento_id == doc.id,
                    DocumentoVisto.usuario_id == current_user.id
                )
            ).first()
            
            doc_data = DocumentoResponse.from_orm(doc)
            doc_data.visto = visto.visto if visto else False
            docs_response.append(doc_data)
        
        return RespuestaDocumentos(
            success=True,
            data=docs_response,
            total=len(docs_response)
        )
    except Exception as e:
        return RespuestaDocumentos(
            success=False,
            error=str(e)
        )


# ==================================================
# GET - OBTENER DOCUMENTOS NUEVOS
# ==================================================
@router.get("/hijo/{hijo_id}/nuevos", response_model=RespuestaDocumentos)
def get_documentos_nuevos(
    hijo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtiene solo los documentos nuevos (no vistos) de un hijo.
    """
    try:
        documentos = db.query(Documento).filter(
            and_(
                Documento.nino_id == hijo_id,
                Documento.activo == True,
                Documento.nuevo == True
            )
        ).order_by(Documento.fecha_subida.desc()).all()
        
        docs_response = []
        for doc in documentos:
            visto = db.query(DocumentoVisto).filter(
                and_(
                    DocumentoVisto.documento_id == doc.id,
                    DocumentoVisto.usuario_id == current_user.id
                )
            ).first()
            
            doc_data = DocumentoResponse.from_orm(doc)
            doc_data.visto = visto.visto if visto else False
            docs_response.append(doc_data)
        
        return RespuestaDocumentos(
            success=True,
            data=docs_response,
            total=len(docs_response)
        )
    except Exception as e:
        return RespuestaDocumentos(success=False, error=str(e))


# ==================================================
# GET - OBTENER UN DOCUMENTO ESPECÍFICO
# ==================================================
@router.get("/{documento_id}", response_model=DocumentoResponse)
def get_documento(
    documento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtiene un documento específico"""
    documento = db.query(Documento).filter(
        and_(
            Documento.id == documento_id,
            Documento.activo == True
        )
    ).first()
    
    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado"
        )
    
    return DocumentoResponse.from_orm(documento)


# ==================================================
# POST - MARCAR DOCUMENTO COMO VISTO
# ==================================================
@router.post("/{documento_id}/visto")
def marcar_documento_visto(
    documento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Marca un documento como visto"""
    documento = db.query(Documento).filter(Documento.id == documento_id).first()
    
    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado"
        )
    
    # Crear o actualizar registro de visto
    visto = db.query(DocumentoVisto).filter(
        and_(
            DocumentoVisto.documento_id == documento_id,
            DocumentoVisto.usuario_id == current_user.id
        )
    ).first()
    
    if not visto:
        visto = DocumentoVisto(
            documento_id=documento_id,
            usuario_id=current_user.id,
            visto=True,
            fecha_visto=datetime.utcnow()
        )
        db.add(visto)
    else:
        visto.visto = True
        visto.fecha_visto = datetime.utcnow()
    
    # Marcar documento como no nuevo si todos lo vieron
    documento.nuevo = False
    
    db.commit()
    
    return {
        "success": True,
        "mensaje": "Documento marcado como visto"
    }


# ==================================================
# GET - DESCARGAR DOCUMENTO
# ==================================================
@router.get("/{documento_id}/descargar")
def descargar_documento(
    documento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Descarga un documento y lo marca como visto"""
    from fastapi.responses import FileResponse
    
    documento = db.query(Documento).filter(
        and_(
            Documento.id == documento_id,
            Documento.activo == True
        )
    ).first()
    
    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado"
        )
    
    # Marcar como visto
    visto = db.query(DocumentoVisto).filter(
        and_(
            DocumentoVisto.documento_id == documento_id,
            DocumentoVisto.usuario_id == current_user.id
        )
    ).first()
    
    if not visto:
        visto = DocumentoVisto(
            documento_id=documento_id,
            usuario_id=current_user.id,
            visto=True
        )
        db.add(visto)
    else:
        visto.visto = True
        visto.fecha_visto = datetime.utcnow()
    
    documento.nuevo = False
    db.commit()
    
    # Retornar archivo
    file_path = UPLOAD_DIR / documento.url_archivo
    
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archivo no encontrado"
        )
    
    return FileResponse(
        path=file_path,
        filename=documento.nombre,
        media_type=documento.tipo_archivo
    )


# ==================================================
# POST - SUBIR NUEVO DOCUMENTO
# ==================================================
@router.post("/hijo/{hijo_id}/upload", response_model=DocumentoResponse)
def subir_documento(
    hijo_id: int,
    tipo: str = Form(...),
    nombre: str = Form(...),
    descripcion: str = Form(None),
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Sube un nuevo documento.
    Solo coordinadores pueden subir ciertos tipos.
    """
    # Validar tipo
    try:
        tipo_doc = TipoDocumento(tipo)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de documento inválido"
        )
    
    # Validar que sea PDF
    if archivo.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se aceptan archivos PDF"
        )
    
    # Validar tamaño (50MB max)
    if archivo.size and archivo.size > 50 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Archivo demasiado grande (máx 50MB)"
        )
    
    # Guardar archivo
    try:
        file_name = f"{datetime.utcnow().timestamp()}_{archivo.filename}"
        file_path = UPLOAD_DIR / file_name
        
        with file_path.open("wb") as f:
            shutil.copyfileobj(archivo.file, f)
        
        # Crear documento en BD
        documento = Documento(
            nino_id=hijo_id,
            tipo_documento=tipo_doc,
            nombre=nombre,
            descripcion=descripcion,
            url_archivo=file_name,
            tipo_archivo=archivo.content_type,
            tamanio_bytes=archivo.size,
            nuevo=True,
            activo=True,
            subido_por=current_user.id
        )
        
        db.add(documento)
        db.commit()
        db.refresh(documento)
        
        return DocumentoResponse.from_orm(documento)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al subir archivo: {str(e)}"
        )


# ==================================================
# PUT - ACTUALIZAR DOCUMENTO
# ==================================================
@router.put("/{documento_id}", response_model=DocumentoResponse)
def actualizar_documento(
    documento_id: int,
    datos: DocumentoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Actualiza un documento (solo coordinadores)"""
    documento = db.query(Documento).filter(Documento.id == documento_id).first()
    
    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado"
        )
    
    # Actualizar campos
    if datos.nombre:
        documento.nombre = datos.nombre
    if datos.descripcion:
        documento.descripcion = datos.descripcion
    if datos.tipo_documento:
        documento.tipo_documento = datos.tipo_documento
    
    documento.fecha_actualizacion = datetime.utcnow()
    
    db.commit()
    db.refresh(documento)
    
    return DocumentoResponse.from_orm(documento)


# ==================================================
# DELETE - ELIMINAR DOCUMENTO
# ==================================================
@router.delete("/{documento_id}")
def eliminar_documento(
    documento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """Elimina un documento (solo coordinadores)"""
    documento = db.query(Documento).filter(Documento.id == documento_id).first()
    
    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado"
        )
    
    # Eliminar archivo físico
    try:
        file_path = UPLOAD_DIR / documento.url_archivo
        if file_path.exists():
            file_path.unlink()
    except Exception as e:
        print(f"Error eliminando archivo: {e}")
    
    # Eliminar de BD (soft delete)
    documento.activo = False
    db.commit()
    
    return {
        "success": True,
        "mensaje": "Documento eliminado"
    }