# app/schemas/padre.py
"""
Schemas Pydantic para el módulo Padre (Dashboard de Padres/Tutores)
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date, time
from app.schemas.enums import (
    EstadoSesion, TipoTerapia, EstadoTarea, TipoDocumento,
    TipoRecurso, TipoNotificacion, MetodoPago, NivelPrioridad, TipoChat
)


# ==================================================
# PADRE / TUTOR
# ==================================================
class PadreBase(BaseModel):
    """Schema base de Padre/Tutor"""
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    email: EmailStr
    telefono: Optional[str] = None
    ocupacion: Optional[str] = None


class PadreCreate(PadreBase):
    """Schema para crear un padre"""
    password: str


class PadreUpdate(BaseModel):
    """Schema para actualizar un padre"""
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    telefono: Optional[str] = None
    ocupacion: Optional[str] = None


class Padre(PadreBase):
    """Schema completo de Padre"""
    id: int
    activo: bool
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True


# ==================================================
# HIJO
# ==================================================
class HijoBase(BaseModel):
    """Schema base de Hijo"""
    nombre: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    fecha_nacimiento: date
    sexo: str = Field(..., pattern="^(M|F|O)$")
    curp: Optional[str] = None


class HijoCreate(HijoBase):
    """Schema para crear un hijo"""
    diagnostico_principal: Optional[str] = None


class HijoUpdate(BaseModel):
    """Schema para actualizar información del hijo"""
    nombre: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    telefono_emergencia: Optional[str] = None


class Hijo(HijoBase):
    """Schema completo de Hijo"""
    id: int
    edad: int
    diagnostico_principal: Optional[str] = None
    estado: str
    fecha_registro: datetime
    
    class Config:
        from_attributes = True


class HijoDetalle(Hijo):
    """Schema detallado de Hijo con información adicional"""
    alergias: List[str] = []
    medicamentos: List[str] = []
    terapias_activas: List[str] = []
    proxima_sesion: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================================================
# ALERGIAS Y MEDICAMENTOS
# ==================================================
class AlergiaBase(BaseModel):
    """Schema de Alergia"""
    nombre: str
    descripcion: Optional[str] = None
    gravedad: Optional[str] = "MEDIA"


class Alergia(AlergiaBase):
    """Schema completo de Alergia"""
    id: int
    hijo_id: int
    fecha_registro: datetime
    
    class Config:
        from_attributes = True


class MedicamentoBase(BaseModel):
    """Schema de Medicamento"""
    nombre: str
    dosis: Optional[str] = None
    frecuencia: Optional[str] = None
    hora_administracion: Optional[str] = None
    indicaciones: Optional[str] = None


class Medicamento(MedicamentoBase):
    """Schema completo de Medicamento"""
    id: int
    hijo_id: int
    activo: bool
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    
    class Config:
        from_attributes = True


# ==================================================
# SESIONES
# ==================================================
class SesionBase(BaseModel):
    """Schema base de Sesión"""
    fecha: date
    hora_inicio: time
    hora_fin: time
    terapia: str
    terapeuta: str
    estado: EstadoSesion


class SesionCreate(SesionBase):
    """Schema para crear una sesión"""
    hijo_id: int
    terapeuta_id: int
    terapia_id: int


class Sesion(SesionBase):
    """Schema completo de Sesión"""
    id: int
    hijo_id: int
    observaciones: Optional[str] = None
    asistio: bool = True
    
    class Config:
        from_attributes = True


class SesionDetalle(Sesion):
    """Schema detallado de Sesión con más información"""
    duracion_minutos: int
    objetivos: List[str] = []
    actividades_realizadas: List[str] = []
    progreso_porcentaje: Optional[int] = None
    comentarios_terapeuta: Optional[str] = None
    materiales_usados: List[str] = []
    recomendaciones: Optional[str] = None
    
    class Config:
        from_attributes = True


class SesionComentarioCreate(BaseModel):
    """Schema para agregar comentarios a una sesión"""
    comentario: str = Field(..., min_length=1, max_length=1000)
    progreso_porcentaje: Optional[int] = Field(None, ge=0, le=100)
    recomendaciones: Optional[str] = None


class BitacoraDaily(BaseModel):
    """Schema de Bitácora Diaria"""
    sesion_id: int
    fecha: date
    hijo_nombre: str
    terapia: str
    terapeuta: str
    actividades: List[str]
    logros: List[str]
    observaciones: str
    recomendaciones_padres: str
    
    class Config:
        from_attributes = True


# ==================================================
# TAREAS
# ==================================================
class TareaBase(BaseModel):
    """Schema base de Tarea"""
    titulo: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    fecha_asignacion: date
    fecha_vencimiento: date
    estado: EstadoTarea = EstadoTarea.PENDIENTE


class TareaCreate(TareaBase):
    """Schema para crear una tarea"""
    hijo_id: int
    terapeuta_id: int


class TareaUpdate(BaseModel):
    """Schema para actualizar una tarea"""
    estado: Optional[EstadoTarea] = None
    fecha_completada: Optional[datetime] = None
    notas_padre: Optional[str] = None


class Tarea(TareaBase):
    """Schema completo de Tarea"""
    id: int
    hijo_id: int
    terapeuta: str
    prioridad: NivelPrioridad = NivelPrioridad.MEDIA
    fecha_completada: Optional[datetime] = None
    tiene_recursos: bool = False
    
    class Config:
        from_attributes = True


# ==================================================
# PAGOS
# ==================================================
class PlanPago(BaseModel):
    """Schema de Plan de Pago"""
    nombre: str
    monto_mensual: float
    fecha_corte: int
    terapias_incluidas: int
    sesiones_mes: int


class PagoBase(BaseModel):
    """Schema base de Pago"""
    monto: float = Field(..., gt=0)
    fecha_pago: date
    metodo_pago: MetodoPago
    concepto: str
    comprobante: Optional[str] = None


class Pago(PagoBase):
    """Schema completo de Pago"""
    id: int
    padre_id: int
    mes: int
    anio: int
    estatus: str  # PENDIENTE, PAGADO, VENCIDO
    fecha_vencimiento: date
    
    class Config:
        from_attributes = True


class HistorialPago(BaseModel):
    """Schema de Historial de Pagos"""
    pagos: List[Pago]
    total_pagado: float
    saldo_pendiente: float
    proximo_pago: Optional[Pago] = None


class InformacionPago(BaseModel):
    """Schema de Información de Pago del Padre"""
    plan: PlanPago
    saldo_actual: float
    ultimo_pago: Optional[Pago] = None
    proximo_vencimiento: Optional[date] = None
    dias_para_vencimiento: Optional[int] = None
    meses_adeudados: int = 0


# ==================================================
# DOCUMENTOS
# ==================================================
class DocumentoBase(BaseModel):
    """Schema base de Documento"""
    titulo: str
    tipo: TipoDocumento
    descripcion: Optional[str] = None
    archivo_url: str


class Documento(DocumentoBase):
    """Schema completo de Documento"""
    id: int
    hijo_id: int
    fecha_subida: datetime
    subido_por: str  # Nombre del terapeuta/coordinador
    visto: bool = False
    fecha_visto: Optional[datetime] = None
    es_nuevo: bool = True
    
    class Config:
        from_attributes = True


# ==================================================
# RECURSOS RECOMENDADOS
# ==================================================
class RecursoBase(BaseModel):
    """Schema base de Recurso"""
    titulo: str
    descripcion: Optional[str] = None
    tipo: TipoRecurso
    url: str
    miniatura: Optional[str] = None


class Recurso(RecursoBase):
    """Schema completo de Recurso"""
    id: int
    hijo_id: int
    terapeuta: str
    fecha_recomendacion: datetime
    objetivo: Optional[str] = None
    visto: bool = False
    fecha_visto: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================================================
# MENSAJES Y CHAT
# ==================================================
class MensajeBase(BaseModel):
    """Schema base de Mensaje"""
    contenido: str = Field(..., min_length=1)
    tipo: str = Field(default="TEXTO", pattern="^(TEXTO|AUDIO|ARCHIVO|IMAGEN)$")


class MensajeCreate(MensajeBase):
    """Schema para crear un mensaje"""
    chat_id: int
    archivo_url: Optional[str] = None


class Mensaje(MensajeBase):
    """Schema completo de Mensaje"""
    id: int
    chat_id: int
    remitente_id: int
    remitente_nombre: str
    fecha_envio: datetime
    leido: bool = False
    fecha_lectura: Optional[datetime] = None
    archivo_url: Optional[str] = None
    
    class Config:
        from_attributes = True


class ChatResumen(BaseModel):
    """Schema de resumen de Chat"""
    id: int
    tipo: TipoChat
    participante_nombre: str
    participante_rol: str
    ultimo_mensaje: Optional[str] = None
    fecha_ultimo_mensaje: Optional[datetime] = None
    mensajes_no_leidos: int = 0
    
    class Config:
        from_attributes = True


# ==================================================
# NOTIFICACIONES
# ==================================================
class NotificacionBase(BaseModel):
    """Schema base de Notificación"""
    tipo: TipoNotificacion
    titulo: str
    mensaje: str
    url: Optional[str] = None


class Notificacion(NotificacionBase):
    """Schema completo de Notificación"""
    id: int
    padre_id: int
    fecha_creacion: datetime
    leida: bool = False
    fecha_lectura: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================================================
# ACCESIBILIDAD
# ==================================================
class AccesibilidadBase(BaseModel):
    """Schema de preferencias de Accesibilidad"""
    tamaño_fuente: str = Field(default="NORMAL", pattern="^(PEQUEÑO|NORMAL|GRANDE|MUY_GRANDE)$")
    contraste_alto: bool = False
    modo_oscuro: bool = False
    lectura_voz: bool = False
    subtitulos_video: bool = True
    notificaciones_sonido: bool = True
    notificaciones_vibracion: bool = True


class Accesibilidad(AccesibilidadBase):
    """Schema completo de Accesibilidad"""
    id: int
    padre_id: int
    fecha_actualizacion: datetime
    
    class Config:
        from_attributes = True


# ==================================================
# DASHBOARD
# ==================================================
class ProximaSesion(BaseModel):
    """Información de próxima sesión"""
    id: int
    hijo_nombre: str
    terapia: str
    terapeuta: str
    fecha: datetime
    duracion_minutos: int
    ubicacion: Optional[str] = None


class AvanceHijo(BaseModel):
    """Avance de un hijo"""
    hijo_id: int
    hijo_nombre: str
    progreso_general: int  # 0-100
    sesiones_mes: int
    sesiones_completadas: int
    objetivos_logrados: int
    objetivos_totales: int


class ObservacionReciente(BaseModel):
    """Observación reciente"""
    id: int
    hijo_nombre: str
    terapeuta: str
    fecha: datetime
    observacion: str
    tipo: str  # LOGRO, RECOMENDACION, ATENCION


class DashboardResumen(BaseModel):
    """Schema de resumen del Dashboard del Padre"""
    padre: Padre
    proxima_sesion: Optional[ProximaSesion] = None
    hijos: List[AvanceHijo] = []
    pagos_pendientes: int = 0
    monto_pendiente: float = 0
    documentos_nuevos: int = 0
    mensajes_no_leidos: int = 0
    notificaciones_no_leidas: int = 0
    tareas_pendientes: int = 0
    observaciones_recientes: List[ObservacionReciente] = []
    
    class Config:
        from_attributes = True


# ==================================================
# HISTORIAL TERAPÉUTICO
# ==================================================
class AsistenciaMes(BaseModel):
    """Asistencia mensual"""
    mes: int
    anio: int
    sesiones_programadas: int
    sesiones_asistidas: int
    sesiones_canceladas: int
    porcentaje_asistencia: float


class EvolucionObjetivo(BaseModel):
    """Evolución de un objetivo"""
    objetivo: str
    fecha_inicio: date
    progreso: List[dict]  # [{fecha: date, porcentaje: int}]
    estado: str  # EN_PROGRESO, LOGRADO, PAUSADO


class HistorialTerapeutico(BaseModel):
    """Schema de Historial Terapéutico"""
    hijo_id: int
    hijo_nombre: str
    periodo: str  # MES, TRIMESTRE, SEMESTRE, AÑO
    fecha_inicio: date
    fecha_fin: date
    asistencia: List[AsistenciaMes]
    evolucion_objetivos: List[EvolucionObjetivo]
    total_sesiones: int
    progreso_general: int
    
    class Config:
        from_attributes = True


# ==================================================
# RESPUESTAS PAGINADAS
# ==================================================
class PaginatedResponse(BaseModel):
    """Respuesta paginada genérica"""
    total: int
    page: int = 1
    page_size: int = 20
    total_pages: int


class HijosListResponse(PaginatedResponse):
    """Respuesta de lista de hijos"""
    items: List[Hijo]


class SesionesListResponse(PaginatedResponse):
    """Respuesta de lista de sesiones"""
    items: List[Sesion]


class TareasListResponse(PaginatedResponse):
    """Respuesta de lista de tareas"""
    items: List[Tarea]


class DocumentosListResponse(PaginatedResponse):
    """Respuesta de lista de documentos"""
    items: List[Documento]


class RecursosListResponse(PaginatedResponse):
    """Respuesta de lista de recursos"""
    items: List[Recurso]


class MensajesListResponse(PaginatedResponse):
    """Respuesta de lista de mensajes"""
    items: List[Mensaje]


class NotificacionesListResponse(PaginatedResponse):
    """Respuesta de lista de notificaciones"""
    items: List[Notificacion]
