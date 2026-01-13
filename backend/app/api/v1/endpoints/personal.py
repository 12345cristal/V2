# backend/app/api/v1/endpoints/personal.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import math

from app.api.deps import get_db, get_current_user
from app.models.personal import Personal, PersonalHorario, EstadoLaboral
from app.models.rol import Rol
from app.schemas.personal import (
    PersonalCreate, PersonalUpdate, PersonalResponse, PersonalListResponse, PersonalListItem,
    HorarioCreate, HorarioUpdate, HorarioResponse
)

router = APIRouter()


# ========== PERSONAL SIN USUARIO ==========
@router.get("/sin-usuario", response_model=List[dict])
def listar_personal_sin_usuario(
    db: Session = Depends(get_db)
):
    """Lista personal que no tiene usuario asociado"""
    from app.models.usuario import Usuario
    
    # Personal que no tiene usuario
    personal_sin_usuario = db.query(Personal).filter(
        Personal.id_usuario == None,
        Personal.estado_laboral == EstadoLaboral.ACTIVO
    ).all()
    
    resultado = []
    for p in personal_sin_usuario:
        nombre_completo = f"{p.nombres} {p.apellido_paterno}"
        if p.apellido_materno:
            nombre_completo += f" {p.apellido_materno}"
        
        resultado.append({
            "id_personal": p.id,
            "nombres": p.nombres,
            "apellido_paterno": p.apellido_paterno,
            "apellido_materno": p.apellido_materno,
            "nombre_completo": nombre_completo,
            "email": p.correo_personal,
            "telefono": p.telefono_personal,
            "rfc": p.rfc,
            "curp": p.curp,
            "especialidad_principal": p.especialidad_principal,
            "grado_academico": p.grado_academico
        })
    
    return resultado


# ========== PERSONAL CRUD ==========
@router.get("/", response_model=PersonalListResponse)
def listar_personal(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    buscar: Optional[str] = None,
    id_rol: Optional[int] = None,
    estado_laboral: Optional[EstadoLaboral] = None
):
    """Lista el personal con paginación y filtros"""
    query = db.query(Personal)
    
    # Filtros
    if buscar:
        buscar_lower = f"%{buscar.lower()}%"
        query = query.filter(
            (Personal.nombres.ilike(buscar_lower)) |
            (Personal.apellido_paterno.ilike(buscar_lower)) |
            (Personal.apellido_materno.ilike(buscar_lower)) |
            (Personal.rfc.ilike(buscar_lower)) |
            (Personal.curp.ilike(buscar_lower))
        )
    
    if id_rol:
        query = query.filter(Personal.id_rol == id_rol)
    
    if estado_laboral:
        query = query.filter(Personal.estado_laboral == estado_laboral)
    
    # Total
    total = query.count()
    total_pages = math.ceil(total / page_size)
    
    # Paginación
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()
    
    return PersonalListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/roles/")
