from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

router = APIRouter(prefix="/padre/hijos", tags=["Padre - Hijos"])

class HijoBase(BaseModel):
  nombre: str = Field(..., min_length=2)
  edad: Optional[int] = None
  fechaNacimiento: Optional[str] = None  # ISO date string
  avatar: Optional[str] = None
  diagnostico: Optional[str] = None

class HijoCreate(HijoBase):
  pass

class HijoUpdate(HijoBase):
  pass

class Hijo(HijoBase):
  id: int

# almacenamiento en memoria (ejemplo)
_db: List[Hijo] = []
_counter = 1

@router.get("", response_model=List[Hijo])
def list_hijos():
  return _db

@router.get("/{hijo_id}", response_model=Hijo)
def get_hijo(hijo_id: int):
  for h in _db:
    if h.id == hijo_id:
      return h
  raise HTTPException(status_code=404, detail="Hijo no encontrado")

@router.post("", response_model=Hijo, status_code=201)
def create_hijo(payload: HijoCreate):
  global _counter
  nuevo = Hijo(id=_counter, **payload.dict())
  _counter += 1
  _db.insert(0, nuevo)
  return nuevo

@router.put("/{hijo_id}", response_model=Hijo)
def update_hijo(hijo_id: int, payload: HijoUpdate):
  for idx, h in enumerate(_db):
    if h.id == hijo_id:
      actualizado = h.copy(update=payload.dict(exclude_unset=True))
      _db[idx] = actualizado
      return actualizado
  raise HTTPException(status_code=404, detail="Hijo no encontrado")

@router.delete("/{hijo_id}", status_code=204)
def delete_hijo(hijo_id: int):
  for idx, h in enumerate(_db):
    if h.id == hijo_id:
      _db.pop(idx)
      return
  raise HTTPException(status_code=404, detail="Hijo no encontrado")