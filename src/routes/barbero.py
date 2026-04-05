from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models.barbero import Barbero
from src.schemas.barbero import BarberoCreate, BarberoRead

router = APIRouter(
    prefix="/barberos",
    tags=["Barberos"]
)

#crear barbero
@router.post("/", response_model=BarberoRead)
def crear_barbero(barbero: BarberoCreate, db:Session = Depends(get_db)):
    nuevo_barbero = Barbero(**barbero.dict())

    db.add(nuevo_barbero)
    db.commit()
    db.refresh(nuevo_barbero)
    return nuevo_barbero

#listar barberos
@router.get("/", response_model=List[BarberoRead])
def listar_barberos(db:Session = Depends(get_db)):
    barberos = db.query(Barbero).all()

    return barberos

#obtener un barbero
@router.get("/{barbero_id}", response_model=BarberoRead)
def obtener_barbero(barbero_id: int, db:Session = Depends(get_db)):
    barbero = db.query(Barbero).filter(Barbero.barbero_id == barbero_id).first()

    if not barbero:
        raise HTTPException(status_code=404, detail="Barbero no existente")
    
    return barbero

#actualizar barbero
@router.put("/{barbero_id}", response_model=BarberoRead)
def actualizar_barbero(barbero_id: int, barbero_actualizado: BarberoCreate, db:Session = Depends(get_db)):
    barbero = db.query(Barbero).filter(Barbero.barbero_id == barbero_id).first()

    if not barbero:
        raise HTTPException(status_code=404, detail="Barbero no existente")
    
    #actualizar campos
    for key, value in barbero_actualizado.dict().items():
        setattr(barbero, key, value)

    db.commit()
    db.refresh(barbero)
    return barbero

#eliminar barbero
@router.delete("/{barbero_id}")
def eliminar_barbero(barbero_id: int, db:Session = Depends(get_db)):
    barbero = db.query(Barbero).filter(Barbero.barbero_id == barbero_id).first()

    if not barbero:
        raise HTTPException(status_code=404, detail="Barbero no existente")
    
    db.delete(barbero)
    db.commit()
    return {"message": "Barbero eliminado exitosamente"}
