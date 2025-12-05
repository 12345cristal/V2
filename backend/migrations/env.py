from __future__ import with_statement
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Import settings and Base
from app.core.config import get_settings
from app.db.base import Base

# IMPORTA TODOS TUS MODELOS PARA QUE ALEMBIC LOS VEA
# (por ahora solo auth, luego agregamos niños, terapias, citas, etc.)
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.permiso import Permiso
from app.models.rol_permiso import RolPermiso
from app.models.auditoria import Auditoria

# Acceso a config de Alembic
config = context.config

# Configuración de logging
fileConfig(config.config_file_name)

# Metadata de SQLAlchemy para autogenerate
target_metadata = Base.metadata

# Leer settings de FastAPI
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_offline():
    """Ejecuta migraciones sin conexión (solo genera script SQL)."""
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,     # Detecta cambios de tipo
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Ejecuta migraciones conectándose a MySQL."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# Selección automática del modo
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
