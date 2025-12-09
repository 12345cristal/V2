# backend/app/api/v1/endpoints/perfil.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from app.api import deps
from app.models.personal import Personal
from app.models.usuario import Usuario
from app.schemas.personal import PersonalResponse
from app.db.session import get_db

router = APIRouter()


@router.get("/me", response_model=PersonalResponse)
def get_mi_perfil(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(deps.get_current_user)
):
    """
    Obtener el perfil del usuario autenticado (personal/terapeuta).
    """
    print(f"\n🔍 GET /perfil/me llamado por usuario ID: {current_user.id}")
    print(f"   Email: {current_user.email}")
    
    # Buscar el registro de Personal asociado al usuario autenticado
    personal = db.query(Personal).filter(
        Personal.id_usuario == current_user.id
    ).first()

    if not personal:
        print(f"❌ No se encontró registro de Personal para usuario ID: {current_user.id}")
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró información de personal para el usuario {current_user.email}"
        )

    print(f"✅ Personal encontrado: {personal.nombres} {personal.apellido_paterno}")
    print(f"   ID Personal: {personal.id}")
    print(f"   Foto: {personal.foto_perfil or 'Sin foto'}")
    print(f"   CV: {personal.cv_archivo or 'Sin CV'}")
    
    return personal


@router.put("/me", response_model=PersonalResponse)
def actualizar_mi_perfil(
    telefono_personal: str = Form(...),
    correo_personal: str = Form(...),
    grado_academico: str = Form(...),
    especialidades: str = Form(...),
    experiencia: str = Form(...),
    domicilio_calle: str = Form(...),
    domicilio_colonia: str = Form(...),
    domicilio_cp: str = Form(...),
    domicilio_municipio: str = Form(...),
    domicilio_estado: str = Form(...),
    foto_perfil: Optional[UploadFile] = File(None),
    cv_archivo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(deps.get_current_user)
):
    """
    Actualizar el perfil del usuario autenticado.
    Solo permite editar campos específicos (contacto, profesional, domicilio, archivos).
    """
    # Buscar el registro de Personal
    personal = db.query(Personal).filter(
        Personal.id_usuario == current_user.id
    ).first()

    if not personal:
        raise HTTPException(
            status_code=404,
            detail="No se encontró información de personal para este usuario"
        )

    # Actualizar campos editables
    personal.telefono_personal = telefono_personal
    personal.correo_personal = correo_personal
    personal.grado_academico = grado_academico
    personal.especialidades = especialidades
    personal.experiencia = experiencia
    
    # Domicilio
    personal.calle = domicilio_calle
    personal.colonia = domicilio_colonia
    personal.codigo_postal = domicilio_cp
    personal.ciudad = domicilio_municipio
    personal.estado = domicilio_estado

    # Guardar archivos si se proporcionan
    if foto_perfil:
        import os
        from pathlib import Path
        
        # Crear directorio de uploads si no existe
        upload_dir = Path("uploads/fotos")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Guardar archivo con nombre único
        file_path = upload_dir / f"user_{current_user.id}_{foto_perfil.filename}"
        with open(file_path, "wb") as f:
            f.write(foto_perfil.file.read())
        
        personal.foto_perfil = f"/uploads/fotos/{file_path.name}"
    
    if cv_archivo:
        import os
        from pathlib import Path
        
        upload_dir = Path("uploads/cv")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_dir / f"cv_{current_user.id}_{cv_archivo.filename}"
        with open(file_path, "wb") as f:
            f.write(cv_archivo.file.read())
        
        personal.cv_archivo = f"/uploads/cv/{file_path.name}"

    try:
        db.commit()
        db.refresh(personal)
        print(f"✅ Perfil actualizado para usuario: {personal.nombres} {personal.apellido_paterno}")
        return personal
    except Exception as e:
        db.rollback()
        print(f"❌ Error al actualizar perfil: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar el perfil: {str(e)}"
        )
