from pydantic import BaseModel
from datetime import datetime
from typing import Optional

#schema para creacion de turno
class TurnoCreate(BaseModel):
    cliente_id: int
    barbero_id: int
    servicio_id: int
    fecha_hora: datetime  
    estado: str="pendiente"
    notas: Optional[str]=None

#schema para leer turno
class TurnoRead(BaseModel):
    turno_id: int
    cliente_id: int
    barbero_id: int
    servicio_id: int
    fecha_hora: datetime
    estado: str
    notas: Optional[str]=None 

    class Config:
        from_attributes=True
