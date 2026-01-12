# app/schemas/enums.py
"""
Enumeraciones para el módulo Padre y otros módulos del sistema
"""
from enum import Enum


class EstadoSesion(str, Enum):
    """Estados de una sesión de terapia"""
    PROGRAMADA = "PROGRAMADA"
    EN_CURSO = "EN_CURSO"
    COMPLETADA = "COMPLETADA"
    CANCELADA = "CANCELADA"
    REPROGRAMADA = "REPROGRAMADA"


class TipoTerapia(str, Enum):
    """Tipos de terapia disponibles"""
    LENGUAJE = "LENGUAJE"
    OCUPACIONAL = "OCUPACIONAL"
    CONDUCTUAL = "CONDUCTUAL"
    FISICA = "FISICA"
    SENSORIAL = "SENSORIAL"
    PSICOLOGICA = "PSICOLOGICA"


class EstadoTarea(str, Enum):
    """Estados de una tarea asignada"""
    PENDIENTE = "PENDIENTE"
    EN_PROGRESO = "EN_PROGRESO"
    COMPLETADA = "COMPLETADA"
    VENCIDA = "VENCIDA"


class TipoDocumento(str, Enum):
    """Tipos de documentos"""
    INFORME = "INFORME"
    EVALUACION = "EVALUACION"
    CONSENTIMIENTO = "CONSENTIMIENTO"
    PLAN_TERAPEUTICO = "PLAN_TERAPEUTICO"
    BITACORA = "BITACORA"
    REPORTE = "REPORTE"
    OTRO = "OTRO"


class TipoRecurso(str, Enum):
    """Tipos de recursos recomendados"""
    PDF = "PDF"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    IMAGEN = "IMAGEN"
    ENLACE = "ENLACE"
    EJERCICIO = "EJERCICIO"


class TipoChat(str, Enum):
    """Tipos de chat"""
    PADRE_TERAPEUTA = "PADRE_TERAPEUTA"
    PADRE_COORDINADOR = "PADRE_COORDINADOR"
    GRUPO_TERAPEUTAS = "GRUPO_TERAPEUTAS"


class TipoNotificacion(str, Enum):
    """Tipos de notificaciones"""
    SESION_PROXIMA = "SESION_PROXIMA"
    SESION_CANCELADA = "SESION_CANCELADA"
    TAREA_ASIGNADA = "TAREA_ASIGNADA"
    DOCUMENTO_NUEVO = "DOCUMENTO_NUEVO"
    MENSAJE_NUEVO = "MENSAJE_NUEVO"
    PAGO_PENDIENTE = "PAGO_PENDIENTE"
    PAGO_RECIBIDO = "PAGO_RECIBIDO"
    OBSERVACION_NUEVA = "OBSERVACION_NUEVA"


class MetodoPago(str, Enum):
    """Métodos de pago aceptados"""
    EFECTIVO = "EFECTIVO"
    TARJETA = "TARJETA"
    TRANSFERENCIA = "TRANSFERENCIA"
    CHEQUE = "CHEQUE"
    DEPOSITO = "DEPOSITO"


class NivelPrioridad(str, Enum):
    """Niveles de prioridad"""
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    URGENTE = "URGENTE"
