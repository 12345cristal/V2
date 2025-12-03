from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_permissions, get_current_active_user
from app.models.personal import Personal
from app.schemas.personal import PersonalCreate, PersonalRead, PersonalUpdate

router = APIRouter(
    prefix="/personal",
    tags=["personal"],
    dependencies=[Depends(require_permissions(["personal:ver"]))],
)


@router.get("/", response_model=list[PersonalRead])
def list_personal(db: Session = Depends(get_db)):
    personal = db.query(Personal).order_by(Personal.id.desc()).all()
    return personal


@router.post("/", response_model=PersonalRead, status_code=201,
             dependencies=[Depends(require_permissions(["personal:crear"]))])
def create_personal(data: PersonalCreate, db: Session = Depends(get_db)):
    personal = Personal(**data.model_dump())
    db.add(personal)
    db.commit()
    db.refresh(personal)
    return personal


@router.get("/{personal_id}", response_model=PersonalRead)
def get_personal(personal_id: int, db: Session = Depends(get_db)):
    obj = db.get(Personal, personal_id)
    if not obj:
        raise HTTPException(404, "Personal no encontrado")
    return obj


@router.put("/{personal_id}", response_model=PersonalRead,
            dependencies=[Depends(require_permissions(["personal:editar"]))])
def update_personal(personal_id: int, data: PersonalUpdate, db: Session = Depends(get_db)):
    personal = db.get(Personal, personal_id)
    if not personal:
        raise HTTPException(404, "Personal no encontrado")

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(personal, k, v)

    db.commit()
    db.refresh(personal)
    return personal


@router.delete("/{personal_id}", status_code=204,
               dependencies=[Depends(require_permissions(["personal:eliminar"]))])
def delete_personal(personal_id: int, db: Session = Depends(get_db)):
    personal = db.get(Personal, personal_id)
    if not personal:
        raise HTTPException(404, "Personal no encontrado")

    db.delete(personal)
    db.commit()
    return