def listar_roles(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lista roles disponibles para personal"""
    roles = db.query(Rol).filter(Rol.id != 1).all()  # Excluir Superadmin
    return [{"id_rol": r.id, "nombre_rol": r.nombre} for r in roles]


@router.get("/sin-terapia", response_model=List[dict])
def listar_personal_sin_terapia(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lista personal que no tiene terapia asignada"""
    from app.models.usuario import Usuario
    from app.models.terapia import TerapiaPersonal
    
    # Subconsulta para obtener IDs de personal con terapia asignada
    subquery = db.query(TerapiaPersonal.personal_id).filter(
        TerapiaPersonal.activo == 1
    ).distinct()
    
    # Personal sin terapia asignada (usando nombres directamente de Personal en lugar de Usuario)
    personal_sin_terapia = db.query(
        Personal.id.label('id_personal'),
        Personal.nombres,
        Personal.apellido_paterno,
        Personal.apellido_materno,
        Personal.especialidad_principal
    ).filter(
        Personal.id.notin_(subquery),
        Personal.estado_laboral == EstadoLaboral.ACTIVO
    ).all()
    
    resultado = []
    for row in personal_sin_terapia:
        nombre_completo = f"{row.nombres} {row.apellido_paterno}"
        if row.apellido_materno:
            nombre_completo += f" {row.apellido_materno}"
        
        resultado.append({
            "id_personal": row.id_personal,
            "nombre_completo": nombre_completo,
            "especialidad": row.especialidad_principal
        })
    
    return resultado


@router.get("/por-terapia/{terapia_id}", response_model=List[dict])
def obtener_terapeutas_por_terapia(
    terapia_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene los terapeutas especializados en una terapia específica"""
    from app.models.terapia import TerapiaPersonal
    
    terapeutas = db.query(Personal).join(
        TerapiaPersonal,
        TerapiaPersonal.personal_id == Personal.id
    ).filter(
        TerapiaPersonal.terapia_id == terapia_id,
        TerapiaPersonal.activo == 1,
        Personal.estado_laboral == EstadoLaboral.ACTIVO
    ).all()
    
    resultado = []
    for terapeuta in terapeutas:
        nombre_completo = f"{terapeuta.nombres} {terapeuta.apellido_paterno}"
        if terapeuta.apellido_materno:
            nombre_completo += f" {terapeuta.apellido_materno}"
        
        resultado.append({
            "id": terapeuta.id,
            "nombres": terapeuta.nombres,
            "apellido_paterno": terapeuta.apellido_paterno,
            "apellido_materno": terapeuta.apellido_materno,
            "especialidad_principal": terapeuta.especialidad_principal,
            "nombre_completo": nombre_completo,
            "rating": terapeuta.rating or 0
        })
    
    return resultado


@router.get("/{id}", response_model=PersonalResponse)
def obtener_personal(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtiene detalle de un personal con sus horarios"""
    personal = db.query(Personal).filter(Personal.id == id).first()
    if not personal:
        raise HTTPException(status_code=404, detail="Personal no encontrado")
    return personal


@router.post("/", response_model=PersonalResponse)
def crear_personal(
    personal_data: PersonalCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crea un nuevo personal"""
    # Verificar RFC único
    if db.query(Personal).filter(Personal.rfc == personal_data.rfc).first():
        raise HTTPException(status_code=400, detail="RFC ya existe")
    
    # Verificar CURP único
    if db.query(Personal).filter(Personal.curp == personal_data.curp).first():
        raise HTTPException(status_code=400, detail="CURP ya existe")
    
    # Verificar rol existe
    rol = db.query(Rol).filter(Rol.id == personal_data.id_rol).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    personal = Personal(**personal_data.model_dump())
    db.add(personal)
    db.commit()
    db.refresh(personal)
    return personal


@router.put("/{id}", response_model=PersonalResponse)
def actualizar_personal(
    id: int,
    personal_data: PersonalUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Actualiza datos de un personal"""
    personal = db.query(Personal).filter(Personal.id == id).first()
    if not personal:
        raise HTTPException(status_code=404, detail="Personal no encontrado")
    
    update_data = personal_data.model_dump(exclude_unset=True)
    
    # Verificar RFC único si se actualiza
    if 'rfc' in update_data:
        existing = db.query(Personal).filter(
            Personal.rfc == update_data['rfc'],
            Personal.id != id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="RFC ya existe")
    
    # Verificar CURP único si se actualiza
    if 'curp' in update_data:
        existing = db.query(Personal).filter(
            Personal.curp == update_data['curp'],
            Personal.id != id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="CURP ya existe")
    
    # Verificar rol si se actualiza
    if 'id_rol' in update_data:
        rol = db.query(Rol).filter(Rol.id == update_data['id_rol']).first()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    for field, value in update_data.items():
        setattr(personal, field, value)
    
    db.commit()
    db.refresh(personal)
    return personal


@router.patch("/{id}/estado")
def cambiar_estado(
    id: int,
    estado: EstadoLaboral = Query(..., description="Nuevo estado laboral"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Cambia el estado laboral (ACTIVO/VACACIONES/INACTIVO)"""
    personal = db.query(Personal).filter(Personal.id == id).first()
    if not personal:
        raise HTTPException(status_code=404, detail="Personal no encontrado")
    
    personal.estado_laboral = estado
    db.commit()
    db.refresh(personal)
    return {"id": personal.id, "estado_laboral": personal.estado_laboral}


@router.delete("/{id}")
def eliminar_personal(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Inactiva un personal (soft delete)"""
    personal = db.query(Personal).filter(Personal.id == id).first()
    if not personal:
        raise HTTPException(status_code=404, detail="Personal no encontrado")
    
    personal.estado_laboral = EstadoLaboral.INACTIVO
    db.commit()
    return {"message": "Personal inactivado correctamente"}


# ========== HORARIOS ==========
@router.get("/{id_personal}/horarios/", response_model=List[HorarioResponse])
def listar_horarios(
    id_personal: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lista horarios de un personal"""
    personal = db.query(Personal).filter(Personal.id == id_personal).first()
    if not personal:
        raise HTTPException(status_code=404, detail="Personal no encontrado")
    
    horarios = db.query(PersonalHorario).filter(
        PersonalHorario.id_personal == id_personal
    ).order_by(PersonalHorario.dia_semana, PersonalHorario.hora_inicio).all()
    
    return horarios


@router.post("/{id_personal}/horarios/", response_model=HorarioResponse)
def crear_horario(
    id_personal: int,
    horario_data: HorarioCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crea un horario para un personal"""
    personal = db.query(Personal).filter(Personal.id == id_personal).first()
    if not personal:
        raise HTTPException(status_code=404, detail="Personal no encontrado")
    
    # Verificar que no haya solapamiento de horarios
    horarios_existentes = db.query(PersonalHorario).filter(
        PersonalHorario.id_personal == id_personal,
        PersonalHorario.dia_semana == horario_data.dia_semana
    ).all()
    
    for h in horarios_existentes:
        if not (horario_data.hora_fin <= h.hora_inicio or horario_data.hora_inicio >= h.hora_fin):
            raise HTTPException(status_code=400, detail="Horario se solapa con otro existente")
    
    horario = PersonalHorario(**horario_data.model_dump())
    db.add(horario)
    db.commit()
    db.refresh(horario)
    return horario


@router.put("/horarios/{id}", response_model=HorarioResponse)
def actualizar_horario(
    id: int,
    horario_data: HorarioUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Actualiza un horario"""
    horario = db.query(PersonalHorario).filter(PersonalHorario.id == id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    
    update_data = horario_data.model_dump(exclude_unset=True)
    
    # Validar solapamiento si se actualizan horas o día
    if 'dia_semana' in update_data or 'hora_inicio' in update_data or 'hora_fin' in update_data:
        dia = update_data.get('dia_semana', horario.dia_semana)
        hora_inicio = update_data.get('hora_inicio', horario.hora_inicio)
        hora_fin = update_data.get('hora_fin', horario.hora_fin)
        
        horarios_existentes = db.query(PersonalHorario).filter(
            PersonalHorario.id_personal == horario.id_personal,
            PersonalHorario.dia_semana == dia,
            PersonalHorario.id != id
        ).all()
        
        for h in horarios_existentes:
            if not (hora_fin <= h.hora_inicio or hora_inicio >= h.hora_fin):
                raise HTTPException(status_code=400, detail="Horario se solapa con otro existente")
    
    for field, value in update_data.items():
        setattr(horario, field, value)
    
    db.commit()
    db.refresh(horario)
    return horario


@router.delete("/horarios/{id}")
def eliminar_horario(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Elimina un horario"""
    horario = db.query(PersonalHorario).filter(PersonalHorario.id == id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    
    db.delete(horario)
    db.commit()
    return {"message": "Horario eliminado correctamente"}
