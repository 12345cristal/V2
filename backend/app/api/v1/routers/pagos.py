# app/api/v1/routers/pagos.py
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from app.db.session import get_db
from app.models.pago import Pago
from app.models.plan_pago import PlanPago
from app.models.usuario import Usuario
from app.schemas.pago import (
    PagoCreate,
    PagoUpdate,
    PagoResponse,
    PagoListItem,
    HistorialPagosResponse
)

router = APIRouter(prefix="/pagos", tags=["Pagos"])


# ==================== FUNCIONES AUXILIARES ====================

def construir_respuesta_pago(pago: Pago) -> dict:
    """Construye diccionario de respuesta para un pago"""
    return {
        "id": pago.id,
        "plan_id": pago.plan_id,
        "usuario_id": pago.usuario_id,
        "monto": pago.monto,
        "metodo": pago.metodo,
        "referencia": pago.referencia,
        "es_abono": pago.es_abono,
        "fecha_pago": pago.fecha_pago,
        "fecha_registro": pago.fecha_registro,
        "comprobante_url": pago.comprobante_url,
        "estado": pago.estado,
        "observaciones": pago.observaciones,
        "plan_nombre": pago.plan.nombre_plan if pago.plan else None,
        "nino_nombre": f"{pago.plan.nino.nombre} {pago.plan.nino.apellido_paterno}" if pago.plan and pago.plan.nino else None,
        "usuario_nombre": f"{pago.usuario.nombres} {pago.usuario.apellido_paterno}" if pago.usuario else None
    }


# ==================== ENDPOINTS ====================

