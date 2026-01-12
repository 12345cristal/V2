from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

router = APIRouter(prefix="/padre/historial", tags=["Padre - Historial"])

# ==================== MODELOS ====================

class AsistenciaMes(BaseModel):
    mes: str
    asistidas: int
    canceladas: int
    porcentajeAsistencia: int

class SesionesVsCanceladas(BaseModel):
    realizadas: int
    canceladas: int
    porcentajeRealizacion: int

class EvolucionObjetivo(BaseModel):
    fecha: str
    objetivo: str
    valor: int
    observaciones: Optional[str] = None

class FrecuenciaTerapia(BaseModel):
    terapia: str
    sesionesPorSemana: int
    totalSesiones: int

class EstadisticasGenerales(BaseModel):
    duracionPromedio: int
    terapeuta: str
    inicioTerapia: str
    evaluacionGeneral: int

class HistorialResumen(BaseModel):
    hijoId: int
    periodo: str
    asistenciaMensual: List[AsistenciaMes]
    sesionesVsCanceladas: SesionesVsCanceladas
    evolucionObjetivos: List[EvolucionObjetivo]
    frecuenciaTerapias: List[FrecuenciaTerapia]
    estadisticasGenerales: EstadisticasGenerales

# ==================== DATOS MOCK ====================

_historial_db: dict = {
    1: HistorialResumen(
        hijoId=1,
        periodo="Últimos 6 meses",
        asistenciaMensual=[
            AsistenciaMes(mes="Enero 2026", asistidas=4, canceladas=1, porcentajeAsistencia=80),
            AsistenciaMes(mes="Diciembre 2025", asistidas=5, canceladas=0, porcentajeAsistencia=100),
            AsistenciaMes(mes="Noviembre 2025", asistidas=4, canceladas=1, porcentajeAsistencia=80),
            AsistenciaMes(mes="Octubre 2025", asistidas=3, canceladas=2, porcentajeAsistencia=60),
            AsistenciaMes(mes="Septiembre 2025", asistidas=5, canceladas=0, porcentajeAsistencia=100),
            AsistenciaMes(mes="Agosto 2025", asistidas=4, canceladas=1, porcentajeAsistencia=80),
        ],
        sesionesVsCanceladas=SesionesVsCanceladas(realizadas=25, canceladas=5, porcentajeRealizacion=83),
        evolucionObjetivos=[
            EvolucionObjetivo(
                fecha="2025-08-01",
                objetivo="Mejorar pronunciación",
                valor=2,
                observaciones="Inicio de terapia logopédica"
            ),
            EvolucionObjetivo(
                fecha="2025-10-01",
                objetivo="Mejorar pronunciación",
                valor=3,
                observaciones="Progreso notorio en fonemas específicos"
            ),
            EvolucionObjetivo(
                fecha="2026-01-01",
                objetivo="Mejorar pronunciación",
                valor=4,
                observaciones="Muy buen avance, seguir reforzando"
            ),
            EvolucionObjetivo(
                fecha="2025-09-01",
                objetivo="Aumentar vocabulario",
                valor=3,
                observaciones="Vocabulario activo en aumento"
            ),
            EvolucionObjetivo(
                fecha="2026-01-01",
                objetivo="Aumentar vocabulario",
                valor=5,
                observaciones="Objetivo alcanzado, muy buen desempeño"
            ),
        ],
        frecuenciaTerapias=[
            FrecuenciaTerapia(terapia="Logopedia", sesionesPorSemana=2, totalSesiones=14),
            FrecuenciaTerapia(terapia="Terapia Ocupacional", sesionesPorSemana=1, totalSesiones=7),
            FrecuenciaTerapia(terapia="Psicología", sesionesPorSemana=1, totalSesiones=7),
        ],
        estadisticasGenerales=EstadisticasGenerales(
            duracionPromedio=50,
            terapeuta="Equipo multidisciplinario",
            inicioTerapia="2025-08-15",
            evaluacionGeneral=8,
        ),
    )
}

# ==================== FUNCIONES AUXILIARES ====================

