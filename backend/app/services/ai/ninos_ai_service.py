# app/services/ai/ninos_ai_service.py
from __future__ import annotations

from typing import Optional, Dict, Any

from sqlalchemy.orm import Session

from app.models.nino import Nino, NinoDiagnostico, NinoInfoEmocional, NinoAlergias, NinoMedicamentosActuales, NinoEscolar
from app.models.terapia import TerapiaNino, SesionTerapia, Terapia
from app.services.ai.gemini_service import GeminiClient
from app.services.decision_logs_service import registrar_decision


def _calcular_metricas_progreso(db: Session, nino_id: int) -> Dict[str, Any]:
    """
    Calcula métricas simples de progreso a partir de sesiones de terapia.
    Esto es IA interna (estadística), NO LLM.
    """
    q = (
        db.query(SesionTerapia)
        .join(TerapiaNino, SesionTerapia.terapia_nino_id == TerapiaNino.id)
        .filter(TerapiaNino.nino_id == nino_id)
    )

    sesiones = q.all()
    if not sesiones:
        return {
            "total_sesiones": 0,
            "promedio_progreso": 0,
            "promedio_colaboracion": 0,
            "porcentaje_asistencia": 0,
        }

    total = len(sesiones)
    suma_prog = sum(s.nivel_progreso for s in sesiones)
    suma_colab = sum(s.nivel_colaboracion for s in sesiones)
    asistidas = sum(1 for s in sesiones if s.asistio)

    return {
        "total_sesiones": total,
        "promedio_progreso": round(suma_prog / total, 2),
        "promedio_colaboracion": round(suma_colab / total, 2),
        "porcentaje_asistencia": round(asistidas * 100 / total, 2),
    }


def _construir_perfil_textual_nino(
    db: Session,
    nino_id: int,
    texto_extra: Optional[str] = None
) -> str:
    """
    Construye un texto con TODA la info del niño desde la BD + texto extra del terapeuta.
    Esto es lo que se manda a Gemini.
    """
    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    if not nino:
        raise ValueError("Niño no encontrado")

    diag = db.query(NinoDiagnostico).filter(NinoDiagnostico.nino_id == nino_id).first()
    emo = db.query(NinoInfoEmocional).filter(NinoInfoEmocional.nino_id == nino_id).first()
    alerg = db.query(NinoAlergias).filter(NinoAlergias.nino_id == nino_id).first()
    meds = (
        db.query(NinoMedicamentosActuales)
        .filter(NinoMedicamentosActuales.nino_id == nino_id)
        .all()
    )
    esc = db.query(NinoEscolar).filter(NinoEscolar.nino_id == nino_id).first()

    terapias_asignadas = (
        db.query(TerapiaNino, Terapia)
        .join(Terapia, TerapiaNino.terapia_id == Terapia.id)
        .filter(TerapiaNino.nino_id == nino_id, TerapiaNino.activo == 1)
        .all()
    )

    metricas = _calcular_metricas_progreso(db, nino_id)

    lineas = []

    # Datos básicos
    lineas.append(f"Nombre del niño: {nino.nombre} {nino.apellido_paterno} {nino.apellido_materno or ''}".strip())
    lineas.append(f"Sexo: {nino.sexo}")
    lineas.append(f"Estado actual: {nino.estado}")
    lineas.append("")

    # Diagnóstico
    if diag:
        lineas.append("Diagnóstico principal:")
        lineas.append(f"- {diag.diagnostico_principal}")
        if diag.diagnostico_resumen:
            lineas.append(f"Resumen diagnósticos: {diag.diagnostico_resumen}")
        if diag.fecha_diagnostico:
            lineas.append(f"Fecha diagnóstico: {diag.fecha_diagnostico}")
        if diag.especialista:
            lineas.append(f"Especialista: {diag.especialista}")
        if diag.institucion:
            lineas.append(f"Institución: {diag.institucion}")
        lineas.append("")

    # Escolar
    if esc:
        lineas.append("Información escolar:")
        if esc.asiste_escuela:
            lineas.append(f"- Asiste a escuela: SÍ ({esc.escuela}, grado {esc.grado})")
        else:
            lineas.append("- No asiste a escuela actualmente.")
        if esc.adaptaciones:
            lineas.append(f"Adaptaciones escolares: {esc.adaptaciones}")
        lineas.append("")

    # Alergias
    if alerg:
        lineas.append("Alergias:")
        if alerg.medicamentos:
            lineas.append(f"- Medicamentos: {alerg.medicamentos}")
        if alerg.alimentos:
            lineas.append(f"- Alimentos: {alerg.alimentos}")
        if alerg.ambiental:
            lineas.append(f"- Ambientales: {alerg.ambiental}")
        lineas.append("")

    # Medicamentos
    if meds:
        lineas.append("Medicamentos actuales:")
        for m in meds:
            lineas.append(f"- {m.nombre} (dosis: {m.dosis}, horario: {m.horario})")
        lineas.append("")

    # Información emocional
    if emo:
        lineas.append("Información emocional y sensorial:")
        if emo.estimulos_ansiedad:
            lineas.append(f"- Estímulos que generan ansiedad: {emo.estimulos_ansiedad}")
        if emo.cosas_que_calman:
            lineas.append(f"- Cosas que lo calman: {emo.cosas_que_calman}")
        if emo.preferencias_sensoriales:
            lineas.append(f"- Preferencias sensoriales: {emo.preferencias_sensoriales}")
        if emo.cosas_no_tolera:
            lineas.append(f"- No tolera: {emo.cosas_no_tolera}")
        if emo.palabras_clave:
            lineas.append(f"- Palabras clave útiles: {emo.palabras_clave}")
        if emo.forma_comunicacion:
            lineas.append(f"- Forma principal de comunicación: {emo.forma_comunicacion}")
        lineas.append(f"- Nivel de comprensión estimado: {emo.nivel_comprension}")
        lineas.append("")

    # Terapias activas
    if terapias_asignadas:
        lineas.append("Terapias activas:")
        for tn, t in terapias_asignadas:
            lineas.append(
                f"- {t.nombre} (frecuencia por semana: {tn.frecuencia_semana}, prioridad_id: {tn.prioridad_id})"
            )
        lineas.append("")

    # Métricas de progreso
    lineas.append("Métricas generales de progreso:")
    lineas.append(f"- Total de sesiones: {metricas['total_sesiones']}")
    lineas.append(f"- Promedio de progreso: {metricas['promedio_progreso']}")
    lineas.append(f"- Promedio de colaboración: {metricas['promedio_colaboracion']}")
    lineas.append(f"- Porcentaje de asistencia: {metricas['porcentaje_asistencia']}%")
    lineas.append("")

    if texto_extra:
        lineas.append("Notas adicionales del terapeuta/del tutor:")
        lineas.append(texto_extra)
        lineas.append("")

    return "\n".join(lineas)


