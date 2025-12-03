class PersonalTerapia(Base):
    __tablename__ = "personal_terapias"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    personal_id: Mapped[int] = mapped_column(ForeignKey("personal.id"))
    terapia_id: Mapped[int] = mapped_column(ForeignKey("terapias.id"))

    personal = relationship("Personal", back_populates="terapias")
    terapia = relationship("Terapia", back_populates="personal_asignado")
