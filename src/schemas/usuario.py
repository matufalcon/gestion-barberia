from pydantic import BaseModel, EmailStr
from typing import Optional

# schema para creacion de usuario
class UsuarioCreate(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    usuario: str
    contraseña: str
    telefono: Optional[str] = None

# schema para leer usuario
class UsuarioRead(BaseModel):
    usuario_id: int
    nombre: str
    email: str
    usuario: str
    telefono: Optional[str] = None

    class Config:
        from_attributes = True