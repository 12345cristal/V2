from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Optional
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

from app.db.session import get_db
from app.models.historial import Historial, AsistenciaMensual, EvolucionObjetivo, FrecuenciaTerapia
from app.models.sesion import Sesion, EstadoSesion
from app.models.paciente import Paciente
from pydantic import BaseModel

router = APIRouter(prefix="/padre/historial", tags=["Padre - Historial"])

# ==================== MODELOS ====================

class AsistenciaMesResponse(BaseModel):
    mes: str
    asistidas: int
    canceladas: int
    porcentajeAsistencia: int
    
    class Config:
        from_attributes = True

class EvolucionObjetivoResponse(BaseModel):
    fecha: str
    objetivo: str
    valor: int
    observaciones: Optional[str] = None
    
    class Config:
        from_attributes = True

class FrecuenciaTerapiaResponse(BaseModel):
    terapia: str
    sesionesPorSemana: int
    totalSesiones: int
    
    class Config:
        from_attributes = True

class SesionesVsCanceladasResponse(BaseModel):
    realizadas: int
    canceladas: int
    porcentajeRealizacion: int

class EstadisticasGeneralesResponse(BaseModel):
    duracionPromedio: int
    terapeuta: str
    inicioTerapia: str
    evaluacionGeneral: int

class HistorialResumenResponse(BaseModel):
    hijoId: int
    periodo: str
    asistenciaMensual: list
    sesionesVsCanceladas: dict
    evolucionObjetivos: list
    frecuenciaTerapias: list
    estadisticasGenerales: dict

# ==================== FUNCIONES AUXILIARES ====================

def calcular_estadisticas(db: Session, hijo_id: int) -> dict:
    """Calcula estadísticas del historial."""
    sesiones = db.query(Sesion).filter(Sesion.hijo_id == hijo_id).all()
    
    total_sesiones = len(sesiones)
    completadas = sum(1 for s in sesiones if s.estado == EstadoSesion.COMPLETADA)
    canceladas = sum(1 for s in sesiones if s.estado == EstadoSesion.CANCELADA)
    
    porcentaje = round((completadas / total_sesiones * 100), 2) if total_sesiones > 0 else 0
    
    return {
        "realizadas": completadas,
        "canceladas": canceladas,
        "total": total_sesiones,
        "porcentajeRealizacion": porcentaje
    }

