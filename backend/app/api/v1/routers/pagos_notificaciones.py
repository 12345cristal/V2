from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models.pago import Pago, EstadoPago
from app.models.usuario import Usuario
from app.models.paciente import Paciente
from pydantic import BaseModel

router = APIRouter(prefix="/pagos", tags=["Pagos"])

# ==================== MODELOS ====================

class PagoResponse(BaseModel):
    id: int
    padreId: int
    hijoId: int
    monto: float
    concepto: str
    estado: str
    fechaVencimiento: str
    fechaPago: Optional[str] = None
    metodoPago: Optional[str] = None
    
    class Config:
        from_attributes = True

# ==================== ENDPOINTS ====================

@router.get("/padre/{padre_id}", response_model=List[PagoResponse])
def get_pagos_padre(padre_id: int, db: Session = Depends(get_db)):
    """Obtiene todos los pagos de un padre."""
    padre = db.query(Usuario).filter(Usuario.id == padre_id).first()
    if not padre:
        raise HTTPException(status_code=404, detail="Padre no encontrado")
    
    pagos = db.query(Pago).filter(Pago.padre_id == padre_id).options(
        joinedload(Pago.padre),
        joinedload(Pago.hijo)
    ).order_by(Pago.fecha_vencimiento.desc()).all()
    
    return [
        {
            "id": p.id,
            "padreId": p.padre_id,
            "hijoId": p.hijo_id,
            "monto": p.monto,
            "concepto": p.concepto,
            "estado": p.estado.value,
            "fechaVencimiento": p.fecha_vencimiento.isoformat(),
            "fechaPago": p.fecha_pago.isoformat() if p.fecha_pago else None,
            "metodoPago": p.metodo_pago
        }
        for p in pagos
    ]

@router.get("/hijo/{hijo_id}/pendientes", response_model=List[PagoResponse])
def get_pagos_pendientes_hijo(hijo_id: int, db: Session = Depends(get_db)):
    """Obtiene pagos pendientes de un hijo."""
    hijo = db.query(Paciente).filter(Paciente.id == hijo_id).first()
    if not hijo:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    
    pagos = db.query(Pago).filter(
        Pago.hijo_id == hijo_id,
        Pago.estado.in_([EstadoPago.PENDIENTE, EstadoPago.ATRASADO])
    ).options(
        joinedload(Pago.padre),
        joinedload(Pago.hijo)
    ).order_by(Pago.fecha_vencimiento).all()
    
    return [
        {
            "id": p.id,
            "padreId": p.padre_id,
            "hijoId": p.hijo_id,
            "monto": p.monto,
            "concepto": p.concepto,
            "estado": p.estado.value,
            "fechaVencimiento": p.fecha_vencimiento.isoformat(),
            "fechaPago": p.fecha_pago.isoformat() if p.fecha_pago else None,
            "metodoPago": p.metodo_pago
        }
        for p in pagos
    ]

@router.post("/verificar-pendientes")
def verificar_pagos_pendientes(db: Session = Depends(get_db)):
    """Verifica y actualiza pagos atrasados, envía notificaciones."""
    ahora = datetime.now()
    
    # Actualizar pagos vencidos a atrasados
    pagos_vencidos = db.query(Pago).filter(
        Pago.estado == EstadoPago.PENDIENTE,
        Pago.fecha_vencimiento < ahora
    ).all()
    
    for pago in pagos_vencidos:
        pago.estado = EstadoPago.ATRASADO
    
    db.commit()
    
    # Notificar
    from app.api.v1.routers.notificaciones import notificar_padre, MetadataNotificacion
    
    for pago in pagos_vencidos:
        notificar_padre(
            db=db,
            padre_id=pago.padre_id,
            hijo_id=pago.hijo_id,
            tipo="PAGO_ATRASADO",
            mensaje=f"⚠️ Tienes un pago atrasado de ${pago.monto:.2f} por {pago.concepto}",
            metadata=MetadataNotificacion(
                relacionadoId=pago.id,
                relacionadoTipo="pago",
                prioridad="alta"
            )
        )
    
    # Notificar sobre pagos próximos a vencer
    pagos_proximos = db.query(Pago).filter(
        Pago.estado == EstadoPago.PENDIENTE,
        Pago.fecha_vencimiento > ahora,
        Pago.fecha_vencimiento <= ahora + timedelta(days=5)
    ).all()
    
    for pago in pagos_proximos:
        dias = (pago.fecha_vencimiento - ahora).days
        notificar_padre(
            db=db,
            padre_id=pago.padre_id,
            hijo_id=pago.hijo_id,
            tipo="PAGO_PROXIMO",
            mensaje=f"💳 Recordatorio: Tienes un pago de ${pago.monto:.2f} por {pago.concepto}. Vence en {dias} días.",
            metadata=MetadataNotificacion(
                relacionadoId=pago.id,
                relacionadoTipo="pago",
                prioridad="media"
            )
        )
    
    return {
        "pagos_atrasados": len(pagos_vencidos),
        "pagos_proximos": len(pagos_proximos),
        "total_procesados": len(pagos_vencidos) + len(pagos_proximos)
    }

@router.put("/{pago_id}/registrar-pago")
def registrar_pago(
    pago_id: int,
    metodo_pago: str,
    referencia: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Registra un pago realizado."""
    pago = db.query(Pago).filter(Pago.id == pago_id).first()
    
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    
    pago.estado = EstadoPago.PAGADO
    pago.fecha_pago = datetime.now()
    pago.metodo_pago = metodo_pago
    pago.referencia = referencia
    
    db.commit()
    db.refresh(pago)
    
    # Notificar
    from app.api.v1.routers.notificaciones import notificar_padre, MetadataNotificacion
    
    notificar_padre(
        db=db,
        padre_id=pago.padre_id,
        hijo_id=pago.hijo_id,
        tipo="NUEVO_RECURSO",  # Usar como confirmación de pago
        mensaje=f"✅ Pago de ${pago.monto:.2f} registrado correctamente",
        metadata=MetadataNotificacion(
            relacionadoId=pago.id,
            relacionadoTipo="pago",
            prioridad="media"
        )
    )
    
    return {
        "id": pago.id,
        "estado": pago.estado.value,
        "fechaPago": pago.fecha_pago.isoformat()
    }