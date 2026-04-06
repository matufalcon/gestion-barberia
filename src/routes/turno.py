from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from src.database import get_db
from src.models.turno import Turno
from src.models.usuario import Usuario
from src.models.barbero import Barbero
from src.models.servicio import Servicio
from src.schemas.turno import TurnoCreate, TurnoRead

router = APIRouter( 
    prefix="/turnos",
    tags=["Turnos"]
)

#crear turno
@router.post("/", response_model=TurnoRead)
def crear_turno(turno: TurnoCreate, db:Session = Depends(get_db)):

    #validaciones cliente, barbero, servicio
    cliente = db.query(Usuario).filter(Usuario.usuario_id == turno.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente inexistente!")
    
    barbero = db.query(Barbero).filter(Barbero.barbero_id == turno.barbero_id).first()
    if not barbero:
        raise HTTPException(status_code=404, detail="Barbero inexistente!")
    
    servicio = db.query(Servicio).filter(Servicio.servicio_id == turno.servicio_id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio inexistente!")

    #validaciones para la fecha
    fecha_turno = turno.fecha_hora.replace(tzinfo=None)
    fecha_actual = datetime.now()

    if fecha_turno < fecha_actual:
        raise HTTPException(status_code=400, detail="No se pueden crear turnos en fechas pasadas")

    #validaciones barbero ocupado
    inicio_nuevo = turno.fecha_hora.replace(tzinfo=None)
    fin_nuevo = inicio_nuevo + timedelta(minutes=servicio.duracion)

    # Turnos existentes del barbero:
    turnos_existentes = db.query(Turno).filter(
        Turno.barbero_id == turno.barbero_id, 
        Turno.estado != "cancelado"
    ).all()

    # Verificar solapamiento con cada turno existente
    for turno_existente in turnos_existentes:
        inicio_existente = turno_existente.fecha_hora.replace(tzinfo=None)
        fin_existente = inicio_existente + timedelta(minutes=turno_existente.servicio.duracion)
    
        # ¿Hay solapamiento?
        if inicio_nuevo < fin_existente and fin_nuevo > inicio_existente:
            raise HTTPException(
                status_code=400, 
                detail=f"El barbero ya tiene un turno a las {inicio_existente.strftime('%H:%M')}"
            )

    nuevo_turno = Turno(**turno.dict())
    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)
    return nuevo_turno


#listar turnos
@router.get("/", response_model=List[TurnoRead])
def listar_turnos(db:Session = Depends(get_db)):
    turnos = db.query(Turno).all()
    return turnos


#obtener turno por id
@router.get("/{turno_id}", response_model=TurnoRead)
def obtener_turno(turno_id: int, db:Session = Depends(get_db)):
    turno = db.query(Turno).filter(Turno.turno_id == turno_id).first()

    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    return turno

#actualizar turno
@router.put("/{turno_id}", response_model=TurnoRead)
def actualizar_turno(turno_id: int, turno_actualizado: TurnoCreate, db:Session = Depends(get_db)):
    turno = db.query(Turno).filter(Turno.turno_id == turno_id).first()

    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    #actualizar campos
    for key, value in turno_actualizado.dict().items():
        setattr(turno, key, value)

    db.commit()
    db.refresh(turno)
    return turno

#eliminar turno
@router.delete("/{turno_id}")
def eliminar_turno(turno_id: int, db:Session = Depends(get_db)):
    turno = db.query(Turno).filter(Turno.turno_id == turno_id).first()

    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    db.delete(turno)
    db.commit()
    return {"message": "Turno eliminado exitosamente"}