def generar_pdf_historial(historial: Historial, nombre_hijo: str) -> bytes:
    """Genera PDF del historial."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        'Titulo',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#007bff'),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    story = []
    story.append(Paragraph(f"📊 Historial Terapéutico", titulo_style))
    story.append(Paragraph(f"Paciente: <b>{nombre_hijo}</b>", styles['Normal']))
    story.append(Paragraph(f"Fecha de reporte: <b>{datetime.now().strftime('%d/%m/%Y')}</b>", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Estadísticas generales
    story.append(Paragraph("Estadísticas Generales", styles['Heading2']))
    stats_data = [
        ["Duración promedio sesión", f"{historial.duracion_promedio_sesion} minutos"],
        ["Evaluación general", f"{historial.evaluacion_general}/10"],
        ["Terapeuta responsable", historial.terapeuta_responsable or "N/A"],
        ["Inicio de terapia", historial.fecha_inicio_terapia.strftime('%d/%m/%Y')]
    ]
    stats_table = Table(stats_data, colWidths=[2.5*inch, 2.5*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Asistencia mensual
    story.append(Paragraph("Asistencia por Mes", styles['Heading2']))
    asistencia_data = [["Mes", "Asistidas", "Canceladas", "% Asistencia"]]
    for asistencia in historial.asistencias:
        porcentaje = round((asistencia.asistidas / (asistencia.asistidas + asistencia.canceladas) * 100), 0) if (asistencia.asistidas + asistencia.canceladas) > 0 else 0
        asistencia_data.append([
            asistencia.mes,
            str(asistencia.asistidas),
            str(asistencia.canceladas),
            f"{int(porcentaje)}%"
        ])
    
    asistencia_table = Table(asistencia_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1.5*inch])
    asistencia_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(asistencia_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Frecuencia de terapias
    story.append(Paragraph("Frecuencia de Terapias", styles['Heading2']))
    freq_data = [["Tipo de Terapia", "Sesiones/Semana", "Total"]]
    for freq in historial.frecuencias:
        freq_data.append([freq.tipo_terapia, str(freq.sesiones_por_semana), str(freq.total_sesiones)])
    
    freq_table = Table(freq_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
    freq_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(freq_table)
    story.append(PageBreak())
    
    # Evolución de objetivos
    story.append(Paragraph("Evolución de Objetivos", styles['Heading2']))
    for evo in historial.evoluciones:
        estrellas = "★" * evo.valor + "☆" * (5 - evo.valor)
        evo_text = f"<b>{evo.objetivo}</b><br/>Fecha: {evo.fecha.strftime('%d/%m/%Y')} | {estrellas} ({evo.valor}/5)"
        if evo.observaciones:
            evo_text += f"<br/><i>{evo.observaciones}</i>"
        story.append(Paragraph(evo_text, styles['Normal']))
        story.append(Spacer(1, 0.15*inch))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# ==================== ENDPOINTS ====================

@router.get("/{hijo_id}")
def get_historial(hijo_id: int, db: Session = Depends(get_db)):
    """Obtiene el historial de un hijo."""
    hijo = db.query(Paciente).filter(Paciente.id == hijo_id).first()
    if not hijo:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    
    historial = db.query(Historial).filter(Historial.hijo_id == hijo_id).options(
        joinedload(Historial.asistencias),
        joinedload(Historial.evoluciones),
        joinedload(Historial.frecuencias)
    ).first()
    
    if not historial:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    
    # Calcular estadísticas en tiempo real
    stats = calcular_estadisticas(db, hijo_id)
    
    return {
        "hijoId": hijo_id,
        "periodo": "Últimos 6 meses",
        "asistenciaMensual": [
            {
                "mes": a.mes,
                "asistidas": a.asistidas,
                "canceladas": a.canceladas,
                "porcentajeAsistencia": round((a.asistidas / (a.asistidas + a.canceladas) * 100), 0) if (a.asistidas + a.canceladas) > 0 else 0
            }
            for a in historial.asistencias
        ],
        "sesionesVsCanceladas": stats,
        "evolucionObjetivos": [
            {
                "fecha": e.fecha.isoformat(),
                "objetivo": e.objetivo,
                "valor": e.valor,
                "observaciones": e.observaciones
            }
            for e in historial.evoluciones
        ],
        "frecuenciaTerapias": [
            {
                "terapia": f.tipo_terapia,
                "sesionesPorSemana": f.sesiones_por_semana,
                "totalSesiones": f.total_sesiones
            }
            for f in historial.frecuencias
        ],
        "estadisticasGenerales": {
            "duracionPromedio": historial.duracion_promedio_sesion,
            "terapeuta": historial.terapeuta_responsable or "Equipo multidisciplinario",
            "inicioTerapia": historial.fecha_inicio_terapia.isoformat(),
            "evaluacionGeneral": historial.evaluacion_general
        }
    }

@router.get("/{hijo_id}/reporte")
def descargar_reporte(hijo_id: int, db: Session = Depends(get_db)):
    """Descarga reporte en PDF."""
    hijo = db.query(Paciente).filter(Paciente.id == hijo_id).first()
    if not hijo:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    
    historial = db.query(Historial).filter(Historial.hijo_id == hijo_id).options(
        joinedload(Historial.asistencias),
        joinedload(Historial.evoluciones),
        joinedload(Historial.frecuencias)
    ).first()
    
    if not historial:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    
    pdf_bytes = generar_pdf_historial(historial, hijo.nombre)
    
    return {
        "content": pdf_bytes,
        "filename": f"historial-{hijo.nombre}-{datetime.now().strftime('%Y%m%d')}.pdf"
    }