class RecursoVisto(Base):
    __tablename__ = "recursos_vistos"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False
    )

    recurso_id = Column(
        Integer,
        ForeignKey("recursos.id", ondelete="CASCADE"),
        nullable=False
    )

    fecha_visto = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("usuario_id", "recurso_id", name="uq_usuario_recurso"),
    )

    usuario = relationship(
        "Usuario",
        back_populates="recursos_vistos"
    )

    recurso = relationship(
        "Recurso",
        back_populates="vistas"
    )