def analisis_completo_nino(
    db: Session,
    nino_id: int,
    texto_extra: Optional[str],
    usuario_id: int
) -> Dict[str, Any]:
    """
    A3: Usa COMBINADO:
    - BD del niño
    - texto_extra opcional del terapeuta
    - Gemini para análisis avanzado
    """
    perfil_texto = _construir_perfil_textual_nino(db, nino_id, texto_extra)
    metricas = _calcular_metricas_progreso(db, nino_id)

    ia = GeminiClient()

    # IA: análisis emocional
    analisis_emo = ia.perfil_emocional(perfil_texto)
    registrar_decision(db, "nino_perfil_emocional", perfil_texto, analisis_emo, usuario_id)

    # IA: recomendación de terapias (usa diagnóstico si existe)
    diag = (
        db.query(NinoDiagnostico)
        .filter(NinoDiagnostico.nino_id == nino_id)
        .first()
    )
    texto_diag = diag.diagnostico_principal if diag else perfil_texto
    recomendaciones_terapias = ia.recomendar_terapias(texto_diag)
    registrar_decision(db, "nino_recomendar_terapias", texto_diag, recomendaciones_terapias, usuario_id)

    # IA: recomendación de actividades (usa perfil completo)
    recomendaciones_actividades = ia.recomendar_actividades(perfil_texto)
    registrar_decision(db, "nino_recomendar_actividades", perfil_texto, recomendaciones_actividades, usuario_id)

    # IA: explicación para padres (usa métrica + análisis)
    resumen_simple = (
        f"Progreso promedio: {metricas['promedio_progreso']}, "
        f"colaboración: {metricas['promedio_colaboracion']}, "
        f"asistencia: {metricas['porcentaje_asistencia']}%."
    )
    explicacion_padres = ia.explicar_progreso(resumen_simple)
    registrar_decision(db, "nino_explicar_progreso_padres", resumen_simple, explicacion_padres, usuario_id)

    return {
        "metricas": metricas,
        "perfil_textual": perfil_texto,
        "analisis_emocional": analisis_emo,
        "recomendaciones_terapias": recomendaciones_terapias,
        "recomendaciones_actividades": recomendaciones_actividades,
        "explicacion_para_padres": explicacion_padres,
    }
