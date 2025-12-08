# app/schemas/__init__.py
"""Schemas Pydantic para validación y serialización"""

# Auth schemas
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    Token,
    UserInToken,
    ChangePasswordRequest,
)

# Usuario schemas
from app.schemas.usuario import (
    UsuarioBase,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioChangePassword,
    UsuarioInDB,
    UsuarioWithRol,
    UsuarioList,
)

# Rol y Permiso schemas
from app.schemas.rol import (
    PermisoBase,
    PermisoCreate,
    PermisoUpdate,
    PermisoInDB,
    RolBase,
    RolCreate,
    RolUpdate,
    RolInDB,
    RolWithPermisos,
    RolePermisoAssign,
)

# Personal schemas
from app.schemas.personal import (
    PersonalBase,
    PersonalCreate,
    PersonalUpdate,
    PersonalInDB,
    PersonalWithUsuario,
    PersonalCompleto,
    PersonalList,
)

# Tutor schemas
from app.schemas.tutor import (
    TutorBase,
    TutorCreate,
    TutorUpdate,
    TutorInDB,
    TutorWithUsuario,
)

# Niño schemas
from app.schemas.nino import (
    NinoBase,
    NinoCreate,
    NinoUpdate,
    NinoInDB,
    NinoCompleto,
    NinoList,
)

# Terapia schemas
from app.schemas.terapia import (
    TerapiaCreate,
    TerapiaUpdate,
    TerapiaInDB,
    TerapiaCompleta,
    SesionCreate,
    SesionUpdate,
    SesionInDB,
    SesionWithDetails,
    SesionList,
)

# Cita schemas
from app.schemas.cita import (
    CitaCreate,
    CitaUpdate,
    CitaInDB,
    CitaWithDetails,
    CitaList,
)

# Recurso schemas
from app.schemas.recurso import (
    RecursoCreate,
    RecursoUpdate,
    RecursoInDB,
    RecursoWithDetails,
    RecursoList,
    TareaRecursoCreate,
    TareaRecursoUpdate,
    ValoracionCreate,
    RecomendacionCreate,
)

# Notificación schemas
from app.schemas.notificacion import (
    NotificacionCreate,
    NotificacionInDB,
    NotificacionList,
    NotificacionCreateBulk,
)

__all__ = [
    "LoginRequest",
    "LoginResponse",
    "Token",
    "UserInToken",
    "ChangePasswordRequest",
]
