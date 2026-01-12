# app/api/v1/routers/planes_pago.py
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional
from decimal import Decimal

from app.db.session import get_db
from app.models.plan_pago import PlanPago
from app.models.pago import Pago
from app.models.nino import Nino
from app.schemas.plan_pago import (
    PlanPagoCreate,
    PlanPagoUpdate,
    PlanPagoResponse,
    PlanPagoListItem,
    SaldoPendienteResponse
)

router = APIRouter(prefix="/planes-pago", tags=["Planes de Pago"])


# ==================== FUNCIONES AUXILIARES ====================

def construir_respuesta_plan(plan: PlanPago, incluir_stats: bool = True) -> dict:
    """Construye diccionario de respuesta para un plan de pago"""
    response = {
        "id": plan.id,
        "nino_id": plan.nino_id,
        "nombre_plan": plan.nombre_plan,
        "monto_total": plan.monto_total,
        "permite_abonos": plan.permite_abonos,
        "monto_pagado": plan.monto_pagado,
        "saldo_pendiente": plan.saldo_pendiente,
        "fecha_inicio": plan.fecha_inicio,
        "fecha_fin": plan.fecha_fin,
        "fecha_creacion": plan.fecha_creacion,
        "activo": plan.activo,
        "estado": plan.estado,
        "nino_nombre": plan.nino.nombre if plan.nino else None,
        "nino_apellido": f"{plan.nino.apellido_paterno}" if plan.nino else None
    }
    
    if incluir_stats:
        response["numero_pagos"] = len(plan.pagos) if plan.pagos else 0
    
    return response


# ==================== ENDPOINTS ====================

