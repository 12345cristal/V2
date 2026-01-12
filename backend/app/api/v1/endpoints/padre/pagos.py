# app/api/v1/endpoints/padre/pagos.py
"""
Router para gestión de Pagos desde el módulo Padre
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db_session, require_padre
from app.models.usuario import Usuario
from app.models.tutor import Tutor
from app.schemas.padre import InformacionPago, Pago, HistorialPago, PlanPago


router = APIRouter()


@router.get("/pagos/{padre_id}/info", response_model=InformacionPago)
async def obtener_info_pago(
    padre_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene información del plan y saldo del padre
    """
    # Verificar permisos
    tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
    if not tutor or tutor.id != padre_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a esta información"
        )
    
    # TODO: Implementar lógica real de pagos
    plan = PlanPago(
        nombre="Plan Básico",
        monto_mensual=5000.0,
        fecha_corte=15,
        terapias_incluidas=3,
        sesiones_mes=12
    )
    
    return InformacionPago(
        plan=plan,
        saldo_actual=0.0,
        ultimo_pago=None,
        proximo_vencimiento=None,
        dias_para_vencimiento=None,
        meses_adeudados=0
    )


@router.get("/pagos/{padre_id}/historial", response_model=List[Pago])
async def obtener_historial_pagos(
    padre_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene historial de pagos del padre
    """
    # Verificar permisos
    tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
    if not tutor or tutor.id != padre_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a esta información"
        )
    
    # TODO: Implementar lógica real
    return []


@router.get("/pagos/{padre_id}/historial/{pago_id}/comprobante")
async def descargar_comprobante(
    padre_id: int,
    pago_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Descarga comprobante de pago
    """
    # Verificar permisos
    tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
    if not tutor or tutor.id != padre_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a esta información"
        )
    
    # TODO: Implementar descarga de comprobante
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidad en desarrollo"
    )


@router.get("/pagos/{padre_id}/reporte")
async def descargar_reporte_pagos(
    padre_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Descarga reporte de pagos en PDF
    """
    # Verificar permisos
    tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
    if not tutor or tutor.id != padre_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a esta información"
        )
    
    # TODO: Implementar generación de PDF
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Funcionalidad en desarrollo"
    )
