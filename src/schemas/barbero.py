from pydantic import BaseModel

# schema para creacion de barbero
class BarberoCreate(BaseModel):
    usuario_id: int
    especialidad: str
    activo: bool=True

# schema para leer barbero
class BarberoRead(BaseModel):
    barbero_id: int
    usuario_id: int
    especialidad: str
    activo: bool

    class Config:
        from_attributes = True