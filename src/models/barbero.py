from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Barbero(Base):
    __tablename__="barberos"

    barbero_id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    especialidad = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)

    #relacion con usuario
    usuario = relationship("Usuario", back_populates="barbero")


