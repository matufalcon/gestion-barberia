from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models.servicio import Servicio
from src.schemas.servicio import ServicioCreate, ServicioRead

router = APIRouter(
    prefix="/servicios",
    tags=["Servicios"]
)
# POST /servicios/ - Crear servicio
@router.post("/", response_model=ServicioRead)
def crear_servicio(servicio: ServicioCreate, db: Session = Depends(get_db)):

    nuevo_servicio = Servicio(**servicio.dict())
    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)
    return nuevo_servicio
    
# GET /servicios/ - Listar todos
@router.get("/", response_model=List[ServicioRead])
def listar_servicios(db:Session = Depends(get_db)):
    servicios = db.query(Servicio).all()
    return servicios

# GET /servicios/{servicio_id} - Obtener uno
@router.get("/{servicio_id}", response_model=ServicioRead)
def obtener_servicio(servicio_id: int, db: Session = Depends(get_db)):
    servicio = db.query(Servicio).filter(Servicio.servicio_id == servicio_id).first()
    
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    return servicio

# PUT /servicios/{servicio_id} - Actualizar
@router.put("/{servicio_id}", response_model=ServicioRead)
def actualizar_servicio(servicio_id: int, servicio_actualizado: ServicioCreate,db: Session = Depends(get_db)):
    servicio = db.query(Servicio).filter(Servicio.servicio_id == servicio_id).first()

    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    #actualizar campos
    for key, value in servicio_actualizado.dict().items():
        setattr(servicio, key, value)
    
    db.commit()
    db.refresh(servicio)
    return servicio

# DELETE /servicios/{servicio_id} - Eliminar
@router.delete("/{servicio_id}")
def eliminar_servicio(servicio_id: int, db:Session = Depends(get_db)):
    servicio = db.query(Servicio).filter(Servicio.servicio_id == servicio_id).first()

    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    db.delete(servicio)
    db.commit()
    return {"message": "Servicio eliminado exitosamente"}