@router.get("", response_model=List[PagoListItem])
def listar_pagos(
    plan_id: Optional[int] = Query(None, description="Filtrar por plan"),
    usuario_id: Optional[int] = Query(None, description="Filtrar por usuario"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Lista todos los pagos con filtros opcionales"""
    query = db.query(Pago).options(
        joinedload(Pago.plan).joinedload(PlanPago.nino),
        joinedload(Pago.usuario)
    )
    
    # Aplicar filtros
    if plan_id is not None:
        query = query.filter(Pago.plan_id == plan_id)
    if usuario_id is not None:
        query = query.filter(Pago.usuario_id == usuario_id)
    if estado:
        query = query.filter(Pago.estado == estado)
    
    # Ordenar por fecha de pago descendente
    query = query.order_by(desc(Pago.fecha_pago))
    
    pagos = query.offset(skip).limit(limit).all()
    
    # Construir respuesta
    result = []
    for pago in pagos:
        result.append({
            "id": pago.id,
            "plan_id": pago.plan_id,
            "plan_nombre": pago.plan.nombre_plan if pago.plan else None,
            "monto": pago.monto,
            "metodo": pago.metodo,
            "fecha_pago": pago.fecha_pago,
            "estado": pago.estado,
            "nino_nombre": f"{pago.plan.nino.nombre} {pago.plan.nino.apellido_paterno}" if pago.plan and pago.plan.nino else None
        })
    
    return result


@router.get("/plan/{plan_id}", response_model=List[PagoListItem])
def listar_pagos_plan(
    plan_id: int,
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    db: Session = Depends(get_db)
):
    """Lista todos los pagos de un plan específico"""
    # Verificar que el plan existe
    plan = db.query(PlanPago).filter(PlanPago.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de pago no encontrado")
    
    query = db.query(Pago).options(
        joinedload(Pago.plan).joinedload(PlanPago.nino),
        joinedload(Pago.usuario)
    ).filter(Pago.plan_id == plan_id)
    
    if estado:
        query = query.filter(Pago.estado == estado)
    
    query = query.order_by(desc(Pago.fecha_pago))
    
    pagos = query.all()
    
    # Construir respuesta
    result = []
    for pago in pagos:
        result.append({
            "id": pago.id,
            "plan_id": pago.plan_id,
            "plan_nombre": pago.plan.nombre_plan if pago.plan else None,
            "monto": pago.monto,
            "metodo": pago.metodo,
            "fecha_pago": pago.fecha_pago,
            "estado": pago.estado,
            "nino_nombre": f"{pago.plan.nino.nombre} {pago.plan.nino.apellido_paterno}" if pago.plan and pago.plan.nino else None
        })
    
    return result


@router.get("/{pago_id}", response_model=PagoResponse)
def obtener_pago(pago_id: int, db: Session = Depends(get_db)):
    """Obtiene un pago por ID"""
    pago = db.query(Pago).options(
        joinedload(Pago.plan).joinedload(PlanPago.nino),
        joinedload(Pago.usuario)
    ).filter(Pago.id == pago_id).first()
    
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    
    return construir_respuesta_pago(pago)


@router.post("", response_model=PagoResponse, status_code=201)
def registrar_pago(pago_data: PagoCreate, db: Session = Depends(get_db)):
    """Registra un nuevo pago"""
    # Validar plan si se proporciona
    if pago_data.plan_id:
        plan = db.query(PlanPago).filter(PlanPago.id == pago_data.plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Plan de pago no encontrado")
        
        # Verificar que el plan permite abonos si es un abono
        if pago_data.es_abono == 1 and plan.permite_abonos == 0:
            raise HTTPException(
                status_code=400,
                detail="El plan no permite abonos, debe pagarse completo"
            )
    
    # Validar usuario si se proporciona
    if pago_data.usuario_id:
        usuario = db.query(Usuario).filter(Usuario.id == pago_data.usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Crear pago
    nuevo_pago = Pago(
        plan_id=pago_data.plan_id,
        usuario_id=pago_data.usuario_id,
        monto=pago_data.monto,
        metodo=pago_data.metodo,
        referencia=pago_data.referencia,
        es_abono=pago_data.es_abono,
        comprobante_url=pago_data.comprobante_url,
        observaciones=pago_data.observaciones,
        estado='COMPLETADO'
    )
    
    db.add(nuevo_pago)
    db.flush()  # Para obtener el ID
    
    # Si está asociado a un plan, actualizar el plan
    if pago_data.plan_id:
        plan = db.query(PlanPago).filter(PlanPago.id == pago_data.plan_id).first()
        if plan:
            plan.actualizar_monto_pagado(db)
    
    db.commit()
    db.refresh(nuevo_pago)
    
    return obtener_pago(nuevo_pago.id, db)


@router.put("/{pago_id}", response_model=PagoResponse)
def actualizar_pago(
    pago_id: int,
    pago_data: PagoUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un pago existente"""
    pago = db.query(Pago).filter(Pago.id == pago_id).first()
    
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    
    # Actualizar campos proporcionados
    update_data = pago_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pago, key, value)
    
    db.commit()
    db.refresh(pago)
    
    # Si se cambió el estado, recalcular el plan
    if "estado" in update_data and pago.plan_id:
        plan = db.query(PlanPago).filter(PlanPago.id == pago.plan_id).first()
        if plan:
            plan.actualizar_monto_pagado(db)
            db.commit()
    
    return obtener_pago(pago_id, db)


@router.delete("/{pago_id}", status_code=204)
def eliminar_pago(pago_id: int, db: Session = Depends(get_db)):
    """Elimina un pago"""
    pago = db.query(Pago).filter(Pago.id == pago_id).first()
    
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    
    plan_id = pago.plan_id
    
    db.delete(pago)
    db.commit()
    
    # Recalcular el plan si estaba asociado
    if plan_id:
        plan = db.query(PlanPago).filter(PlanPago.id == plan_id).first()
        if plan:
            plan.actualizar_monto_pagado(db)
            db.commit()
    
    return None


@router.get("/usuario/{usuario_id}/historial", response_model=HistorialPagosResponse)
def obtener_historial_usuario(
    usuario_id: int,
    limite: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Obtiene el historial de pagos de un usuario"""
    # Verificar que el usuario existe
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Obtener pagos
    pagos = db.query(Pago).options(
        joinedload(Pago.plan).joinedload(PlanPago.nino)
    ).filter(
        Pago.usuario_id == usuario_id
    ).order_by(
        desc(Pago.fecha_pago)
    ).limit(limite).all()
    
    # Construir lista de pagos
    lista_pagos = []
    for pago in pagos:
        lista_pagos.append({
            "id": pago.id,
            "plan_id": pago.plan_id,
            "plan_nombre": pago.plan.nombre_plan if pago.plan else None,
            "monto": pago.monto,
            "metodo": pago.metodo,
            "fecha_pago": pago.fecha_pago,
            "estado": pago.estado,
            "nino_nombre": f"{pago.plan.nino.nombre} {pago.plan.nino.apellido_paterno}" if pago.plan and pago.plan.nino else None
        })
    
    # Calcular totales
    total_pagos = len(pagos)
    monto_total = sum(float(pago.monto) for pago in pagos if pago.estado == 'COMPLETADO')
    ultimo_pago = pagos[0].fecha_pago if pagos else None
    
    return {
        "pagos": lista_pagos,
        "total_pagos": total_pagos,
        "monto_total": Decimal(str(monto_total)),
        "ultimo_pago": ultimo_pago
    }
