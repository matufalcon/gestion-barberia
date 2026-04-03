from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    usuario = Column(String(50), nullable=False, unique=True)
    contraseña = Column(String(100), nullable=False)
    telefono = Column(Integer, nullable=False)

    #relacion con barbero -> uselist relación 1:1
    barbero = relationship("Barbero", back_populates="usuario", uselist=False)