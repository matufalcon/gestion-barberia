from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models.usuario import Usuario
from src.schemas.usuario import UsuarioCreate, UsuarioRead

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

#crear usuario
@router.post("/", response_model=UsuarioRead)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    #verificar si el email ya existe
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()

    if db_usuario:
        raise HTTPException(status_code=400, detail="Email ya registrado") #error controlado

    #crear nuevo usuario
    nuevo_usuario = Usuario(**usuario.dict())    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

#listar usuarios
@router.get("/", response_model=List[UsuarioRead])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return usuarios

#obtener un usuario por id
@router.put("/{usuario_id}", response_model=UsuarioRead)
def actualizar_usuario(usuario_id: int, usuario_actualizado: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    #actualizar campos
    for key, value in usuario_actualizado.dict().items():
        setattr(usuario, key, value)
    
    db.commit()
    db.refresh(usuario)
    return usuario

#eliminar usuario
@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado exitosamente"}
