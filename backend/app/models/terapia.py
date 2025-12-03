class Terapia(Base):
    __tablename__ = "terapias"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    descripcion: Mapped[str | None]
    tipo_terapia_id: Mapped[int] = mapped_column(
        ForeignKey("cat_tipo_terapia.id", ondelete="RESTRICT", onupdate="CASCADE")
    )
    duracion_minutos: Mapped[int]
    objetivo_general: Mapped[str]
    activo: Mapped[bool] = mapped_column(default=True)

    tipo = relationship("CatTipoTerapia")
    personal_asignado = relationship("PersonalTerapia", back_populates="terapia")
