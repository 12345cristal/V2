from pydantic import BaseModel

class TutorDireccionRead(BaseModel):
    calle: str | None
    numero: str | None
    colonia: str | None
    municipio: str | None
    codigo_postal: str | None


class TutorRead(BaseModel):
    id: int
    ocupacion: str | None
    notas: str | None
    direccion: TutorDireccionRead | None
