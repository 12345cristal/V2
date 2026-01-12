# app/db/session.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.core.config import settings

# Crear el engine de SQLAlchemy para MySQL
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=settings.DEBUG,
    connect_args={"charset": "utf8mb4"}
)

# Crear la sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Generador de sesiones de base de datos
    Uso: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializa la base de datos creando todas las tablas."""
    from app.models import (
        Usuario,
        Paciente,
        Notificacion,
        Tarea,
        RecursoTarea,
        EvidenciaTarea,
        Sesion,
        ActividadSesion,
        Historial,
        AsistenciaMensual,
        EvolucionObjetivo,
        FrecuenciaTerapia,
        Pago
    )
    from app.models.documento import Documento, DocumentoVisto

    Base.metadata.create_all(bind=engine)
