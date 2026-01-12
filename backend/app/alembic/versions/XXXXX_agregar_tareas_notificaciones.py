"""Agregar tablas de tareas y notificaciones

Revision ID: XXXXX
Revises: 
Create Date: 2026-01-12
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'XXXXX'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Tabla notificaciones
    op.create_table(
        'notificaciones',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('hijo_id', sa.Integer(), nullable=True),
        sa.Column('tipo', sa.String(50), nullable=False),
        sa.Column('mensaje', sa.Text(), nullable=False),
        sa.Column('leida', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('metadata_json', sa.Text(), nullable=True),
        sa.Column(
            'fecha_creacion',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(
            ['usuario_id'], ['usuarios.id'], ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['hijo_id'], ['pacientes.id'], ondelete='CASCADE'
        )
    )
    op.create_index(
        'ix_notificaciones_usuario_id',
        'notificaciones',
        ['usuario_id']
    )

    # Tabla tareas
    op.create_table(
        'tareas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hijo_id', sa.Integer(), nullable=False),
        sa.Column('terapeuta_id', sa.Integer(), nullable=False),
        sa.Column('objetivo', sa.String(255), nullable=False),
        sa.Column('instrucciones', sa.Text(), nullable=False),
        sa.Column(
            'fecha_asignacion',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.Column('fecha_limite', sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            'estado',
            sa.Enum(
                'PENDIENTE', 'REALIZADA', 'VENCIDA',
                name='estadotarea'
            ),
            nullable=False
        ),
        sa.Column('observaciones', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(
            ['hijo_id'], ['pacientes.id'], ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['terapeuta_id'], ['usuarios.id'], ondelete='CASCADE'
        )
    )
    op.create_index('ix_tareas_hijo_id', 'tareas', ['hijo_id'])

    # Tabla recursos_tareas
    op.create_table(
        'recursos_tareas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tarea_id', sa.Integer(), nullable=False),
        sa.Column('titulo', sa.String(255), nullable=False),
        sa.Column(
            'tipo',
            sa.Enum(
                'PDF', 'IMAGEN', 'VIDEO', 'ENLACE',
                name='tiporecurso'
            ),
            nullable=False
        ),
        sa.Column('url', sa.String(500), nullable=False),
        sa.Column('nombre_archivo', sa.String(255), nullable=True),
        sa.Column(
            'fecha_subida',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(
            ['tarea_id'], ['tareas.id'], ondelete='CASCADE'
        )
    )

    # Tabla evidencias_tareas
    op.create_table(
        'evidencias_tareas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tarea_id', sa.Integer(), nullable=False),
        sa.Column(
            'tipo',
            sa.Enum(
                'PDF', 'IMAGEN', 'VIDEO', 'ENLACE',
                name='tiporecurso'
            ),
            nullable=False
        ),
        sa.Column('url', sa.String(500), nullable=False),
        sa.Column('nombre_archivo', sa.String(255), nullable=False),
        sa.Column(
            'fecha_subida',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(
            ['tarea_id'], ['tareas.id'], ondelete='CASCADE'
        ),
        sa.UniqueConstraint('tarea_id')
    )


def downgrade():
    op.drop_table('evidencias_tareas')
    op.drop_table('recursos_tareas')
    op.drop_table('tareas')
    op.drop_table('notificaciones')

    op.execute('DROP TYPE IF EXISTS estadotarea')
    op.execute('DROP TYPE IF EXISTS tiporecurso')
