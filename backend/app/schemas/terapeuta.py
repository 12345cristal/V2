from pydantic import BaseModel, EmailStr
from typing import Optional, List, Literal
from datetime import datetime, date

# ============================================
# SCHEMAS PARA PACIENTES / HIJOS
# ============================================

class PacienteResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    edad: int
    fecha_nacimiento: str
    diagnostico: str
    nivel_tea: str
    padre_id: int
    padre_nombre: str
    padre_email: str
    padre_telefono: str
    fecha_asignacion: Optional[str]
    total_sesiones: int
    ultima_sesion: Optional[str]
    proxima_sesion: Optional[str]
    recursos_asignados: int
    nivel_progreso: str
    observaciones: Optional[str]
    foto_perfil: Optional[str]

    class Config:
        from_attributes = True


class PadreInfo(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: str


class SesionResumen(BaseModel):
    id: int
    fecha: str
    tipo: str
    estado: str
    duracion: Optional[int]
    notas: Optional[str]
    objetivo: Optional[str]


class ProgresoResumen(BaseModel):
    id: int
    fecha: str
    area: str
    nivel: str
    observaciones: Optional[str]
    puntuacion: Optional[float]


class RecursoResumen(BaseModel):
    id: int
    titulo: str
    tipo: str
    categoria: str
    fecha_asignacion: str


class EstadisticasPaciente(BaseModel):
    total_sesiones: int
    sesiones_completadas: int
    recursos_asignados: int
    tendencia_progreso: str


class PacienteDetalleResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    edad: int
    fecha_nacimiento: str
    diagnostico: str
    nivel_tea: str
    observaciones: Optional[str]
    foto_perfil: Optional[str]
    padre: PadreInfo
    fecha_asignacion: str
    estadisticas: EstadisticasPaciente
    sesiones_recientes: List[SesionResumen]
    progresos: List[ProgresoResumen]
    recursos: List[RecursoResumen]

    class Config:
        from_attributes = True


class SesionesStats(BaseModel):
    total: int
    completadas: int
    canceladas: int
    tasa_asistencia: float


class AreaProgreso(BaseModel):
    area: str
    promedio: float
    evaluaciones: int


class EstadisticasPacienteResponse(BaseModel):
    periodo: str
    fecha_inicio: str
    fecha_fin: str
    sesiones: SesionesStats
    horas_terapia: float
    progresos_por_area: List[AreaProgreso]
    recursos_asignados: int

    class Config:
        from_attributes = True


# ============================================
# SCHEMAS PARA TERAPEUTA
# ============================================

class EstadisticasTerapeuta(BaseModel):
    total_pacientes: int
    total_sesiones: int
    total_recursos: int
    sesiones_proximas: int


class SesionProxima(BaseModel):
    id: int
    fecha: str
    hijo_nombre: tuple
    tipo: str


class TerapeutaPerfilResponse(BaseModel):
    id: int
    nombre: str
    email: str
    especialidad: Optional[str]
    cedula_profesional: Optional[str]
    telefono: Optional[str]
    anos_experiencia: Optional[int]
    estadisticas: EstadisticasTerapeuta
    proximas_sesiones: List[SesionProxima]

    class Config:
        from_attributes = True


class RegistrarAsistencia(BaseModel):
    id_sesion: int
    estado: Literal['asistio', 'cancelada', 'reprogramada']
    fecha_registro: str
    nota: Optional[str] = None


class ReprogramarSesion(BaseModel):
    id_sesion: int
    nueva_fecha: str
    nueva_hora: str
    motivo: str


class EnviarMensaje(BaseModel):
    tipo_destinatario: str
    id_destinatario: int
    mensaje: str