@router.get("", response_model=List[PlanPagoListItem])
def listar_planes(
    nino_id: Optional[int] = Query(None, description="Filtrar por niño"),
    activo: Optional[int] = Query(None, description="Filtrar por estado activo (0/1)"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Lista todos los planes de pago con filtros opcionales"""
    query = db.query(PlanPago).options(joinedload(PlanPago.nino))
    
    # Aplicar filtros
    if nino_id is not None:
        query = query.filter(PlanPago.nino_id == nino_id)
    if activo is not None:
        query = query.filter(PlanPago.activo == activo)
    if estado:
        query = query.filter(PlanPago.estado == estado)
    
    # Ordenar por fecha de creación descendente
    query = query.order_by(PlanPago.fecha_creacion.desc())
    
    planes = query.offset(skip).limit(limit).all()
    
    # Construir respuesta
    result = []
    for plan in planes:
        result.append({
            "id": plan.id,
            "nino_id": plan.nino_id,
            "nino_nombre": f"{plan.nino.nombre} {plan.nino.apellido_paterno}" if plan.nino else "Sin nombre",
            "nombre_plan": plan.nombre_plan,
            "monto_total": plan.monto_total,
            "monto_pagado": plan.monto_pagado,
            "saldo_pendiente": plan.saldo_pendiente,
            "estado": plan.estado,
            "activo": plan.activo,
            "fecha_inicio": plan.fecha_inicio,
            "fecha_fin": plan.fecha_fin
        })
    
    return result


@router.get("/nino/{nino_id}", response_model=List[PlanPagoListItem])
def listar_planes_nino(
    nino_id: int,
    activo: Optional[int] = Query(None, description="Filtrar por activo"),
    db: Session = Depends(get_db)
):
    """Lista todos los planes de pago de un niño específico"""
    # Verificar que el niño existe
    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    if not nino:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    
    query = db.query(PlanPago).options(
        joinedload(PlanPago.nino)
    ).filter(PlanPago.nino_id == nino_id)
    
    if activo is not None:
        query = query.filter(PlanPago.activo == activo)
    
    query = query.order_by(PlanPago.fecha_creacion.desc())
    
    planes = query.all()
    
    # Construir respuesta
    result = []
    for plan in planes:
        result.append({
            "id": plan.id,
            "nino_id": plan.nino_id,
            "nino_nombre": f"{plan.nino.nombre} {plan.nino.apellido_paterno}",
            "nombre_plan": plan.nombre_plan,
            "monto_total": plan.monto_total,
            "monto_pagado": plan.monto_pagado,
            "saldo_pendiente": plan.saldo_pendiente,
            "estado": plan.estado,
            "activo": plan.activo,
            "fecha_inicio": plan.fecha_inicio,
            "fecha_fin": plan.fecha_fin
        })
    
    return result


@router.get("/{plan_id}", response_model=PlanPagoResponse)
def obtener_plan(plan_id: int, db: Session = Depends(get_db)):
    """Obtiene un plan de pago por ID"""
    plan = db.query(PlanPago).options(
        joinedload(PlanPago.nino),
        joinedload(PlanPago.pagos)
    ).filter(PlanPago.id == plan_id).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de pago no encontrado")
    
    return construir_respuesta_plan(plan)


@router.post("", response_model=PlanPagoResponse, status_code=201)
def crear_plan(plan_data: PlanPagoCreate, db: Session = Depends(get_db)):
    """Crea un nuevo plan de pago"""
    # Validar niño
    nino = db.query(Nino).filter(Nino.id == plan_data.nino_id).first()
    if not nino:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    
    # Crear plan
    nuevo_plan = PlanPago(
        nino_id=plan_data.nino_id,
        nombre_plan=plan_data.nombre_plan,
        monto_total=plan_data.monto_total,
        permite_abonos=plan_data.permite_abonos,
        fecha_inicio=plan_data.fecha_inicio,
        fecha_fin=plan_data.fecha_fin,
        monto_pagado=Decimal("0.00")
    )
    
    # Calcular saldo inicial
    nuevo_plan.calcular_saldo()
    
    db.add(nuevo_plan)
    db.commit()
    db.refresh(nuevo_plan)
    
    return obtener_plan(nuevo_plan.id, db)


@router.put("/{plan_id}", response_model=PlanPagoResponse)
def actualizar_plan(
    plan_id: int,
    plan_data: PlanPagoUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un plan de pago existente"""
    plan = db.query(PlanPago).filter(PlanPago.id == plan_id).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de pago no encontrado")
    
    # Actualizar campos proporcionados
    update_data = plan_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(plan, key, value)
    
    # Recalcular saldo si se modificó el monto total
    if "monto_total" in update_data:
        plan.calcular_saldo()
    
    db.commit()
    db.refresh(plan)
    
    return obtener_plan(plan_id, db)


@router.delete("/{plan_id}", status_code=204)
def eliminar_plan(plan_id: int, db: Session = Depends(get_db)):
    """Elimina (desactiva) un plan de pago"""
    plan = db.query(PlanPago).filter(PlanPago.id == plan_id).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de pago no encontrado")
    
    # Verificar que no tenga pagos asociados
    tiene_pagos = db.query(Pago).filter(Pago.plan_id == plan_id).count() > 0
    
    if tiene_pagos:
        # Si tiene pagos, solo desactivar
        plan.activo = 0
        plan.estado = 'CANCELADO'
        db.commit()
    else:
        # Si no tiene pagos, se puede eliminar
        db.delete(plan)
        db.commit()
    
    return None


@router.get("/{plan_id}/saldo", response_model=SaldoPendienteResponse)
def calcular_saldo(plan_id: int, db: Session = Depends(get_db)):
    """Calcula y retorna el saldo pendiente de un plan"""
    plan = db.query(PlanPago).filter(PlanPago.id == plan_id).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de pago no encontrado")
    
    # Actualizar monto pagado desde la BD
    plan.actualizar_monto_pagado(db)
    db.commit()
    db.refresh(plan)
    
    # Calcular porcentaje pagado
    porcentaje_pagado = (float(plan.monto_pagado) / float(plan.monto_total) * 100) if float(plan.monto_total) > 0 else 0
    
    return {
        "plan_id": plan.id,
        "monto_total": plan.monto_total,
        "monto_pagado": plan.monto_pagado,
        "saldo_pendiente": plan.saldo_pendiente,
        "porcentaje_pagado": round(porcentaje_pagado, 2)
    }


@router.post("/{plan_id}/recalcular", response_model=PlanPagoResponse)
def recalcular_plan(plan_id: int, db: Session = Depends(get_db)):
    """Recalcula el saldo de un plan basándose en los pagos registrados"""
    plan = db.query(PlanPago).options(
        joinedload(PlanPago.pagos)
    ).filter(PlanPago.id == plan_id).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de pago no encontrado")
    
    # Actualizar monto pagado y estado
    plan.actualizar_monto_pagado(db)
    
    db.commit()
    db.refresh(plan)
    
    return obtener_plan(plan_id, db)