def generar_pdf(resumen: HistorialResumen, nombre_hijo: str) -> BytesIO:
    """Genera PDF del historial terapéutico."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        'Titulo',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#007bff'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )
    
    # Contenido
    story = []
    
    # Título
    story.append(Paragraph(f"📊 Historial Terapéutico", titulo_style))
    story.append(Paragraph(f"Paciente: <b>{nombre_hijo}</b>", styles['Normal']))
    story.append(Paragraph(f"Período: <b>{resumen.periodo}</b>", styles['Normal']))
    story.append(Paragraph(f"Fecha de reporte: <b>{datetime.now().strftime('%d/%m/%Y')}</b>", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Estadísticas Generales
    story.append(Paragraph("Estadísticas Generales", heading_style))
    stats = resumen.estadisticasGenerales
    stats_data = [
        ["Duración promedio sesión", f"{stats.duracionPromedio} minutos"],
        ["Evaluación general", f"{stats.evaluacionGeneral}/10"],
        ["Terapeuta responsable", stats.terapeuta],
        ["Inicio de terapia", stats.inicioTerapia],
    ]
    stats_table = Table(stats_data, colWidths=[2.5*inch, 2.5*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Asistencia Mensual
    story.append(Paragraph("Asistencia por Mes", heading_style))
    asistencia_data = [["Mes", "Asistidas", "Canceladas", "% Asistencia"]]
    for m in resumen.asistenciaMensual:
        asistencia_data.append([m.mes, str(m.asistidas), str(m.canceladas), f"{m.porcentajeAsistencia}%"])
    
    asistencia_table = Table(asistencia_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1.5*inch])
    asistencia_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
    ]))
    story.append(asistencia_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Sesiones realizadas vs canceladas
    story.append(Paragraph("Sesiones Realizadas vs Canceladas", heading_style))
    sesiones = resumen.sesionesVsCanceladas
    sesiones_text = f"""
    Total de sesiones realizadas: <b>{sesiones.realizadas}</b><br/>
    Total de sesiones canceladas: <b>{sesiones.canceladas}</b><br/>
    Porcentaje de realización: <b>{sesiones.porcentajeRealizacion}%</b>
    """
    story.append(Paragraph(sesiones_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Frecuencia de terapias
    story.append(Paragraph("Frecuencia de Terapias", heading_style))
    freq_data = [["Tipo de Terapia", "Sesiones/Semana", "Total de Sesiones"]]
    for f in resumen.frecuenciaTerapias:
        freq_data.append([f.terapia, str(f.sesionesPorSemana), str(f.totalSesiones)])
    
    freq_table = Table(freq_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
    freq_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
    ]))
    story.append(freq_table)
    story.append(PageBreak())
    
    # Evolución de objetivos
    story.append(Paragraph("Evolución de Objetivos", heading_style))
    for evo in resumen.evolucionObjetivos:
        fecha = datetime.fromisoformat(evo.fecha).strftime('%d/%m/%Y')
        estrellas = "★" * evo.valor + "☆" * (5 - evo.valor)
        evo_text = f"""
        <b>{evo.objetivo}</b><br/>
        Fecha: {fecha} | Progreso: {estrellas} ({evo.valor}/5)<br/>
        """
        if evo.observaciones:
            evo_text += f"<i>Observaciones: {evo.observaciones}</i>"
        
        story.append(Paragraph(evo_text, styles['Normal']))
        story.append(Spacer(1, 0.15*inch))
    
    # Firma
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("_" * 60, styles['Normal']))
    story.append(Paragraph("Firma del Terapeuta Responsable", styles['Normal']))
    story.append(Paragraph(f"Fecha: {datetime.now().strftime('%d de %B de %Y')}", styles['Normal']))
    
    # Generar PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

# ==================== ENDPOINTS ====================

@router.get("/{hijo_id}", response_model=HistorialResumen)
def get_historial(hijo_id: int):
    """Obtiene el historial y resumen de progreso de un hijo."""
    if hijo_id in _historial_db:
        return _historial_db[hijo_id]
    
    # Retorna datos por defecto si no existen
    return HistorialResumen(
        hijoId=hijo_id,
        periodo="Sin datos",
        asistenciaMensual=[],
        sesionesVsCanceladas=SesionesVsCanceladas(realizadas=0, canceladas=0, porcentajeRealizacion=0),
        evolucionObjetivos=[],
        frecuenciaTerapias=[],
        estadisticasGenerales=EstadisticasGenerales(
            duracionPromedio=0,
            terapeuta="N/A",
            inicioTerapia=datetime.now().isoformat(),
            evaluacionGeneral=0,
        ),
    )

@router.get("/{hijo_id}/reporte")
def descargar_reporte(hijo_id: int):
    """Descarga el reporte en PDF."""
    if hijo_id not in _historial_db:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    
    resumen = _historial_db[hijo_id]
    
    # Obtener nombre del hijo (necesitaría venir de BD)
    nombres_hijos = {
        1: "Juan Pérez García"
    }
    nombre_hijo = nombres_hijos.get(hijo_id, f"Paciente {hijo_id}")
    
    # Generar PDF
    pdf_buffer = generar_pdf(resumen, nombre_hijo)
    
    return {
        "content": pdf_buffer.getvalue(),
        "media_type": "application/pdf",
        "headers": {"Content-Disposition": f"attachment; filename=historial-{nombre_hijo}-{datetime.now().strftime('%Y%m%d')}.pdf"}
    }