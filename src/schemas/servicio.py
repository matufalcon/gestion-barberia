from pydantic import BaseModel

# schema para creacion de servicio
class ServicioCreate(BaseModel):
    descripcion: str
    precio: float
    duracion: int

# schema para leer servicio
class ServicioRead(BaseModel):
    servicio_id: int
    descripcion: str
    precio: float
    duracion: int

    class Config: 
        from_attributes = True